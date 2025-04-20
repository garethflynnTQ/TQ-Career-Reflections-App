
import streamlit as st
import os

# App setup
st.set_page_config(page_title="TQ Career Drivers", layout="wide")

# Load custom CSS (with fallback)
css_path = "tq_brand_styles.css"
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

TQ_BLUE = "#244092"
TQ_ORANGE = "#f03c24"
CARD_STYLE = f"""
    background-color: white;
    border: 2px solid {TQ_ORANGE};
    border-radius: 16px;
    padding: 16px;
    margin: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    color: {TQ_BLUE};
    text-align: center;
    height: 160px;
    display: flex;
    flex-direction: column;
    justify-content: center;
"""

# Define categories (shorter set for example, full set should be used in practice)
categories = {
    "Growth": [
        ("🌱 Personal Growth", "Maturity and mindset shift", True),
        ("🧠 Learning", "Love of exploring new ideas", True),
        ("🧗 Challenge", "Pushed to achieve more", True),
    ],
    "Freedom": [
        ("🎨 Creative Expression", "Freedom to create", True),
        ("🧭 Autonomy", "Work your own way", True),
        ("❤️ Passion", "Excited by your work", True),
    ]
}

if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.selections = {}
    st.session_state.final_picks = []
    st.session_state.top3 = []
    st.session_state.remaining = []
    st.session_state.final5 = []
    st.session_state.scores = {}

# Step 1: Pick 2 from each category using card visuals
if st.session_state.step == 1:
    st.title("TQ Career Drivers (v3.6)")
    st.markdown("### Step 1: Pick your top 2 cards from each category")

    valid = True
    all_selected = []

    for cat, cards in categories.items():
        st.subheader(cat)
        selected = []
        cols = st.columns(len(cards))
        for i, (title, desc, is_adapt) in enumerate(cards):
            with cols[i]:
                if st.checkbox(title, key=f"{cat}_{title}"):
                    selected.append(title)
                st.markdown(f"<div style='{CARD_STYLE}'><strong>{title}</strong><br><span style='font-size:12px'>{desc}</span></div>", unsafe_allow_html=True)
        if len(selected) != 2:
            valid = False
        st.session_state.selections[cat] = selected
        all_selected.extend(selected)

    if valid and st.button("Continue"):
        st.session_state.final_picks = all_selected
        st.session_state.remaining = all_selected.copy()
        st.session_state.step = 2
        st.experimental_rerun()

# Step 2: Select Top 3
elif st.session_state.step == 2:
    st.markdown("### Step 2: Select your Top 3 Drivers")
    top3 = st.multiselect("Your Top 3 Drivers", st.session_state.final_picks, max_selections=3)
    if len(top3) == 3:
        st.session_state.top3 = top3
        st.session_state.remaining = [d for d in st.session_state.final_picks if d not in top3]
        st.session_state.step = 3
        st.experimental_rerun()

# Step 3: One-by-one challenge with visible Top 3 cards
elif st.session_state.step == 3:
    st.markdown("### Step 3: Challenge Your Top 3")
    st.markdown("#### Your Current Top 3 Drivers:")
    cols = st.columns(3)
    for i, driver in enumerate(st.session_state.top3):
        with cols[i]:
            st.markdown(f"<div style='{CARD_STYLE}'><strong>{driver}</strong></div>", unsafe_allow_html=True)

    if st.session_state.remaining:
        card = st.session_state.remaining.pop(0)
        st.markdown(f"#### Would you replace one of your Top 3 with:")
        st.markdown(f"<div style='{CARD_STYLE}'><strong>{card}</strong></div>", unsafe_allow_html=True)
        if st.radio("Decision", ["No", "Yes"], key=f"replace_{card}") == "Yes":
            to_replace = st.selectbox("Which one to replace?", st.session_state.top3, key=f"swap_{card}")
            if to_replace:
                st.session_state.top3.remove(to_replace)
                st.session_state.top3.append(card)
        st.button("Next", on_click=st.experimental_rerun)
    else:
        st.session_state.step = 4
        st.experimental_rerun()

# Step 4: Add final 2
elif st.session_state.step == 4:
    st.markdown("### Step 4: Add 2 more drivers to complete your Top 5")
    extras = st.multiselect("Pick 2 additional drivers", [x for x in st.session_state.final_picks if x not in st.session_state.top3], max_selections=2)
    if len(extras) == 2:
        st.session_state.final5 = st.session_state.top3 + extras
        st.session_state.step = 5
        st.experimental_rerun()

# Step 5: Scoring
elif st.session_state.step == 5:
    st.markdown("### Step 5: Score how well your work environment supports these")
    for driver in st.session_state.final5:
        st.session_state.scores[driver] = st.slider(driver, 0, 10, 5)

    st.markdown("---")
    st.subheader("📋 Your Final Top 5 and Scores")
    for d in st.session_state.final5:
        st.write(f"- {d}: {st.session_state.scores[d]}/10")

    # Adaptability summary
    adaptability_cards = [c[0] for cards in categories.values() for c in cards if c[2]]
    count = len([d for d in st.session_state.final5 if d in adaptability_cards])
    if count >= 4:
        st.success("💪 Strong adaptability traits – you thrive in change, learning, and exploration.")
    elif count >= 2:
        st.info("🧠 Moderate adaptability – you show openness to variety and learning.")
    else:
        st.warning("😐 Lower adaptability signals – consider how you respond to uncertainty or growth.")
