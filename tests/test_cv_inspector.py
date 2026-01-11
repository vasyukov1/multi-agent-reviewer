import numpy as np
import cv2
from app.agents.cv_inspector import analyze_images


def _fake_image(color=255, blur=False):
    img = np.ones((224, 224, 3), dtype=np.uint8) * color
    if blur:
        img = cv2.GaussianBlur(img, (21, 21), 0)
    _, buf = cv2.imencode(".jpg", img)
    return buf.tobytes()


def test_good_ad():
    imgs = [_fake_image(200), _fake_image(220)]
    res = analyze_images(imgs, ad_text="Белая футболка")

    assert res.cv_score > 0.6
    assert len(res.image_issues) == 0


def test_blurry_ad():
    imgs = [_fake_image(200, blur=True)]
    res = analyze_images(imgs, ad_text="Смартфон")

    assert res.cv_score < 0.5
    assert any(i.code == "blurry" for i in res.image_issues)


def test_mismatch_ad():
    imgs = [_fake_image(255)]
    res = analyze_images(imgs, ad_text="Красные кроссовки")

    assert any(i.code == "low_relevance" for i in res.image_issues)
