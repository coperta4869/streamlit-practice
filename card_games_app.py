import streamlit as st
# 初期化
if "count" not in st.session_state:
    st.session_state.count = 0
# 更新
if st.button("カウントアップ"):
    st.session_state.count += 1
# 表示
st.write("カウント:", st.session_state.count)