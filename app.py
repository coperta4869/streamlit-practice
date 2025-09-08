import streamlit as st

# アプリのタイトル
st.title("簡単計算機")
st.write("2つの数字を入力して、基本的な計算を行います")

# 2つの数字の入力欄
col1, col2 = st.columns(2)

with col1:
    input1 = st.text_input("1つ目の数字", value="0", placeholder="数字を入力してください")

with col2:
    input2 = st.text_input("2つ目の数字", value="0", placeholder="数字を入力してください")

# 入力値の検証と計算
if input1 and input2:
    try:
        # 文字列を数値に変換
        num1 = float(input1)
        num2 = float(input2)
        
        # 計算結果を表示
        st.subheader("計算結果")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("足し算", f"{num1 + num2}")
            st.write(f"{num1} + {num2} = {num1 + num2}")
            
            st.metric("引き算", f"{num1 - num2}")
            st.write(f"{num1} - {num2} = {num1 - num2}")
        
        with col2:
            st.metric("掛け算", f"{num1 * num2}")
            st.write(f"{num1} × {num2} = {num1 * num2}")
            
            # 割り算はゼロ除算をチェック
            if num2 != 0:
                st.metric("割り算", f"{num1 / num2:.4f}")
                st.write(f"{num1} ÷ {num2} = {num1 / num2:.4f}")
            else:
                st.error("割り算: ゼロで割ることはできません")
        
    except ValueError:
        # 数字以外が入力された場合のエラーメッセージ
        st.error("⚠️ 数字を入力してください。小数点や負の数も使用できます。")
        
        # どちらの入力が問題かを特定
        error_details = []
        try:
            float(input1)
        except ValueError:
            error_details.append(f"1つ目の入力: '{input1}' は数字ではありません")
            
        try:
            float(input2)
        except ValueError:
            error_details.append(f"2つ目の入力: '{input2}' は数字ではありません")
        
        for detail in error_details:
            st.write(f"- {detail}")

elif input1 or input2:
    # どちらか一方しか入力されていない場合
    st.info("両方の入力欄に数字を入力してください")

# 使用方法の説明
with st.expander("使用方法"):
    st.write("""
    1. 上の2つの入力欄に数字を入力してください
    2. 整数、小数、負の数も使用できます
    3. 両方の数字を入力すると、自動で計算結果が表示されます
    4. 数字以外を入力するとエラーメッセージが表示されます
    
    **例:**
    - 正の数: 10, 3.14
    - 負の数: -5, -2.5
    - 小数: 0.5, 123.456
    """)