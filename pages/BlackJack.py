import streamlit as st
import random

# セッション状態の初期化
if 'player_cards' not in st.session_state:
    st.session_state.player_cards = []
if 'dealer_cards' not in st.session_state:
    st.session_state.dealer_cards = []
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'start'  # start, betting, playing, finished
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
    rank = card[:-1]  # スートを除く
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11  # Aの値は後で調整
    else:
        return int(rank)

def calculate_hand_value(cards):
    """手札の合計値を計算（Aの処理込み）"""
    total = 0
    aces = 0
    
    for card in cards:
        value = card_value(card)
        if card[:-1] == 'A':
            aces += 1
        total += value
    
    # Aを1として数える必要があるかチェック
    while total > 21 and aces > 0:
        total -= 10  # A を 11 から 1 に変更
        aces -= 1
    
    return total

def deal_card():
    """カードを1枚配る"""
    deck = create_deck()
    return random.choice(deck)

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
    
    # ブラックジャック（21）のチェック
    if calculate_hand_value(st.session_state.player_cards) == 21:
        st.session_state.blackjack_bonus = True
        stand()

def double_down():
    """ダブルダウン"""
    if st.session_state.coins >= st.session_state.current_bet:
        st.session_state.coins -= st.session_state.current_bet
        st.session_state.current_bet *= 2
        st.session_state.is_doubled_down = True
        
        # カードを1枚だけ引いて強制的にスタンド
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
    
    # ブラックジャックボーナス（最初の2枚で21）
    if st.session_state.blackjack_bonus and dealer_value != 21:
        payout = int(st.session_state.current_bet * 2.5)  # 3:2の配当
        st.session_state.result = f'ブラックジャック！ボーナス配当 {payout} コイン獲得！'
    elif "勝ち" in st.session_state.result or "バースト" in st.session_state.result:
        payout = st.session_state.current_bet * 2  # 元本 + 賞金
    elif "引き分け" in st.session_state.result:
        payout = st.session_state.current_bet  # 元本のみ返却
    
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
    
    # ディーラーが17以上になるまでカードを引く
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
    
    # 配当計算
    payout = calculate_payout()

def reset_stats():
    """統計をリセット"""
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.draws = 0
    st.session_state.total_games = 0

def reset_game():
    """ゲーム全体をリセット（コインも含む）"""
    reset_stats()
    st.session_state.coins = 100
    st.session_state.current_bet = 0
    st.session_state.game_state = 'start'
    st.session_state.is_doubled_down = False
    st.session_state.blackjack_bonus = False

def display_cards(cards, title, hide_first=False):
    """カードを表示"""
    st.markdown(f"**{title}**")
    cards_display = []
    total = 0
    
    for i, card in enumerate(cards):
        if hide_first and i == 0:
            cards_display.append("🎴")
        else:
            cards_display.append(card)
            total += card_value(card)
    
    if hide_first and len(cards) > 1:
        # 2枚目以降の合計のみ表示
        visible_cards = cards[1:]
        total = calculate_hand_value(visible_cards)
        st.markdown(f"カード: {' '.join(cards_display)} (合計: {total} + ?)")
    else:
        total = calculate_hand_value(cards)
        st.markdown(f"カード: {' '.join(cards_display)} (合計: {total})")
    
    return total

# タイトル
st.title("🃏 Blackjack Game!")

# ルール説明
st.markdown("""
## 📋 ルール説明

1. **目標**: カードの合計を21に近づける（21を超えないように）
2. **カードの値**: 
   - 数字カード（2-10）: 額面通り
   - 絵札（J, Q, K）: 10点
   - A（エース）: 11点または1点（有利な方を自動選択）
3. **賭けシステム**:
   - 初期コイン: 100枚
   - ベット額を選んで勝負
   - ブラックジャック: 3:2配当（1.5倍）
   - 通常勝利: 2倍配当
   - 引き分け: 賭け金返却
4. **ゲームアクション**:
   - **Hit**: カードをもう1枚引く
   - **Stand**: カードを引かずに勝負
   - **Double Down**: 賭け金を2倍にして1枚だけ引く
5. **ゲームの流れ**:
   - ベット額を選択
   - プレイヤーとディーラーに2枚ずつ配られる
   - ディーラーの1枚目は裏向き
   - Hit/Stand/Double Downを選択
6. **勝敗**:
   - 21を超える = バースト（負け）
   - ディーラーは17以上になるまで必ずカードを引く
   - より21に近い方が勝ち
""")

