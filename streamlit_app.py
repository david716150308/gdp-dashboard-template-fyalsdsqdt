import streamlit as st
from pathlib import Path

# 目標文件夾路徑
target_dir = Path("I:/python/新版網頁/意見收集網頁")

# 確保目標文件夾存在，如果不存在則創建它
target_dir.mkdir(parents=True, exist_ok=True)

# 列出目標文件夾中的所有文件和文件夾
files_in_target_dir = [item.name for item in target_dir.iterdir()]

# 顯示在目標文件夾中找到的所有文件和文件夾名稱
for file_name in files_in_target_dir:
    st.write(file_name)
