import streamlit as st

# ページ設定（スマホでも見やすく）
st.set_page_config(page_title="プロテイン・コンシェルジュ", layout="centered")

# --- ヘッダーエリア ---
st.title("💪 Protein Prompt Generator")
st.caption("あなたの今の状態に最適な「食事提案プロンプト」を作成するツールです。")
st.divider()

# --- サイドバー：基本設定 ---
with st.sidebar:
    st.header("👤 プロフィール設定")
    # 体重入力
    weight = st.number_input("体重 (kg)", min_value=30, max_value=150, value=60, step=1)
    
    # 活動強度の選択
    st.subheader("活動レベル")
    activity_options = {
        "低": {"icon": "💻", "desc": "デスクワーク・運動不足", "factor": 1.2},
        "中": {"icon": "🏃‍♂️", "desc": "立ち仕事・週1〜2回の運動", "factor": 1.5},
        "高": {"icon": "🏋️‍♀️", "desc": "ハードな筋トレ・肉体労働", "factor": 2.0},
    }
    
    selected_activity = st.radio(
        "普段の活動量は？",
        options=list(activity_options.keys()),
        format_func=lambda x: f"{activity_options[x]['icon']} {x} : {activity_options[x]['desc']}"
    )

    # 目標値の計算と表示
    factor = activity_options[selected_activity]["factor"]
    daily_target = weight * factor
    meal_target = daily_target / 3
    
    st.info(f"📊 1食の目安: **{meal_target:.1f}g**")
    st.caption(f"1日トータル: {daily_target:.1f}g")

# --- メインエリア：状況入力 ---
st.header("🍽️ 今の気分・状況は？")

col1, col2 = st.columns(2)

with col1:
    timing = st.selectbox("いつ食べますか？", ["朝食", "昼食", "夕食", "間食/夜食"])
    location = st.selectbox("どこで調達しますか？", ["コンビニ（セブン/ローソン/ファミマ）", "外食チェーン", "自炊（スーパー/冷蔵庫）"])

with col2:
    mood = st.radio(
        "今の気分を選んでください",
        ["⚡️ クイック（5分で）", "🌿 さっぱり（胃に優しく）", "🍖 ガッツリ（肉食！）"]
    )

# --- プロンプト生成ロジック ---
mood_instruction = ""
if "クイック" in mood:
    mood_instruction = "調理時間や待ち時間を極限まで短くしてください。ワンハンドで食べられるものや、レンジ調理のみのものを優先してください。"
elif "さっぱり" in mood:
    mood_instruction = "脂質を抑え、胃腸への負担が少ないメニューにしてください。揚げ物は除外。薬味や酸味を活用した提案をお願いします。"
elif "ガッツリ" in mood:
    mood_instruction = "「食べた！」という満足感を最優先してください。肉や丼もの中心で、しかしタンパク質目標は必ずクリアする組み合わせにしてください。"

prompt_text = f"""
あなたはプロのパーソナルトレーナー兼管理栄養士です。
以下の私の状況に合わせて、最適な「高タンパク質メニュー」を1つだけ提案してください。

【ユーザーデータ】
- 現在の体重: {weight}kg
- 活動レベル: {selected_activity}
- **今回の摂取目標: タンパク質 約{meal_target:.1f}g**

【現在の状況】
- タイミング: {timing}
- 調達場所: {location}
- **気分・モード: {mood}**

【重要：選定基準】
1. {mood_instruction}
2. 指定された場所（{location}）で、今すぐ入手・実行可能な現実的なメニューにしてください。
3. 単品で目標（{meal_target:.1f}g）に届かない場合は、相性の良いサイドメニュー（卵、乳製品、サラダチキン等）を組み合わせて達成させてください。

【出力形式】
提案メニュー：[メニュー名]
--------------------------------
■ 組み合わせ内容
1. [メイン商品/食材] (約xx g)
2. [サブ商品/食材] (約xx g)
--------------------------------
合計タンパク質: 約 XX g / カロリー: 約 XX kcal

■ {mood}ポイント
[なぜこのメニューが今の気分に最適なのかを一言で]
"""

# --- 出力エリア ---
st.divider()
st.subheader("🤖 生成されたプロンプト")
st.markdown("右上のコピーボタンでコピーして、ChatGPTやGeminiに貼り付けてください。")

# コードブロックとして表示（コピーボタンが自動で付きます）
st.code(prompt_text, language="text")

# 補足情報
st.markdown(f"""
<small>※ 現在の設定（体重{weight}kg / {selected_activity}）に基づき、
1食あたり <b>{meal_target:.1f}g</b> のタンパク質確保を目指す指示になっています。</small>
""", unsafe_allow_html=True)