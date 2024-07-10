import streamlit as st
import pandas as pd
import os
from io import BytesIO
import base64

def add_other_word_def(other_words, other_files, other_file_names, other_word, upload_file):
    if other_word and upload_file:
        other_words.append(other_word)
        other_files.append(upload_file)
        other_file_names.append(upload_file.name)
    else:
        st.write('請確認上傳的檔案與喚醒詞')
    return other_words, other_files, other_file_names


# 初始化狀態
if 'other_words' not in st.session_state:
    st.session_state.other_words = []
if 'other_files' not in st.session_state:
    st.session_state.other_files = []
if 'other_file_names' not in st.session_state:
    st.session_state.other_file_names = []

# 顯示基本資料輸入欄位
st.title("線上意見調查")
name = st.text_input("名字")
email = st.text_input("Email")

if name and email:
    # 調查主題1
    st.header("喚醒詞的閩南語發音及必要性調查")

    # 喚醒詞1
    st.subheader("喚醒詞1: 松下冷氣")
    st.markdown("請上傳\"松下冷氣\"的閩南語發音錄音文件")
    st.session_state.upload_file1 = st.file_uploader("上傳錄音文件", type=["wav", "mp3"], key="file1")

    # 喚醒詞2
    st.subheader("喚醒詞2: 松下空調")
    need = st.radio("是否需要", ("需要", "不需要"))
    st.session_state.upload_file2 = None
    if need == "需要":
        st.markdown("請上傳\"松下空調\"的閩南語發音錄音文件")
        st.session_state.upload_file2 = st.file_uploader("上傳錄音文件", type=["wav", "mp3"], key="file2")

    st.subheader("其他喚醒詞")
    other_word = st.text_input("請輸入其他喚醒詞")
    upload_file = st.file_uploader(f"上傳\"{other_word}\"的錄音文件", type=["wav", "mp3"], key="file_other")

    if st.button("新增"):
        st.session_state.other_words, st.session_state.other_files, st.session_state.other_file_names = add_other_word_def(
            st.session_state.other_words, st.session_state.other_files, st.session_state.other_file_names, other_word, upload_file)

    if st.session_state.upload_file1 and (need == '不需要' or (need == '需要' and st.session_state.upload_file2)):
        data = {
            "名字": name,
            "Email": email,
            '喚醒詞': ['松下冷氣'],
            '錄音檔名': [st.session_state.upload_file1.name]
        }

        if need == '需要':
            data['喚醒詞'].append('松下空調')
            data['錄音檔名'].append(st.session_state.upload_file2.name)
        # other_words, other_files, other_file_names
        # st.session_state.other_words, st.session_state.other_files, st.session_state.other_file_names
        data1={
            '名字':name,
            'Email':email,
            '喚醒詞':st.session_state.other_words,
            '錄音檔名':st.session_state.other_file_names
        }
        df1=pd.DataFrame(data1)
        df = pd.DataFrame(data)
        df=pd.concat([df,df1]).reset_index(drop=True)
        st.dataframe(df)

    else:
        data1 = {
            '名字': name,
            'Email': email,
            '喚醒詞': st.session_state.other_words,
            '錄音檔名': st.session_state.other_file_names
        }
        df = pd.DataFrame(data1)
        df

    # 收集結果
    if st.button("送出"):
        UPLOAD_FOLDER = name
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        if st.session_state.upload_file1 is not None:
            with open(os.path.join(UPLOAD_FOLDER, st.session_state.upload_file1.name), "wb") as f:
                f.write(st.session_state.upload_file1.getbuffer())
            st.success("已上傳松下冷氣的錄音文件")

        if st.session_state.upload_file2 is not None:
            with open(os.path.join(UPLOAD_FOLDER, st.session_state.upload_file2.name), "wb") as f:
                f.write(st.session_state.upload_file2.getbuffer())
            st.success("已上傳松下空調的錄音文件")
        if st.session_state.other_files:
            for upload_file3 in st.session_state.other_files:
                with open(os.path.join(UPLOAD_FOLDER, upload_file3.name), "wb") as f:
                    f.write(upload_file3.getbuffer())
                st.success(f"已上傳 {upload_file3.name} 的錄音文件")

        output = BytesIO()
        df.to_csv('紀錄.csv', index=False,mode='a',header=False)
        output.seek(0)
        st.success("資料已送出並生成 Excel 文件")
    if st.button("清空"):
        st.session_state.other_words = []
        st.session_state.other_files = []
        st.session_state.other_file_names = []


