import torch
import clip
from typing import Tuple


class CVModelLoader:
    _clip_model = None
    _clip_preprocess = None
    _device = None

    @classmethod
    def load_clip(cls) -> Tuple[torch.nn.Module, callable, torch.device]:
        if cls._clip_model is not None:
            return cls._clip_model, cls._clip_preprocess, cls._device
        
        cls._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model, preprocess = clip.load("ViT-B/32", device=cls._device)
        model.eval()

        cls._clip_model = model
        cls._clip_preprocess = preprocess
        return model, preprocess, cls._device
