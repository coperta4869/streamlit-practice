import streamlit as st

# ページ設定
st.set_page_config(
    page_title="猫ちゃんカウンター",
    page_icon="🐱",
    layout="centered"
)

# 初期化
if "count" not in st.session_state:
    st.session_state.count = 0

# タイトルセクション
st.title("card game arena")
st.markdown("""
### ようこそ！
現在は2種類のゲームを作成済み！増える可能性はあまりないです。  
暇だったらボタン連打して遊んでてね
""")

st.divider()

# カウント表示
st.markdown(f"## 🎯 現在のカウント")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"<h1 style='text-align: center; font-size: 4em; color: #FF6B9D;'>{st.session_state.count}</h1>", unsafe_allow_html=True)

st.markdown("---")

# 猫ちゃんボタン（大きく表示）
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <style>
    div.stButton > button {
        background: linear-gradient(135deg, #FFB6C1 0%, #FF69B4 100%);
        border: none;
        border-radius: 50%;
        width: 200px;
        height: 200px;
        font-size: 8em;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 16px rgba(255, 105, 180, 0.3);
        position: relative;
        overflow: hidden;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 24px rgba(255, 105, 180, 0.5);
    }
    div.stButton > button:active {
        transform: scale(0.95);
    }
    </style>
    """, unsafe_allow_html=True)
    
    if st.button("🐱", key="cat_button"):
        st.session_state.count += 1
        st.rerun()

st.markdown("---")

# 達成バッジ
st.markdown("### 🏆 達成バッジ")

badges = [
    (10, "🥉 猫好き見習い", "10回クリック達成！"),
    (50, "🥈 猫マスター", "50回クリック達成！"),
    (100, "🥇 猫の達人", "100回クリック達成！"),
    (500, "👑 猫キング/クイーン", "500回クリック達成！"),
    (1000, "⭐ 伝説の猫使い", "1000回クリック達成！"),
]

cols = st.columns(len(badges))
for i, (threshold, badge, description) in enumerate(badges):
    with cols[i]:
        if st.session_state.count >= threshold:
            st.success(badge)
            st.caption(description)
        else:
            st.info(f"🔒 {threshold}回")
            st.caption(f"あと{threshold - st.session_state.count}回")

st.markdown("---")

# リセットボタン
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🔄 カウントをリセット", use_container_width=True):
        st.session_state.count = 0
        st.rerun()

# フッター
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    <p>💝 猫ちゃんを愛でて癒されよう 💝</p>
    <p style='font-size: 0.8em;'>Tip: 猫ちゃんボタンをクリックしてね！</p>
</div>
""", unsafe_allow_html=True)