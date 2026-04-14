import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 設定網頁標題
st.set_page_config(page_title="筆記本 AI 掃描助手", layout="centered")

st.title("📝 筆記本 AI 掃描助手")
st.info("🔒 隱私保護：辨識完成後圖片不留存，請安心使用。")

# 設定 Google API Key (從 Streamlit Secrets 讀取)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- 自動偵測並啟動模型 ---
model_list = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-1.5-flash-latest']
model = None

for m_name in model_list:
    try:
        model = genai.GenerativeModel(m_name)
        # 測試是否能正常運作
        test_response = model.generate_content("test")
        if model:
            break
    except Exception:
        continue

# 拍照功能
img_file = st.camera_input("請拍攝筆記本內容")

if img_file:
    # 讀取圖片
    image = Image.open(img_file)
    st.image(image, caption="已成功讀取照片", use_container_width=True)
    
    with st.spinner("AI 正在分析您的手寫筆記..."):
        try:
            if model is None:
                st.error("偵測到連線異常：無法對接到 Gemini 服務，請確認您的 API Key 是否已在 Google AI Studio 啟用。")
            else:
                # 提示 AI 進行結構化整理 (針對您的會議紀錄內頁設計)
                prompt = """
                這是一張手寫的會議紀錄照片。請幫我完成以下任務：
                1. 辨識所有手寫文字。
                2. 整理出「To Do 待辦事項」。
                3. 整理出「Key Takeaways 總結」。
                4. 如果有提到人名（如小明、小美），請標註其對應任務。
                請用繁體中文回答，並使用清楚的條列式排版。
                """
                
                response = model.generate_content([prompt, image])
                
                st.subheader("📋 AI 整理結果")
                st.markdown(response.text)
                st.success("整理完成！您可以直接複製上述內容。")
                
        except Exception as e:
            st.error(f"分析失敗，錯誤訊息: {e}")
            st.warning("提示：如果是 404 錯誤，通常是 Google API 的模型權限尚未完全開放，請稍後再試。")
