import streamlit as st
import random
import streamlit.components.v1 as components

# セッション状態の初期化
if 'player_cards' not in st.session_state:
    st.session_state.player_cards = []
if 'dealer_cards' not in st.session_state:
    st.session_state.dealer_cards = []
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'start'
if 'result' not in st.session_state:
    st.session_state.result = None
if 'wins' not in st.session_state:
    st.session_state.wins = 0
if 'losses' not in st.session_state:
    st.session_state.losses = 0
if 'draws' not in st.session_state:
    st.session_state.draws = 0
if 'total_games' not in st.session_state:
    st.session_state.total_games = 0
if 'dealer_hidden' not in st.session_state:
    st.session_state.dealer_hidden = True
if 'coins' not in st.session_state:
    st.session_state.coins = 100
if 'current_bet' not in st.session_state:
    st.session_state.current_bet = 0
if 'is_doubled_down' not in st.session_state:
    st.session_state.is_doubled_down = False
if 'blackjack_bonus' not in st.session_state:
    st.session_state.blackjack_bonus = False

def create_deck():
    """デッキを作成"""
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(f"{rank}{suit}")
    return deck

def card_value(card):
    """カードの値を返す"""
    rank = card[:-1]
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)

def calculate_hand_value(cards):
    """手札の合計値を計算"""
    total = 0
    aces = 0
    
    for card in cards:
        value = card_value(card)
        if card[:-1] == 'A':
            aces += 1
        total += value
    
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    
    return total

def deal_card():
    """カードを1枚配る"""
    deck = create_deck()
    return random.choice(deck)

def get_card_color(card):
    """カードの色を取得"""
    suit = card[-1]
    return '#e74c3c' if suit in ['♥', '♦'] else '#2c3e50'

def render_card_html(card, is_hidden=False, animate=False):
    """カードをHTMLで描画"""
    if is_hidden:
        return f'''
        <div class="card card-back {'flip-animation' if animate else ''}">
            <div class="card-pattern">🎴</div>
        </div>
        '''
    
    rank = card[:-1]
    suit = card[-1]
    color = get_card_color(card)
    
    return f'''
    <div class="card {'flip-animation' if animate else ''}" style="color: {color}; border-color: {color};">
        <div class="card-corner top-left">
            <div class="rank">{rank}</div>
            <div class="suit">{suit}</div>
        </div>
        <div class="card-center">
            <span style="font-size: 3em;">{suit}</span>
        </div>
        <div class="card-corner bottom-right">
            <div class="rank">{rank}</div>
            <div class="suit">{suit}</div>
        </div>
    </div>
    '''

