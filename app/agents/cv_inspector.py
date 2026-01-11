import io
import hashlib
from typing import List, Optional

import numpy as np
import torch
import clip
import cv2
from PIL import Image

from app.models.schemas import AgentIssue, CVResult, PerImageScore
from app.services.cv_model_loader import CVModelLoader


def _image_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def _estimate_blur(img_gray: np.ndarray) -> float:
    return float(cv2.Laplacian(img_gray, cv2.CV_64F).var())


def _estimate_brightness(img_gray: np.ndarray) -> float:
    return float(np.mean(img_gray) / 255.0)


def _estimate_foreground_ratio(img_gray: np.ndarray) -> float:
    edges = cv2.Canny(img_gray, 50, 150)
    return float(np.count_nonzero(edges) / edges.size)


def analyze_images(
    images: List[bytes],
    ad_text: Optional[str] = None,
) -> CVResult:
    clip_model, clip_preprocess, device = CVModelLoader.load_clip()

    per_image_scores: List[PerImageScore] = []
    global_issues: List[AgentIssue] = []

    image_embeddings = []
    relevance_scores = []

    for idx, img_bytes in enumerate(images):
        image_id = _image_hash(img_bytes)

        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img_np = np.array(pil_img)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        blur_val = _estimate_blur(gray)
        brightness = _estimate_brightness(gray)
        fg_ratio = _estimate_foreground_ratio(gray)

        issues = []

        if blur_val < 50:
            issues.append(AgentIssue(
                code="blurry",
                message="Изображение размыто",
                details={"laplacian_var": blur_val},
            ))

        if brightness < 0.25:
            issues.append(AgentIssue(
                code="too_dark",
                message="Изображение слишком тёмное",
            ))

        image_tensor = clip_preprocess(pil_img).unsqueeze(0).to(device)
        with torch.no_grad():
            img_emb = clip_model.encode_image(image_tensor)
            img_emb = img_emb / img_emb.norm(dim=-1, keepdim=True)

        image_embeddings.append(img_emb)

        relevance = None
        if ad_text:
            text_tokens = clip.tokenize([ad_text]).to(device)
            with torch.no_grad():
                text_emb = clip_model.encode_text(text_tokens)
                text_emb = text_emb / text_emb.norm(dim=-1, keepdim=True)
                similarity = float((img_emb @ text_emb.T).item())
                relevance = max(0.0, min(1.0, (similarity + 1) / 2))

            relevance_scores.append(relevance)

            if relevance < 0.3:
                issues.append(AgentIssue(
                    code="low_relevance",
                    message="Изображение плохо соответствует описанию",
                    details={"clip_similarity": similarity},
                ))

        quality_score = float(
            np.clip(
                0.4 * np.tanh(blur_val / 100)
                + 0.3 * brightness
                + 0.3 * fg_ratio,
                0.0,
                1.0,
            )
        )

        per_image_scores.append(PerImageScore(
            image_id=image_id,
            quality_score=quality_score,
            relevance_score=relevance,
            blur=blur_val,
            brightness=brightness,
            foreground_ratio=fg_ratio,
            issues=issues,
        ))

    # aggregation
    if relevance_scores:
        cv_score = float(np.mean([
            0.6 * p.quality_score + 0.4 * (p.relevance_score or 0)
            for p in per_image_scores
        ]))
    else:
        cv_score = float(np.mean([p.quality_score for p in per_image_scores]))

    suggestions = []
    if cv_score < 0.4:
        suggestions.append("Сделайте более чёткие и светлые фотографии товара")
    if relevance_scores and np.mean(relevance_scores) < 0.4:
        suggestions.append("Загрузите фото, соответствующие описанию товара")

    return CVResult(
        cv_score=cv_score,
        per_image_scores=per_image_scores,
        image_issues=[i for p in per_image_scores for i in p.issues],
        suggestions=suggestions,
    )
