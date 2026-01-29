import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
import random
import time

# --- ၁။ PAGE CONFIG (ဒီကောင်က အမြဲတမ်း အပေါ်ဆုံးမှာပဲ ရှိရမယ်) ---
st.set_page_config(
    page_title="Yamin's IBS Care", 
    page_icon="🌸", 
    layout="wide"
)

# --- ၂။ CSS STYLING (App တစ်ခုလုံး ပန်းရောင်သန်းပြီး အပြင် App ပုံစံပေါက်အောင်) ---
st.markdown("""
    <style>
    /* Streamlit ရဲ့ Default Header နဲ့ Footer ကို ဖျောက်တာ */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp { background-color: #fdf2f8; }
    [data-testid="stSidebar"] { background-color: #FFF0F5 !important; border-right: 2px solid #FFC0CB; }
    
    /* Tabs Style */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #FFF0F5; padding: 10px; border-radius: 15px; }
    .stTabs [data-baseweb="tab"] { height: 45px; background-color: white; border-radius: 10px; color: #FF1493 !important; font-weight: bold; padding:20px; border: 1px solid #FFC0CB; }
    .stTabs [aria-selected="true"] { background-color: #FFB6C1 !important; color: white !important; }

    .profile-outer { display: flex; justify-content: center; align-items: center; padding: 10px; }
    .circle-img { width: 120px; height: 120px; border-radius: 50%; border: 4px solid #FFB6C1; object-fit: cover; }
    
    h1, h2, h3, p, label { color: #FF1493 !important; font-family: 'Segoe UI', sans-serif; }
    div.stButton > button { background-color: #FFB6C1; color: white !important; border-radius: 20px; font-weight: bold; width: 100%; height: 50px; border: none; }
    
    .danger-alert { background-color: #FFCDD2; color: #B71C1C; padding: 15px; border-radius: 10px; border-left: 8px solid #D32F2F; font-weight: bold; }
    .water-card { background-color: #E0F7FA; padding: 15px; border-radius: 15px; border: 1px solid #4DD0E1; text-align: center; color: #00838F; font-weight: bold; }
    .tip-box { background-color: #FFF9C4; padding: 15px; border-radius: 10px; border-left: 5px solid #FBC02D; color: #7F0000; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- ၃။ HELPERS & DATA ---
def get_image_base64(image_raw):
    img = Image.open(image_raw)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

if 'all_users_data' not in st.session_state: st.session_state.all_users_data = {"Yamin": []}
if 'user_profiles' not in st.session_state: st.session_state.user_profiles = {"Yamin": {"age": 20, "weight": 50, "water": 0, "sleep": 7}}

# --- ၄။ SIDEBAR ---
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

# --- ၅။ MAIN CONTENT ---
# App Header (Custom Logo & Name)
col_title1, col_title2 = st.columns([1, 6])
with col_title1:
    # logo.png မရှိရင် icon ပြပေးမယ့် logic
    try:
        st.image("logo.png", width=80)
    except:
        st.title("🌸")

with col_title2:
    st.title(f"{current_user}'s IBS Assistant")

# Daily Tip
tips = ["ဗိုက်ကို နာရီလက်တံအတိုင်း အသာအယာ နှိပ်ပေးခြင်းက အစာကြေစေပါတယ် ✨", "စိတ်ဖိစီးမှုက IBS ကို ပိုဆိုးစေလို့ အသက်ပြင်းပြင်းရှူပေးပါ 🧘‍♀️", "အစာကို ဖြည်းဖြည်းချင်း ဝါးစားတာက လေပွတာကို သက်သာစေတယ်နော် 🍽️"]
st.markdown(f'<div class="tip-box">💡 Daily Tip: {random.choice(tips)}</div>', unsafe_allow_html=True)

st.write("") # Spacer

tab1, tab2, tab3, tab4 = st.tabs(["📝 Log Meal", "🍱 Gut Guide", "📅 History", "🧘‍♀️ Wellness"])

with tab1:
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("🕵️‍♀️ What's on your plate?")
        food = st.text_input("Enter food name:", placeholder="e.g. Spicy Noodle, Milk")
        
        bad_foods = ["အစပ်", "ဆီကြော်", "နို့", "ကော်ဖီ", "လက်ဖက်", "အချဉ်", "ကြက်သွန်ဖြူ", "မုန့်ဟင်းခါး","အုန်းနို့ခေါက်ဆွဲ","လက်ဖက်ရည်","ကြက်သွန်နီ","ပေါင်မုန့်","ကိတ်မုန့်"]
        is_risky = False
        if food:
            if any(x in food.lower() for x in bad_foods):
                st.markdown(f'<div class="danger-alert">❌ သတိ! "{food}" က {current_user} ဗိုက်နဲ့ မတည့်ဘူးနော်။</div>', unsafe_allow_html=True)
                is_risky = True
            else:
                st.success(f"✅ '{food}' က စားလို့ရနိုင်တဲ့ အစာဖြစ်ပုံရပါတယ်။")
        
        mood = st.select_slider("How is your mood?", options=["😭", "😐", "😊", "💖", "✨"], value="😊")
        pain = st.slider("Pain Level (0-5)", 0, 5, 0)
        
        if st.button("Save Entry 💖"):
            if food:
                st.session_state.all_users_data[current_user].append({
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"), 
                    "Food": food, 
                    "Status": "Risky ⚠️" if is_risky else "Safe ✅",
                    "Mood": mood, 
                    "Pain": pain
                })
                st.balloons()
                st.rerun()

    with col_r:
        st.markdown(f'<div class="water-card">💧 Water<br><span style="font-size:25px;">{p_info["water"]}/8 Glasses</span></div>', unsafe_allow_html=True)
        if st.button("Add Glass 🥤"): 
            p_info["water"] += 1
            st.rerun()
        st.write("")
        p_info["sleep"] = st.number_input("Sleep (Hours) 🌙", value=p_info["sleep"])

with tab2:
    st.subheader("🍱 Food Database")
    c1, c2 = st.columns(2)
    c1.success("**Safe Foods:**\n- Rice & Chicken\n- Carrots & Papaya\n- Eggs\n- Soup")
    c2.error("**Avoid Foods:**\n- Spicy & Fried\n- Dairy (Milk/Ice cream)\n- Onions & Garlic\n- Coffee/Tea")

with tab3:
    st.subheader("📊 Your Journey")
    history = st.session_state.all_users_data.get(current_user, [])
    if history:
        st.table(pd.DataFrame(history).iloc[::-1])
    else:
        st.info("မှတ်တမ်း မရှိသေးပါ။")

with tab4:
    st.subheader("🧘‍♀️ Breathe & Relax")
    if st.button("Start Breathing Exercise ⏱️"):
        placeholder = st.empty()
        for i in range(10, 0, -1):
            placeholder.subheader(f"🌬️ အသက်ကို ဖြည်းဖြည်းချင်း ရှူသွင်း/ရှူထုတ်ပါ... {i}")
            time.sleep(1)
        placeholder.success("✨ စိတ်ထဲ ပေါ့ပါးသွားပြီလား?")
