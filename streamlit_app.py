import streamlit as st
import os
from pathlib import Path

# 設置 Streamlit 的文件上傳器
uploaded_file = st.file_uploader("上傳音頻文件", type=["wav", "mp3"])

if uploaded_file is not None:
    # 確保目標文件夾存在，如果不存在則創建它
    target_dir = Path("I:/python/新版網頁/意見收集網頁")
    target_dir.mkdir(parents=True, exist_ok=True)

    # 獲取文件名
    filename = uploaded_file.name

    # 保存文件到目標文件夾
    target_path = target_dir / filename
    try:
        with open(target_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success(f"成功保存文件：{filename} 到 {target_path}")
    except Exception as e:
        st.error(f"保存文件時出現錯誤：{e}")