st.divider()

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
    
    st.markdown(f"**総ゲーム数**: {st.session_state.total_games}")
    
    st.divider()

# ゲーム開始ボタン
if st.session_state.game_state == 'start':
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎮 ゲーム開始", type="primary"):
            start_new_game()
            st.rerun()
    with col2:
        if st.button("🔄 ゲームリセット"):
            reset_game()
            st.rerun()

# ベット画面
elif st.session_state.game_state == 'betting':
    st.markdown("### 💰 ベット額を選択してください")
    
    # ベット額選択ボタン
    bet_options = [5, 10, 25, 50]
    cols = st.columns(len(bet_options))
    
    for i, bet in enumerate(bet_options):
        with cols[i]:
            if st.session_state.coins >= bet:
                if st.button(f"{bet} 枚", key=f"bet_{bet}"):
                    place_bet(bet)
                    st.rerun()
            else:
                st.button(f"{bet} 枚", key=f"bet_{bet}", disabled=True)
    
    # カスタムベット
    st.markdown("**カスタムベット:**")
    custom_bet = st.number_input("ベット額", min_value=1, max_value=st.session_state.coins, value=1, step=1)
    if st.button("ベット", type="secondary"):
        place_bet(custom_bet)
        st.rerun()
    
    if st.button("← 戻る"):
        st.session_state.game_state = 'start'
        st.rerun()

# ゲーム中の表示
elif st.session_state.game_state == 'playing':
    # ディーラーのカード表示
    st.markdown("### 🎩 ディーラー")
    display_cards(st.session_state.dealer_cards, "", hide_first=st.session_state.dealer_hidden)
    
    st.markdown("### 👤 あなた")
    player_total = display_cards(st.session_state.player_cards, "")
    
    # プレイヤーのアクション
    if player_total <= 21:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🎴 Hit (カードを引く)", type="secondary"):
                hit()
                st.rerun()
        with col2:
            if st.button("✋ Stand (勝負)", type="primary"):
                stand()
                st.rerun()
        with col3:
            # ダブルダウンは最初の2枚の時のみ、かつコインが足りる場合のみ
            can_double = (len(st.session_state.player_cards) == 2 and 
                         st.session_state.coins >= st.session_state.current_bet)
            if can_double:
                if st.button("💰 Double Down", type="secondary"):
                    double_down()
                    st.rerun()
            else:
                st.button("💰 Double Down", disabled=True)

# ゲーム終了時の表示
elif st.session_state.game_state == 'finished':
    # 最終結果表示
    st.markdown("### 🎩 ディーラー")
    dealer_total = display_cards(st.session_state.dealer_cards, "")
    
    st.markdown("### 👤 あなた")
    player_total = display_cards(st.session_state.player_cards, "")
    
    # 結果表示
    st.divider()
    if "勝ち" in st.session_state.result or "ブラックジャック" in st.session_state.result:
        st.success(f"🎉 {st.session_state.result}")
    elif "負け" in st.session_state.result or "バースト" in st.session_state.result:
        st.error(f"😔 {st.session_state.result}")
    else:
        st.info(f"🤝 {st.session_state.result}")
    
    # コイン不足チェック
    if st.session_state.coins <= 0:
        st.error("💸 コインがなくなりました！ゲームをリセットしてください。")
    
    # 次のゲームボタン
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.coins > 0:
            if st.button("🎮 新しいゲーム", type="primary"):
                start_new_game()
                st.rerun()
        else:
            st.button("🎮 新しいゲーム", disabled=True)
    with col2:
        if st.button("🔄 ゲームリセット"):
            reset_game()
            st.rerun()

# フッター
st.markdown("---")
st.markdown("*💡 ヒント: Double Downは11の時が効果的！ブラックジャックなら1.5倍配当！*")