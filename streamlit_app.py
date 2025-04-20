
import streamlit as st
import random

st.set_page_config(page_title="TQ Career Drivers", layout="wide")

# Load custom CSS
with open("tq_brand_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

TQ_BLUE = "#244092"
TQ_ORANGE = "#f03c24"
CARD_STYLE = f"""
    background-color: white;
    border: 2px solid {TQ_ORANGE};
    border-radius: 16px;
    padding: 16px;
    margin: 10px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    color: {TQ_BLUE};
    text-align: center;
    height: 160px;
    display: flex;
    flex-direction: column;
    justify-content: center;
"""

# Define categories and cards (6 categories, with emoji, description, and adaptability flag)
categories = {
    "Growth, Challenge & Future Potential": [
        ("🌱 Personal Growth", "Maturity, confidence, and mindset shift", True),
        ("🛠️ New Skill Development", "Learning new hard or soft skills", True),
        ("👤 Professional Credibility", "Reputation in your field or industry", False),
        ("🧗 Stretch & Challenge", "Pushed to achieve beyond your comfort zone", True),
        ("🚪 Career Opportunities", "Clear path to future options", False),
        ("🏆 Career Progression", "Promotion or elevated recognition", False),
        ("🎖️ Achievement Milestones", "Momentum in achieving goals", False),
        ("🧠 Curiosity & Learning", "You love exploring new ideas", True),
        ("🧪 Innovation & Experimentation", "Trying new approaches and technologies", True),
    ],
    "Expression, Freedom & Creativity": [
        ("🎨 Creative Expression", "Freedom to create and ideate", True),
        ("🧭 Self-Directed Work", "Autonomy in how you deliver outcomes", True),
        ("🌍 Exploration & Variety", "Always something new to explore", True),
        ("❤️ Work That Excites You", "Genuinely passionate about what you do", True),
        ("🔥 Bold Decision-Making", "Space to take risks and experiment", True),
        ("🔄 Role Variety", "Mix of projects, people or tasks", True),
        ("🌠 Personal Aspirations", "Work aligned to personal ambitions", False),
        ("🦸 Empowered to Act", "Permission and confidence to act", True),
    ],
    "Connection, Belonging & Relationships": [
        ("🫶 Empathetic Culture", "Working with emotionally intelligent people", False),
        ("🏁 Healthy Competition", "Positively driven by others", False),
        ("🧑‍🤝‍🧑 Great Colleagues", "Enjoy working with the team around you", False),
        ("🚪 Inclusive Environment", "Safe and welcoming space", False),
        ("🤝 Trust & Safety", "Confidence in colleagues and culture", False),
        ("🧓 Mentorship & Guidance", "Learning from experienced people", False),
        ("🧘 Flexibility for Life", "Work fits into your life needs", True),
        ("🆘 Service to Others", "Helping people or creating social impact", False),
        ("🤝 Collaborative Culture", "Work is built with others, not alone", False),
    ],
    "Purpose, Performance & Impact": [
        ("🎯 Meaning & Purpose", "Doing work that feels important", False),
        ("🧑‍💼 Leading Others", "Inspiring and guiding people or projects", False),
        ("🧠 Solving Complex Problems", "Stretch thinking to resolve challenges", False),
        ("📈 Results Orientation", "Driven by success metrics or outcomes", False),
        ("🧾 Ownership & Responsibility", "You take accountability for results", False),
        ("📋 Role Clarity", "Clear expectations for your role", False),
        ("📚 Depth of Knowledge", "Valued for your expertise", False),
        ("📢 Influence & Voice", "Shaping decisions or ideas", False),
        ("🌍 Making a Difference", "Your work has positive real-world impact", False),
    ],
    "Reward, Recognition & Security": [
        ("🙌 Appreciation & Recognition", "Regular acknowledgment of your work", False),
        ("💰 Fair Compensation", "Equitably paid for your contribution", False),
        ("🎁 Lifestyle Benefits", "Perks that enhance your life", False),
        ("🏷️ Job Title", "Status or externally recognised title", False),
        ("🛡️ Job Security", "Feeling stable in role and income", False),
        ("🤗 Manager & Team Support", "Support from team and leaders", False),
        ("⚖️ Balance & Boundaries", "Time and space for life outside work", False),
        ("🪞 Sense of Worth", "Valued as a whole person", False),
    ],
    "Brand, Purpose & Identity": [
        ("🏢 Brand Affinity", "Aligned with a company brand you admire", True),
        ("🌟 Shared Vision", "Working toward a meaningful future direction", False),
        ("🏆 Reputation of Employer", "High-status or respected organisation", False),
        ("🤝 Cultural Fit", "Workplace aligned with your values", False),
        ("🎯 Sense of Mission", "Connected to a higher purpose", False),
        ("💼 Industry Alignment", "Field or domain that inspires you", False),
        ("✈️ Global Reach & Mobility", "Opportunities across geographies", True),
        ("📍 Work Environment & Location", "Location or setup that energises you", False),
        ("🌈 Inclusion & Belonging", "Genuine diversity and inclusion", False),
    ]
}

# Session state
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.selections = {}
    st.session_state.final_picks = []
    st.session_state.top3 = []
    st.session_state.remaining = []
    st.session_state.final5 = []
    st.session_state.scores = {}

# Step 1: Top 2 per category
if st.session_state.step == 1:
    st.title("TQ Career Drivers (v3.5)")
    st.markdown("### Step 1: Pick your top 2 cards from each category")
    all_selected = []
    valid = True
    for cat, cards in categories.items():
        st.subheader(cat)
        selected = st.multiselect(f"Pick 2 from {cat}", [c[0] for c in cards], max_selections=2, key=cat)
        if len(selected) != 2:
            valid = False
        st.session_state.selections[cat] = selected
        all_selected.extend(selected)

    if valid:
        if st.button("Continue"):
            st.session_state.final_picks = all_selected
            st.session_state.remaining = all_selected.copy()
            st.session_state.step = 2
            st.experimental_rerun()

# Step 2: Top 3
elif st.session_state.step == 2:
    st.markdown("### Step 2: From those 12, pick your Top 3 drivers")
    top3 = st.multiselect("Select your Top 3 Drivers", st.session_state.final_picks, max_selections=3)
    if len(top3) == 3:
        st.session_state.top3 = top3
        st.session_state.remaining = [x for x in st.session_state.final_picks if x not in top3]
        st.session_state.step = 3
        st.experimental_rerun()

# Step 3: One-by-one challenge
elif st.session_state.step == 3:
    st.markdown("### Step 3: Card Challenge")
    if st.session_state.remaining:
        card = st.session_state.remaining.pop(0)
        st.markdown(f"Would you replace one of your Top 3 with **{card}**?")
        replace = st.radio("Decision", ["No", "Yes"], key=f"replace_{card}")
        if replace == "Yes":
            to_replace = st.selectbox("Choose one to replace", st.session_state.top3, key=f"choose_{card}")
            if to_replace:
                st.session_state.top3.remove(to_replace)
                st.session_state.top3.append(card)
        st.button("Next", on_click=st.experimental_rerun)
    else:
        st.session_state.step = 4
        st.experimental_rerun()

# Step 4: Add 2 to make Top 5
elif st.session_state.step == 4:
    st.markdown("### Step 4: Add 2 more to make your Top 5")
    extras = st.multiselect("Pick 2 additional drivers", [x for x in st.session_state.final_picks if x not in st.session_state.top3], max_selections=2)
    if len(extras) == 2:
        st.session_state.final5 = st.session_state.top3 + extras
        st.session_state.step = 5
        st.experimental_rerun()

# Step 5: Score each
elif st.session_state.step == 5:
    st.markdown("### Step 5: Score your current work against your Top 5 Drivers")
    for driver in st.session_state.final5:
        st.session_state.scores[driver] = st.slider(driver, 0, 10, 5)

    st.markdown("---")
    st.subheader("Your Top 5 Drivers and Scores")
    for d in st.session_state.final5:
        st.markdown(f"- **{d}**: {st.session_state.scores[d]}/10")

    adaptability_cards = []
    for cat, cards in categories.items():
        adaptability_cards.extend([c[0] for c in cards if c[2]])

    count = len([x for x in st.session_state.final5 if x in adaptability_cards])
    if count >= 4:
        st.success("💪 Strong adaptability traits — you thrive in change, learning, and exploration.")
    elif count >= 2:
        st.info("🧠 Moderate adaptability — you show openness to variety and learning.")
    else:
        st.warning("😐 Lower adaptability signals — consider how you respond to uncertainty or growth.")
