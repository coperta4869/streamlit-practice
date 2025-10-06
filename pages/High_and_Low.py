import streamlit as st
import random
import streamlit.components.v1 as components

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
if 'show_next_card' not in st.session_state:
    st.session_state.show_next_card = False

def card_name(card_num):
    """カード番号を名前に変換"""
    if card_num == 1:
        return "A"
    elif card_num == 11:
        return "J"
    elif card_num == 12:
        return "Q"
    elif card_num == 13:
        return "K"
    else:
        return str(card_num)

def get_random_suit():
    """ランダムなスートを取得"""
    return random.choice(['♠', '♥', '♦', '♣'])

def get_card_color(suit):
    """カードの色を取得"""
    return '#e74c3c' if suit in ['♥', '♦'] else '#2c3e50'

def render_card_html(card_num, suit, is_hidden=False, animate=False):
    """カードをHTMLで描画"""
    if is_hidden:
        return '''
        <div class="card card-back">
            <div class="card-pattern">🎴</div>
        </div>
        '''
    
    rank = card_name(card_num)
    color = get_card_color(suit)
    
    return f'''
    <div class="card {'flip-animation' if animate else ''}" style="color: {color}; border-color: {color};">
        <div class="card-corner top-left">
            <div class="rank">{rank}</div>
            <div class="suit">{suit}</div>
        </div>
        <div class="card-center">
            <span style="font-size: 3.5em;">{suit}</span>
        </div>
        <div class="card-corner bottom-right">
            <div class="rank">{rank}</div>
            <div class="suit">{suit}</div>
        </div>
    </div>
    '''

def display_card(card_num, suit, title, is_hidden=False, animate=False):
    """カードを表示"""
    card_html = '<div class="card-container">'
    card_html += render_card_html(card_num, suit, is_hidden, animate)
    card_html += '</div>'
    
    css = '''
    <style>
    .card-container {
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
        margin: 20px 0;
        justify-content: center;
    }
    
    .card {
        width: 120px;
        height: 170px;
        background: white;
        border-radius: 12px;
        border: 3px solid;
        box-shadow: 0 6px 12px rgba(0,0,0,0.25);
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 12px;
        transition: transform 0.3s;
    }
    
    .card:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 8px 16px rgba(0,0,0,0.35);
    }
    
    .card-back {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: #4a5568;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .card-pattern {
        font-size: 4em;
        opacity: 0.9;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.9; }
        50% { transform: scale(1.1); opacity: 1; }
    }
    
    .flip-animation {
        animation: flip 0.8s ease-in-out;
    }
    
    @keyframes flip {
        0% {
            transform: perspective(600px) rotateY(0deg);
        }
        50% {
            transform: perspective(600px) rotateY(90deg);
        }
        100% {
            transform: perspective(600px) rotateY(0deg);
        }
    }
    
    .card-corner {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-weight: bold;
    }
    
    .top-left {
        position: absolute;
        top: 12px;
        left: 12px;
    }
    
    .bottom-right {
        position: absolute;
        bottom: 12px;
        right: 12px;
        transform: rotate(180deg);
    }
    
    .rank {
        font-size: 1.6em;
        line-height: 1;
    }
    
    .suit {
        font-size: 1.2em;
        line-height: 1;
    }
    
    .card-center {
        display: flex;
        align-items: center;
        justify-content: center;
        flex: 1;
    }
    </style>
    '''
    
    st.markdown(f"**{title}**")
    components.html(css + card_html, height=220)

