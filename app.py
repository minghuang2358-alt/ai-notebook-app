import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 頁面標題
st.set_page_config(page_title="明鍠文具 AI 助手")
st.title("📝 筆記本 AI 掃描助手")

# --- 設定 API Key (請確保這裡貼的是 A 帳號那串) ---
GOOGLE_API_KEY = "AIzaSyDvDPjcxA7arMy_sZUQgCsn5kHhxo_nCxY"
genai.configure(api_key=GOOGLE_API_KEY)

st.info("🔒 隱私保護：辨識完成後圖片不留存，請安心使用。")

# 手機相機元件
img_file_buffer = st.camera_input("請拍攝筆記本內容")

if img_file_buffer is not None:
    img = Image.open(img_file_buffer)
    with st.spinner('AI 正在讀取手寫文字...'):
        try:
            # 【保險機制】自動尋找可用的模型名稱
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = "你是一位專業的文具助手。請精確辨識附圖中的手寫繁體中文內容，並依據專案、日期、成員、筆記、待辦事項、總結等欄位進行整理。請用易讀的 Markdown 格式輸出。"
            
            # 加上 stream=False 確保穩定性
            response = model.generate_content([prompt, img])
            
            if response.text:
                st.success("分析完成！")
                st.markdown(response.text)
                
                st.download_button(
                    label="📥 下載整理後的內容 (.txt)",
                    data=response.text,
                    file_name="meeting_notes.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"偵測到連線異常：{e}")
            st.warning("提示：請確認您的 API Key 是否已在 Google AI Studio 啟用，或稍後再試。")
