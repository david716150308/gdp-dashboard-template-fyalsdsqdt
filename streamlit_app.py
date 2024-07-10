import streamlit as st
import requests

# 设置 Streamlit 的文件上传器
uploaded_file = st.file_uploader("上传音频文件", type=["wav", "mp3"])

if uploaded_file is not None:
    # 保存文件到临时位置
    temp_file_path = f"/tmp/{uploaded_file.name}"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # 通过 API 将文件上传到桌机
    files = {'file': open(temp_file_path, 'rb')}
    response = requests.post("http://192.168.68.110:5000/upload", files=files)

    if response.status_code == 200:
        st.success(f"成功保存文件：{uploaded_file.name}")
    else:
        st.error("文件上传失败")
