import streamlit as st
import random

# セッション状態の初期化
if 'current_card' not in st.session_state:
    st.session_state.current_card = random.randint(1, 13)
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'result' not in st.session_state:
    st.session_state.result = None
if 'next_card' not in st.session_state:
    st.session_state.next_card = None
if 'prediction' not in st.session_state:
    st.session_state.prediction = None
if 'wins' not in st.session_state:
    st.session_state.wins = 0
if 'losses' not in st.session_state:
    st.session_state.losses = 0
if 'draws' not in st.session_state:
    st.session_state.draws = 0
if 'total_games' not in st.session_state:
    st.session_state.total_games = 0

def card_name(card_num):
    """カード番号を名前に変換"""
    if card_num == 1:
        return "A (1)"
    elif card_num == 11:
        return "J (11)"
    elif card_num == 12:
        return "Q (12)"
    elif card_num == 13:
        return "K (13)"
    else:
        return str(card_num)

def reset_game():
    """ゲームをリセット"""
    st.session_state.current_card = random.randint(1, 13)
    st.session_state.game_started = False
    st.session_state.result = None
    st.session_state.next_card = None
    st.session_state.prediction = None
    # 統計もリセット
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.draws = 0
    st.session_state.total_games = 0

def make_prediction(prediction):
    """予想を行い結果を判定"""
    st.session_state.prediction = prediction
    st.session_state.next_card = random.randint(1, 13)
    
    # 結果判定
    if st.session_state.current_card == st.session_state.next_card:
        st.session_state.result = "引き分け"
        st.session_state.draws += 1
    elif prediction == "high" and st.session_state.next_card > st.session_state.current_card:
        st.session_state.result = "勝ち"
        st.session_state.wins += 1
    elif prediction == "low" and st.session_state.next_card < st.session_state.current_card:
        st.session_state.result = "勝ち"
        st.session_state.wins += 1
    else:
        st.session_state.result = "負け"
        st.session_state.losses += 1
    
    st.session_state.total_games += 1
    st.session_state.game_started = True

# タイトル
st.title("♠ High and Low Game!♣")

# ルール説明
st.markdown("""
## 📋 ルール説明

1. ディーラーが1から13の間でランダムにカードを選びます
2. 次に選ばれるカードが現在のカードより**大きい（High）**か**小さい（Low）**かを予想してください
3. 予想が当たれば**勝ち**、外れれば**負け**、同じ数字なら**引き分け**です

**カード表記**: A(1), 2-10, J(11), Q(12), K(13)
""")

st.divider()

# 統計表示（ゲームが開始されている場合）
if st.session_state.total_games > 0:
    st.markdown("### 📊 統計")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎉 勝ち", st.session_state.wins)
    
    with col2:
        st.metric("😔 負け", st.session_state.losses)
    
    with col3:
        st.metric("🤝 引き分け", st.session_state.draws)
    
    with col4:
        win_rate = (st.session_state.wins / st.session_state.total_games) * 100
        st.metric("🎯 勝率", f"{win_rate:.1f}%")
    
    st.markdown(f"**総ゲーム数**: {st.session_state.total_games}")
    
    st.divider()

# 現在のカード表示
st.markdown(f"### 🎯 現在のカード: **{card_name(st.session_state.current_card)}**")

# 予想ボタン
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("📈 High (大きい)", key="high_btn", type="secondary"):
        make_prediction("high")

with col2:
    if st.button("📉 Low (小さい)", key="low_btn", type="secondary"):
        make_prediction("low")

with col3:
    if st.button("🔄 新しいゲーム", key="reset_btn"):
        reset_game()
        st.rerun()

# 結果表示
if st.session_state.game_started and st.session_state.result:
    st.divider()
    
    # 次のカード表示
    st.markdown(f"### 🃏 次のカード: **{card_name(st.session_state.next_card)}**")
    
    # 予想表示
    prediction_text = "High (大きい)" if st.session_state.prediction == "high" else "Low (小さい)"
    st.markdown(f"**あなたの予想**: {prediction_text}")
    
    # 結果表示
    if st.session_state.result == "勝ち":
        st.success(f"🎉 **{st.session_state.result}!** おめでとうございます！")
    elif st.session_state.result == "負け":
        st.error(f"😔 **{st.session_state.result}!** 残念でした！")
    else:  # 引き分け
        st.info(f"🤝 **{st.session_state.result}!** 同じ数字でした！")
    
    # 次のゲームのために現在のカードを更新
    if st.button("➡️ 続けてプレイ", key="continue_btn", type="primary"):
        st.session_state.current_card = st.session_state.next_card
        st.session_state.game_started = False
        st.session_state.result = None
        st.session_state.next_card = None
        st.session_state.prediction = None
        st.rerun()

# フッター
st.markdown("---")
st.markdown("*ヒント: 確率がすべて正しいとは限りません。自らの直観を信じてみることも必要かも？*")