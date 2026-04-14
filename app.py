import streamlit as st
import google.generativeai as genai
from PIL import Image

# 頁面標題與設定
st.set_page_config(page_title="筆記本 AI 掃描助手", layout="centered")
st.title("📝 筆記本 AI 掃描助手")

# 隱私聲明
st.info("🔒 隱私保護：辨識完成後圖片不留存，請安心使用。")

# 設定 API Key (請確保已在 Streamlit Secrets 設定或直接貼上)
# 建議做法：在 Streamlit 部署網頁的 Settings -> Secrets 加入：GOOGLE_API_KEY = "您的金鑰"
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    # 如果沒設定 Secrets，請在此暫時填入您的 API Key 做測試
    genai.configure(api_key="AIzaSyDvDPjcxA7arMy_sZUQgCsn5kHhxo_nCxY")

# --- 核心模型連線邏輯 ---
try:
    # 嘗試多種可能的路徑格式，解決 v1beta 版本連線問題
    model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-1.5-flash-latest']
    model = None
    
    for name in model_names:
        try:
            temp_model = genai.GenerativeModel(name)
            # 測試連線
            model = temp_model
            break
        except:
            continue
            
    if model is None:
        st.error("無法連線至 Gemini 模型，請檢查 Google AI Studio 權限。")
except Exception as e:
    st.error(f"系統初始化失敗：{e}")

# 相機輸入組件
img_file = st.camera_input("請拍攝筆記本內容")

if img_file:
    # 轉換圖片格式
    img = Image.open(img_file)
    st.image(img, caption="已成功讀取照片", use_container_width=True)
    
    with st.spinner("AI 正在分析您的筆記，請稍候..."):
        try:
            # 設計精準的 Prompt，針對您的會議記錄模板
            prompt = """
            你是一個專業的筆記整理助手。請辨識這張照片中的手寫文字內容，並按照以下格式整理輸出：
            1. **會議基本資訊**：包含主題、日期、成員、地點。
            2. **詳細筆記內容**：逐條列出照片中記錄的發言或重點。
            3. **To-Do 待辦事項**：從筆記中提取所有需要後續執行的任務。
            4. **Key Takeaways 總結**：提供這份筆記的核心結論。
            請使用繁體中文回答。
            """
            
            # 執行辨識
            response = model.generate_content([prompt, img])
            
            # 顯示結果
            st.success("辨識完成！")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"偵測到連線異常：{e}")
            st.warning("提示：請確認您的 API Key 是否已在 Google AI Studio 啟用，或稍後再試。")
