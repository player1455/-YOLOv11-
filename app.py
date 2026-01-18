# infer_only.py
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO

# -------------------------
# 1. 加载模型（全局只加载一次）
# -------------------------
model = YOLO("weights/best.pt")      # 换成你的权重路径

# -------------------------
# 2. 纯推理函数
# -------------------------
def infer_image(image_pil: Image.Image,
                conf: float = 0.25,
                iou: float = 0.45,
                imgsz: int = 640) -> np.ndarray:
    """
    输入 PIL 图片，返回画好框的 RGB ndarray
    """
    img_np = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
    results = model.predict(source=img_np,
                            imgsz=imgsz,
                            conf=conf,
                            iou=iou,
                            save=False)
    plotted_bgr = results[0].plot()
    return cv2.cvtColor(plotted_bgr, cv2.COLOR_BGR2RGB)

# -------------------------
# 3. 使用示例（可直接 import 调用）
# -------------------------
if __name__ == "__main__":
    src = Image.open("C:\\Users\\hh\\Downloads\\OIP-C.jpg").convert("RGB")
    out = infer_image(src, conf=0.25, iou=0.45)
    Image.fromarray(out).save("result.jpg")