def display_cards_animated(cards, title, hide_first=False):
    """アニメーション付きカード表示"""
    total = calculate_hand_value([c for i, c in enumerate(cards) if not (hide_first and i == 0)])
    
    card_html = '<div class="card-container">'
    for i, card in enumerate(cards):
        is_hidden = hide_first and i == 0
        animate = i == len(cards) - 1
        card_html += render_card_html(card, is_hidden, animate)
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
        border-radius: 10px;
        border: 3px solid;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 10px;
        transition: transform 0.3s;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
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
        opacity: 0.8;
    }
    
    .flip-animation {
        animation: flip 0.6s ease-in-out;
    }
    
    @keyframes flip {
        0% {
            transform: perspective(400px) rotateY(0deg);
        }
        50% {
            transform: perspective(400px) rotateY(90deg);
        }
        100% {
            transform: perspective(400px) rotateY(0deg);
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
        top: 10px;
        left: 10px;
    }
    
    .bottom-right {
        position: absolute;
        bottom: 10px;
        right: 10px;
        transform: rotate(180deg);
    }
    
    .rank {
        font-size: 1.5em;
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
    
    if hide_first and len(cards) > 1:
        visible_total = calculate_hand_value(cards[1:])
        st.markdown(f"**合計: {visible_total} + ?**")
    else:
        st.markdown(f"**合計: {total}**")
    
    return total

def show_result_animation(result_type):
    """勝敗の演出を表示"""
    if result_type == 'win':
        # 勝利時の紙吹雪エフェクト
        html_code = '''
        <style>
        .confetti-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
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
                transform: translateY(-100px) rotate(0deg);
            }
            100% {
                opacity: 0;
                transform: translateY(100vh) rotate(720deg);
            }
        }
        .win-message {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 4em;
            font-weight: bold;
            color: #FFD700;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
            animation: win-bounce 1s ease-out;
            pointer-events: none;
            z-index: 10000;
        }
        @keyframes win-bounce {
            0%, 100% { transform: translate(-50%, -50%) scale(1); }
            50% { transform: translate(-50%, -50%) scale(1.3); }
        }
        </style>
        <div class="confetti-container" id="confetti-container"></div>
        <div class="win-message">🎉 WIN!</div>
        <script>
        const container = document.getElementById('confetti-container');
        const colors = ['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'];
        for (let i = 0; i < 100; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.animationDelay = Math.random() * 0.5 + 's';
            confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
            container.appendChild(confetti);
        }
        setTimeout(() => {
            container.remove();
            document.querySelector('.win-message').remove();
        }, 3000);
        </script>
        '''
        components.html(html_code, height=0)
    
    elif result_type == 'loss':
        # 敗北時の暗転エフェクト
        html_code = '''
        <style>
        .lose-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 9999;
            animation: fade-in-out 2s ease-out forwards;
            pointer-events: none;
        }
        .lose-message {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 3em;
            font-weight: bold;
            color: #FF4444;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            animation: shake 0.5s ease-in-out;
            pointer-events: none;
            z-index: 10000;
        }
        @keyframes fade-in-out {
            0% { opacity: 0; }
            50% { opacity: 1; }
            100% { opacity: 0; }
        }
        @keyframes shake {
            0%, 100% { transform: translate(-50%, -50%) rotate(0deg); }
            25% { transform: translate(-50%, -50%) rotate(-5deg); }
            75% { transform: translate(-50%, -50%) rotate(5deg); }
        }
        </style>
        <div class="lose-overlay"></div>
        <div class="lose-message">😢 LOSE </div>
        <script>
        setTimeout(() => {
            document.querySelector('.lose-overlay').remove();
            document.querySelector('.lose-message').remove();
        }, 2000);
        </script>
        '''
        components.html(html_code, height=0)
    
    elif result_type == 'blackjack':
        # ブラックジャック時の特別演出
        html_code = '''
        <style>
        .blackjack-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
        }
        .star {
            position: absolute;
            color: gold;
            font-size: 2em;
            animation: star-burst 1.5s ease-out forwards;
        }
        @keyframes star-burst {
            0% {
                opacity: 1;
                transform: translate(0, 0) scale(0);
            }
            100% {
                opacity: 0;
                transform: translate(var(--tx), var(--ty)) scale(1);
            }
        }
        .blackjack-message {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 4em;
            font-weight: bold;
            background: linear-gradient(45deg, #FFD700, #FFA500, #FFD700);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient-shift 2s ease infinite, blackjack-pulse 1s ease-out;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
            pointer-events: none;
            z-index: 10000;
        }
        @keyframes gradient-shift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        @keyframes blackjack-pulse {
            0%, 100% { transform: translate(-50%, -50%) scale(1); }
            50% { transform: translate(-50%, -50%) scale(1.2); }
        }
        </style>
        <div class="blackjack-container" id="star-container"></div>
        <div class="blackjack-message">⭐ BLACKJACK! </div>
        <script>
        const container = document.getElementById('star-container');
        for (let i = 0; i < 30; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            star.textContent = '⭐';
            star.style.left = '50%';
            star.style.top = '50%';
            const angle = (i / 30) * Math.PI * 2;
            const distance = 200 + Math.random() * 200;
            star.style.setProperty('--tx', Math.cos(angle) * distance + 'px');
            star.style.setProperty('--ty', Math.sin(angle) * distance + 'px');
            star.style.animationDelay = (i * 0.05) + 's';
            container.appendChild(star);
        }
        setTimeout(() => {
            container.remove();
            document.querySelector('.blackjack-message').remove();
        }, 2500);
        </script>
        '''
        components.html(html_code, height=0)

def start_new_game():
    """新しいゲームを開始"""
    if st.session_state.coins <= 0:
        st.error("コインが不足しています！ゲームをリセットしてください。")
        return
    st.session_state.game_state = 'betting'

def place_bet(bet_amount):
    """ベットを設定してゲーム開始"""
    st.session_state.current_bet = bet_amount
    st.session_state.coins -= bet_amount
    st.session_state.player_cards = [deal_card(), deal_card()]
    st.session_state.dealer_cards = [deal_card(), deal_card()]
    st.session_state.game_state = 'playing'
    st.session_state.result = None
    st.session_state.dealer_hidden = True
    st.session_state.is_doubled_down = False
    st.session_state.blackjack_bonus = False
    
    if calculate_hand_value(st.session_state.player_cards) == 21:
        st.session_state.blackjack_bonus = True
        stand()

def double_down():
    """ダブルダウン"""
    if st.session_state.coins >= st.session_state.current_bet:
        st.session_state.coins -= st.session_state.current_bet
        st.session_state.current_bet *= 2
        st.session_state.is_doubled_down = True
        st.session_state.player_cards.append(deal_card())
        
        player_value = calculate_hand_value(st.session_state.player_cards)
        if player_value > 21:
            st.session_state.game_state = 'finished'
            st.session_state.result = 'ダブルダウンでバースト！負けです'
            st.session_state.losses += 1
            st.session_state.total_games += 1
            st.session_state.dealer_hidden = False
        else:
            stand()

def calculate_payout():
    """配当を計算"""
    payout = 0
    player_value = calculate_hand_value(st.session_state.player_cards)
    dealer_value = calculate_hand_value(st.session_state.dealer_cards)
    
    if st.session_state.blackjack_bonus and dealer_value != 21:
        payout = int(st.session_state.current_bet * 2.5)
        st.session_state.result = f'ブラックジャック！ボーナス配当 {payout} コイン獲得！'
    elif "勝ち" in st.session_state.result or "バースト" in st.session_state.result:
        payout = st.session_state.current_bet * 2
    elif "引き分け" in st.session_state.result:
        payout = st.session_state.current_bet
    
    st.session_state.coins += payout
    return payout

def hit():
    """プレイヤーがカードを引く"""
    st.session_state.player_cards.append(deal_card())
    player_value = calculate_hand_value(st.session_state.player_cards)
    
    if player_value > 21:
        st.session_state.game_state = 'finished'
        st.session_state.result = 'バースト！負けです'
        st.session_state.losses += 1
        st.session_state.total_games += 1
        st.session_state.dealer_hidden = False

def stand():
    """プレイヤーがスタンド"""
    st.session_state.dealer_hidden = False
    
    while calculate_hand_value(st.session_state.dealer_cards) < 17:
        st.session_state.dealer_cards.append(deal_card())
    
    player_value = calculate_hand_value(st.session_state.player_cards)
    dealer_value = calculate_hand_value(st.session_state.dealer_cards)
    
    st.session_state.game_state = 'finished'
    
    if dealer_value > 21:
        st.session_state.result = 'ディーラーがバースト！あなたの勝ちです'
        st.session_state.wins += 1
    elif player_value > dealer_value:
        st.session_state.result = 'あなたの勝ちです！'
        st.session_state.wins += 1
    elif player_value < dealer_value:
        st.session_state.result = 'ディーラーの勝ちです'
        st.session_state.losses += 1
    else:
        st.session_state.result = '引き分けです'
        st.session_state.draws += 1
    
    st.session_state.total_games += 1
    calculate_payout()

def reset_game():
    """ゲーム全体をリセット"""
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.draws = 0
    st.session_state.total_games = 0
    st.session_state.coins = 100
    st.session_state.current_bet = 0
    st.session_state.game_state = 'start'
    st.session_state.is_doubled_down = False
    st.session_state.blackjack_bonus = False

# タイトル
st.title("🃏 Blackjack Game!")

# コイン表示
st.markdown(f"### 💰 現在のコイン: **{st.session_state.coins}** 枚")
if st.session_state.game_state in ['playing', 'finished'] and st.session_state.current_bet > 0:
    st.markdown(f"**現在のベット**: {st.session_state.current_bet} 枚")

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
    
    st.divider()

# ゲーム開始画面
if st.session_state.game_state == 'start':
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎮 ゲーム開始", type="primary", use_container_width=True):
            start_new_game()
            st.rerun()
    with col2:
        if st.button("🔄 ゲームリセット", use_container_width=True):
            reset_game()
            st.rerun()

# ベット画面
elif st.session_state.game_state == 'betting':
    st.markdown("### 💰 ベット額を選択してください")
    
    bet_options = [5, 10, 25, 50]
    cols = st.columns(len(bet_options))
    
    for i, bet in enumerate(bet_options):
        with cols[i]:
            if st.session_state.coins >= bet:
                if st.button(f"{bet} 枚", key=f"bet_{bet}", use_container_width=True):
                    place_bet(bet)
                    st.rerun()
            else:
                st.button(f"{bet} 枚", key=f"bet_{bet}", disabled=True, use_container_width=True)
    
    st.markdown("**カスタムベット:**")
    custom_bet = st.number_input("ベット額", min_value=1, max_value=st.session_state.coins, value=1, step=1)
    if st.button("ベット", type="secondary", use_container_width=True):
        place_bet(custom_bet)
        st.rerun()
    
    if st.button("← 戻る", use_container_width=True):
        st.session_state.game_state = 'start'
        st.rerun()

# ゲーム中
elif st.session_state.game_state == 'playing':
    st.markdown("### 🎩 ディーラー")
    display_cards_animated(st.session_state.dealer_cards, "", hide_first=st.session_state.dealer_hidden)
    
    st.markdown("### 👤 あなた")
    player_total = display_cards_animated(st.session_state.player_cards, "")
    
    if player_total <= 21:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🎴 Hit", type="secondary", use_container_width=True):
                hit()
                st.rerun()
        with col2:
            if st.button("✋ Stand", type="primary", use_container_width=True):
                stand()
                st.rerun()
        with col3:
            can_double = (len(st.session_state.player_cards) == 2 and 
                         st.session_state.coins >= st.session_state.current_bet)
            if can_double:
                if st.button("💰 Double", use_container_width=True):
                    double_down()
                    st.rerun()
            else:
                st.button("💰 Double", disabled=True, use_container_width=True)

# ゲーム終了
elif st.session_state.game_state == 'finished':
    st.markdown("### 🎩 ディーラー")
    display_cards_animated(st.session_state.dealer_cards, "")
    
    st.markdown("### 👤 あなた")
    display_cards_animated(st.session_state.player_cards, "")
    
    st.divider()
    
    # 勝敗の演出を表示
    if "ブラックジャック" in st.session_state.result:
        show_result_animation('blackjack')
        st.success(f"🎉 {st.session_state.result}")
    elif "勝ち" in st.session_state.result:
        show_result_animation('win')
        st.success(f"🎉 {st.session_state.result}")
    elif "負け" in st.session_state.result or "バースト" in st.session_state.result:
        show_result_animation('loss')
        st.error(f"😔 {st.session_state.result}")
    else:
        st.info(f"🤝 {st.session_state.result}")
    
    if st.session_state.coins <= 0:
        st.error("💸 コインがなくなりました！ゲームをリセットしてください。")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.coins > 0:
            if st.button("🎮 新しいゲーム", type="primary", use_container_width=True):
                start_new_game()
                st.rerun()
        else:
            st.button("🎮 新しいゲーム", disabled=True, use_container_width=True)
    with col2:
        if st.button("🔄 ゲームリセット", use_container_width=True):
            reset_game()
            st.rerun()

st.markdown("---")
st.markdown("*💡 ヒント: ディーラーは17以上になるまでカードを引きます*")