def display_two_cards(card1_num, suit1, card2_num, suit2):
    """2枚のカードを横並びで表示"""
    card_html = '<div class="two-card-container">'
    card_html += '<div class="card-wrapper">' + render_card_html(card1_num, suit1, False, False) + '</div>'
    card_html += '<div class="vs-text">VS</div>'
    card_html += '<div class="card-wrapper">' + render_card_html(card2_num, suit2, False, True) + '</div>'
    card_html += '</div>'
    
    css = '''
    <style>
    .two-card-container {
        display: flex;
        gap: 30px;
        align-items: center;
        justify-content: center;
        margin: 20px 0;
    }
    
    .card-wrapper {
        display: flex;
    }
    
    .vs-text {
        font-size: 2.5em;
        font-weight: bold;
        color: #667eea;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .card {
        width: 120px;
        height: 170px;
        background: white;
        border-radius: 12px;
        border: 3px solid;
        box-shadow: 0 6px 12px rgba(0,0,0,0.25);
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 12px;
        transition: transform 0.3s;
    }
    
    .card:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 8px 16px rgba(0,0,0,0.35);
    }
    
    .flip-animation {
        animation: flip 0.8s ease-in-out;
    }
    
    @keyframes flip {
        0% {
            transform: perspective(600px) rotateY(0deg);
        }
        50% {
            transform: perspective(600px) rotateY(90deg);
        }
        100% {
            transform: perspective(600px) rotateY(0deg);
        }
    }
    
    .card-corner {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-weight: bold;
    }
    
    .top-left {
        position: absolute;
        top: 12px;
        left: 12px;
    }
    
    .bottom-right {
        position: absolute;
        bottom: 12px;
        right: 12px;
        transform: rotate(180deg);
    }
    
    .rank {
        font-size: 1.6em;
        line-height: 1;
    }
    
    .suit {
        font-size: 1.2em;
        line-height: 1;
    }
    
    .card-center {
        display: flex;
        align-items: center;
        justify-content: center;
        flex: 1;
    }
    </style>
    '''
    
    components.html(css + card_html, height=220)

def show_result_animation(result_type):
    """勝敗の演出を表示"""
    if result_type == 'win':
        html_code = '''
        <style>
        body { margin: 0; padding: 0; overflow: hidden; }
        .fullscreen-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            pointer-events: none;
            z-index: 999999;
        }
        .confetti-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        .confetti {
            position: absolute;
            width: 10px;
            height: 10px;
            opacity: 0;
            animation: confetti-fall 3s ease-out forwards;
        }
        @keyframes confetti-fall {
            0% {
                opacity: 1;
                transform: translateY(-20vh) rotate(0deg);
            }
            100% {
                opacity: 0;
                transform: translateY(120vh) rotate(720deg);
            }
        }
        .win-message {
            position: relative;
            font-size: 6vw;
            font-weight: bold;
            color: #FFD700;
            text-shadow: 4px 4px 8px rgba(0,0,0,0.7), 0 0 30px rgba(255, 215, 0, 0.8);
            animation: win-bounce 1s ease-out infinite;
            z-index: 1000000;
            white-space: nowrap;
        }
        @keyframes win-bounce {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.2); }
        }
        </style>
        <div class="fullscreen-overlay">
            <div class="confetti-container" id="confetti-container"></div>
            <div class="win-message">🎉 WIN! 🎉</div>
        </div>
        <script>
        const container = document.getElementById('confetti-container');
        const colors = ['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'];
        for (let i = 0; i < 120; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.animationDelay = Math.random() * 0.5 + 's';
            confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
            container.appendChild(confetti);
        }
        setTimeout(() => {
            document.querySelector('.fullscreen-overlay').remove();
        }, 3000);
        </script>
        '''
        components.html(html_code, height=400)
    
    elif result_type == 'loss':
        html_code = '''
        <style>
        body { margin: 0; padding: 0; overflow: hidden; }
        .fullscreen-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0, 0, 0, 0.85);
            animation: fade-in-out 2s ease-out forwards;
            pointer-events: none;
            z-index: 999999;
        }
        .lose-message {
            font-size: 5vw;
            font-weight: bold;
            color: #FF4444;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.9), 0 0 20px rgba(255, 68, 68, 0.8);
            animation: shake 0.5s ease-in-out 3;
            white-space: nowrap;
        }
        @keyframes fade-in-out {
            0% { opacity: 0; }
            20% { opacity: 1; }
            80% { opacity: 1; }
            100% { opacity: 0; }
        }
        @keyframes shake {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(-8deg); }
            75% { transform: rotate(8deg); }
        }
        </style>
        <div class="fullscreen-overlay">
            <div class="lose-message">😢 LOSE 😢</div>
        </div>
        <script>
        setTimeout(() => {
            document.querySelector('.fullscreen-overlay').remove();
        }, 2000);
        </script>
        '''
        components.html(html_code, height=400)

