import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
import random

# 1. Page Config
st.set_page_config(page_title="IBS Personal Assistant", page_icon="🎀", layout="wide")

# 2. CSS Styling
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #FFF0F5 !important; border-right: 2px solid #FFC0CB; }
    
    /* Nav Bar (Tabs) */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #FFF0F5; padding: 10px; border-radius: 15px; }
    .stTabs [data-baseweb="tab"] { height: 45px; background-color: white; border-radius: 10px; color: #FF1493; font-weight: bold; border: 1px solid #FFC0CB; padding:20px; }
    .stTabs [aria-selected="true"] { background-color: #FFB6C1 !important; color: white !important; }

    .profile-outer { display: flex; justify-content: center; align-items: center; padding: 10px; }
    .circle-img { width: 120px; height: 120px; border-radius: 50%; border: 4px solid #FFB6C1; object-fit: cover; }
    
    .mini-card { background-color: #FDF2F8; padding: 15px; border-radius: 15px; border: 1px solid #FFC0CB; margin-bottom: 10px; }
    .water-card { background-color: #E0F7FA; padding: 10px; border-radius: 15px; border: 1px solid #4DD0E1; text-align: center; color: #00838F; font-weight: bold; }
    
    h1, h2, h3, p, label { color: #FF1493 !important; }
    div.stButton > button { background-color: #FFB6C1; color: white !important; border-radius: 20px; font-weight: bold; margin:10px; }
    .danger-alert { background-color: #FFCDD2; color: #B71C1C; padding: 10px; border-radius: 10px; border-left: 5px solid #D32F2F; margin-bottom: 10px; }
    .tip-box { background-color: #FFF9C4; padding: 10px; border-radius: 10px; border-left: 5px solid #FBC02D; color: #7F0000; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- Function for Circle Image ---
def get_image_base64(image_raw):
    img = Image.open(image_raw)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- 🔐 DATA PRESERVATION LOGIC ---
if 'all_users_data' not in st.session_state: st.session_state.all_users_data = {"Yamin": []}
if 'user_profiles' not in st.session_state: st.session_state.user_profiles = {"Yamin": {"age": 20, "weight": 50, "water": 0, "sleep": 7}}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h3 style='text-align: center;'>User Profile</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Photo", type=["jpg", "png", "jpeg"], key="top_pf")
    
    st.markdown('<div class="profile-outer">', unsafe_allow_html=True)
    if uploaded_file:
        img_base64 = get_image_base64(uploaded_file)
        st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="circle-img">', unsafe_allow_html=True)
    else:
        st.markdown(f'<img src="https://cdn-icons-png.flaticon.com/512/6522/6522516.png" class="circle-img">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    current_user = st.text_input("Profile Name:", value="Yamin")
    if current_user not in st.session_state.user_profiles:
        st.session_state.user_profiles[current_user] = {"age": 20, "weight": 50, "water": 0, "sleep": 7}
        st.session_state.all_users_data[current_user] = []
    
    p_info = st.session_state.user_profiles[current_user]
    p_info["age"] = st.number_input("Age", value=p_info["age"])
    
    st.divider()
    st.write("⏰ **Medicine Reminder**")
    st.checkbox("Morning Probiotics 💊")
    st.checkbox("Digestive Enzyme 🧪")

# --- MAIN CONTENT ---
st.title(f"🌸 {current_user}'s IBS Assistant")

# --- DAILY TIPS (Random) ---
tips = [
    "ဗိုက်ကို နာရီလက်တံအတိုင်း အသာအယာ နှိပ်ပေးခြင်းက အစာကြေစေပါတယ် ✨",
    "စိတ်ဖိစီးမှုက IBS ကို ပိုဆိုးစေလို့ အသက်ပြင်းပြင်းရှူပေးပါ 🧘‍♀️",
    "အစာကို ဖြည်းဖြည်းချင်း ဝါးစားတာက လေပွတာကို သက်သာစေတယ်နော် 🍽️",
    "ရေနွေးနွေးလေး သောက်ပေးတာက အစာအိမ်ကြွက်သားတွေကို ပြေလျော့စေပါတယ် ☕"
]
st.markdown(f'<div class="tip-box">💡 Daily Tip: {random.choice(tips)}</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📝 Log", "🍱 Guide", "📊 History", "🧘‍♀️ Wellness"])

with tab1:
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("🕵️‍♀️ Log Meal")
        food = st.text_input("What did you eat?", key=f"f_{current_user}")
        bad_foods = ["အစပ်", "ဆီကြော်", "နို့", "ကော်ဖီ", "လက်ဖက်", "အချဉ်", "ကြက်သွန်ဖြူ","ကော်ဖီ","လက်ဖက်ရည်","ကိတ်မုန့်","ပေါင်မုန့်","မုန့်ဟင်းခါး","အုန်းနို့ခေါက်ဆွဲ"]
        if food and any(x in food.lower() for x in bad_foods):
            st.markdown(f'<div class="danger-alert">⚠️ သတိ! "{food}" က မတည့်ပါဘူးနော်။</div>', unsafe_allow_html=True)
        
        mood = st.select_slider("Mood", options=["😭", "😐", "😊", "💖", "✨"], value="😊")
        pain = st.slider("Pain Level", 0, 5, 0)
        
        if st.button("Save Log 💖"):
            if food:
                st.session_state.all_users_data[current_user].append({
                    "Date": datetime.now().strftime("%Y-%m-%d"), "Food": food, 
                    "Status": "Risky ⚠️" if any(x in food.lower() for x in bad_foods) else "Safe ✅",
                    "Mood": mood, "Pain": pain
                })
                st.success("Saved!")
                st.rerun()
    
    with col_r:
        st.subheader("💧 & 😴")
        st.markdown(f'<div class="water-card">Water: {p_info["water"]}/8</div>', unsafe_allow_html=True)
        if st.button("Drink 🥤"): 
            p_info["water"] += 1
            st.rerun()
        
        p_info["sleep"] = st.number_input("Sleep Hours 🌙", value=p_info["sleep"], min_value=0, max_value=24)

with tab2:
    st.subheader("🍱 Gut Guide")
    
    st.success("**Safe:** Rice, Chicken, Carrots, Banana, Soup, Papaya.")
    st.error("**Avoid:** Milk, Spicy, Fried, Onions, Garlic.")

with tab3:
    st.subheader("📅 Records")
    user_history = st.session_state.all_users_data.get(current_user, [])
    if user_history:
        st.dataframe(pd.DataFrame(user_history).iloc[::-1], use_container_width=True)
    else: st.info("No records.")

with tab4:
    st.subheader("🧘‍♀️ 3-Minute Breathing")
    st.write("IBS သက်သာဖို့ စိတ်ကို အေးအေးထားပြီး အသက်ရှူလေ့ကျင့်ခန်း လုပ်ရအောင်။")
    
    if st.button("Start Timer ⏱️"):
        with st.empty():
            for i in range(10, 0, -1):
                st.write(f"💨 အသက်ကို ဖြည်းဖြည်းချင်း ရှူသွင်း/ရှူထုတ်ပါ... {i}")
                import time
                time.sleep(1)
            st.write("✨ အရမ်းတော်တယ်! စိတ်ထဲ ပေါ့ပါးသွားပြီလား?")