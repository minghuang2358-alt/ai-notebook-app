import streamlit as st
import google.generativeai as genai
from PIL import Image

# 頁面標題
st.set_page_config(page_title="明鍠文具 AI 助手")
st.title("📝 筆記本 AI 掃描助手")

# 設定 API Key
GOOGLE_API_KEY = "AIzaSyDvDPjcxA7arMy_sZUQgCsn5kHhxo_nCxY"
genai.configure(api_key=GOOGLE_API_KEY)

st.info("🔒 隱私保護：辨識完成後圖片不留存，請安心使用。")

# 手機相機元件
img_file_buffer = st.camera_input("請拍攝筆記本內容")

if img_file_buffer is not None:
    img = Image.open(img_file_buffer)
    with st.spinner('AI 正在讀取手寫文字...'):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = "請精確辨識附圖中的手寫繁體中文內容，並依據專案、日期、成員、筆記、待辦、總結等欄位進行整理。"
            response = model.generate_content([prompt, img])
            
            st.success("分析完成！")
            st.markdown(response.text)
            
            st.download_button(
                label="📥 下載整理後的內容 (.txt)",
                data=response.text,
                file_name="meeting_notes.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"錯誤：{e}")