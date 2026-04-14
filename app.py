import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 基礎網頁設定
st.set_page_config(page_title="明鍠 AI 筆記助手", layout="centered")
st.title("📝 明鍠 AI 筆記助手")
st.info("🔒 隱私保護：照片僅供即時分析，不留存於雲端。")

# 2. 設定 API Key (從 Secrets 讀取)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("❌ 找不到 API Key，請確保 Streamlit Secrets 已設定 GOOGLE_API_KEY")

# 3. 啟動模型 (直接使用最穩定的 Flash 版本名稱)
# 這次我們不加 models/ 前綴，讓 SDK 自己處理
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. 拍照功能
img_file = st.camera_input("請拍攝您的筆記內容")

if img_file:
    image = Image.open(img_file)
    st.image(image, caption="照片已讀取", use_container_width=True)
    
    with st.spinner("AI 正在思考中..."):
        try:
            # 針對您的 2026 會議紀錄設計的專屬指令
            prompt = """
            你現在是明鍠文具的 AI 助手。請分析這張會議紀錄照片：
            1. 條列出「To Do 待辦事項」及其負責人（如：王小明、童小美）。
            2. 總結「Key Takeaways 總結」中的核心重點。
            3. 如果有日期或截止時間，請特別標註。
            請使用繁體中文，格式要整齊好讀。
            """
            
            # 執行辨識
            response = model.generate_content([prompt, image])
            
            st.subheader("📋 整理結果")
            st.markdown(response.text)
            st.success("分析完成！")
            
        except Exception as e:
            # 如果還是報 404，我們提示可能是 Google 帳號地區或 API Key 尚未生效
            st.error(f"分析失敗。")
            st.warning(f"技術詳情：{e}")
            if "404" in str(e):
                st.info("💡 提示：這通常代表 Google AI Studio 的 API Key 剛建立，系統還在同步。請等待 5 分鐘後重新整理網頁再試。")
