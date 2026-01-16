import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import tempfile
import os
import time
# -------------------------
# 页面配置
# -------------------------
st.set_page_config(
    page_title="YOLO 障碍物识别系统",
    layout="wide"
)
# test


st.title("🚧 YOLO 障碍物识别推理系统")
st.markdown("仅用于 **推理（Inference）**，不包含训练功能")

# -------------------------
# 加载模型（只加载一次）
# -------------------------
@st.cache_resource
def load_model(weight_path):
    return YOLO(weight_path)

model = load_model("weights/best.pt")

# -------------------------
# 侧边栏：超参数设置
# -------------------------
st.sidebar.header("⚙️ 推理参数设置")



conf = st.sidebar.slider(
    "置信度阈值 (conf)",
    min_value=0.0,
    max_value=1.0,
    step=0.05,
    value=0.25
)

iou = st.sidebar.slider(
    "IoU 阈值 (iou)",
    min_value=0.0,
    max_value=1.0,
    step=0.05,
    value=0.45
)


# 输入源选择
mode = st.sidebar.radio(
    "输入源",
    ['图片','摄像头']
)

# -------------------------
# 推理逻辑图片
# -------------------------
if mode == '图片':
    imgsz = st.sidebar.slider(
        "输入图片大小 (imgsz)",
        min_value=320,
        max_value=1280,
        step=32,
        value=640
    )

    # -------------------------
    # 图片上传
    # -------------------------
    uploaded_file = st.file_uploader(
        "📷 上传待检测图片",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )
    if uploaded_file is not None and st.button("🔍 开始检测"):
        # 显示原图
        # image = Image.open(uploaded_file).convert("RGB")
        col1, col2 = st.columns(2)
        for uploaded_file in uploaded_file:
            image = Image.open(uploaded_file).convert('RGB')

            with col1:
                st.subheader("原始图片")
                st.image(image, use_container_width=True)

            with st.spinner("YOLO 推理中..."):
                img_np = np.array(image)

                # RGB -> BGR（YOLO / OpenCV 习惯）
                img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)


                # YOLO 推理
                results = model.predict(
                    source= img_np,
                    imgsz=imgsz,
                    conf=conf,
                    iou=iou,
                    save=False
                )

                # 取第一张结果
                result = results[0]
                plotted_img = result.plot()  # BGR ndarray

                # BGR -> RGB
                plotted_img = cv2.cvtColor(plotted_img, cv2.COLOR_BGR2RGB)

                with col2:
                    st.subheader("检测结果")
                    st.image(plotted_img, use_container_width=True)

                # 可选：显示检测信息
                st.subheader("📋 检测结果详情")
                if result.boxes is not None:
                    for box in result.boxes:
                        cls_id = int(box.cls[0])
                        conf_score = float(box.conf[0])
                        class_name = model.names[cls_id]
                        st.write(f"- **{class_name}** | 置信度: `{conf_score:.2f}`")
elif mode == '摄像头':

    # 自己调整显示大小
    display_width = st.sidebar.slider(
        "显示画面宽度",
        min_value=320,
        max_value=1280,
        step=40,
        value=720,
        key="display_width"
    )

    st.subheader("实时摄像头推理")

    if 'cam_running' not in st.session_state:
        st.session_state.cam_running = False

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("启动摄像头", key='start_running'):
            st.session_state.cam_running = True

    with col_btn2:
        if st.button("停止摄像头" , key='stop_running'):
            st.session_state.cam_running = False

    frame_placeholder = st.empty()

    if st.session_state.cam_running:
        cap = cv2.VideoCapture(0)
        # 设置镜头采集的分辨率
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

        if not cap.isOpened():
            st.error("无法打开摄像")
        else:
            while st.session_state.cam_running:
                start_time = time.time()

                ret, frame = cap.read()
                if not ret:
                    st.warning("无法读取摄像头画面")
                    break

                results = model.predict(
                    source=frame,
                    conf=conf,
                    iou=iou,
                    stream=False,
                    verbose=False
                )
                # 绘制FPS
                end_time = time.time()
                fps = 1 / (end_time - start_time)
                st.caption(f"FPS: {fps:.2f}")
                # 绘制结果
                result = results[0]
                plotted_frame = result.plot()
                # 在图像上显示FPS
                cv2.putText(
                    plotted_frame,
                    f"FPS: {fps:.2f}",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )
                plotted_frame = cv2.cvtColor(plotted_frame, cv2.COLOR_BGR2RGB)

                frame_placeholder.image(
                    plotted_frame,
                    channels='RGB',
                    # use_container_width=True
                    width=display_width
                )
            cap.release()