def reset_game():
    """ゲームをリセット"""
    st.session_state.current_card = random.randint(1, 13)
    st.session_state.current_suit = get_random_suit()
    st.session_state.game_started = False
    st.session_state.result = None
    st.session_state.next_card = None
    st.session_state.prediction = None
    st.session_state.show_next_card = False
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.draws = 0
    st.session_state.total_games = 0

def make_prediction(prediction):
    """予想を行い結果を判定"""
    st.session_state.prediction = prediction
    st.session_state.next_card = random.randint(1, 13)
    st.session_state.next_suit = get_random_suit()
    st.session_state.show_next_card = True
    
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

# 初回のスート設定
if 'current_suit' not in st.session_state:
    st.session_state.current_suit = get_random_suit()

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

# 統計表示
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

# カード表示エリア（横並び）
if st.session_state.game_started and st.session_state.show_next_card:
    # 2枚のカードを横並びで表示
    st.markdown("### 🎯 現在のカード　　　　　　　🃏 次のカード")
    display_two_cards(
        st.session_state.current_card, 
        st.session_state.current_suit,
        st.session_state.next_card,
        st.session_state.next_suit
    )
else:
    # 1枚だけ表示
    st.markdown("### 🎯 現在のカード")
    display_card(st.session_state.current_card, st.session_state.current_suit, "", animate=False)

# 予想ボタン
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("📈 High (大きい)", key="high_btn", type="primary", use_container_width=True, disabled=st.session_state.game_started):
        make_prediction("high")
        st.rerun()

with col2:
    if st.button("📉 Low (小さい)", key="low_btn", type="primary", use_container_width=True, disabled=st.session_state.game_started):
        make_prediction("low")
        st.rerun()

with col3:
    if st.button("🔄 リセット", key="reset_btn", use_container_width=True):
        reset_game()
        st.rerun()

# 結果表示
if st.session_state.game_started and st.session_state.result:
    # 演出表示（結果の直後に配置）
    if st.session_state.result == "勝ち":
        show_result_animation('win')
    elif st.session_state.result == "負け":
        show_result_animation('loss')
    
    st.divider()
    
    # 予想表示
    prediction_text = "High (大きい)" if st.session_state.prediction == "high" else "Low (小さい)"
    st.markdown(f"**あなたの予想**: {prediction_text}")
    st.markdown(f"**現在**: {card_name(st.session_state.current_card)} → **次**: {card_name(st.session_state.next_card)}")
    
    # 結果表示
    if st.session_state.result == "勝ち":
        st.success(f"🎉 **{st.session_state.result}!** おめでとうございます！")
    elif st.session_state.result == "負け":
        st.error(f"😔 **{st.session_state.result}!** 残念でした！")
    else:
        st.info(f"🤝 **{st.session_state.result}!** 同じ数字でした！")
    
    # 次のゲーム
    if st.button("➡️ 続けてプレイ", key="continue_btn", type="primary", use_container_width=True):
        st.session_state.current_card = st.session_state.next_card
        st.session_state.current_suit = st.session_state.next_suit
        st.session_state.game_started = False
        st.session_state.result = None
        st.session_state.next_card = None
        st.session_state.prediction = None
        st.session_state.show_next_card = False
        st.rerun()

# フッター
st.markdown("---")
st.markdown("*💡 ヒント: カードがめくられる瞬間をお楽しみください！*")