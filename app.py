"""
Khasi Companion - Text MVP Application
Streamlit interface featuring:
  1. Translate (English <-> Khasi with verification badges and emergency safety guards)
  2. Explore Meghalaya (Zero-hallucination Tourism Knowledge Base)
  3. Learn Khasi (Curated vocabulary, phrases, and cultural concepts)
"""

import streamlit as st
import json
from pathlib import Path
from src.retrieval import TourismKnowledgeRetriever
from src.translation import TranslationService

st.set_page_config(
    page_title="Khasi Companion — Meghalaya AI Assistant",
    page_icon="🌿",
    layout="wide"
)

# Initialize services
@st.cache_resource
def get_retriever():
    return TourismKnowledgeRetriever()

@st.cache_resource
def get_translator():
    return TranslationService()

retriever = get_retriever()
translator = get_translator()

# Sidebar Navigation
st.sidebar.title("🌿 Khasi Companion")
st.sidebar.caption("AI-Powered Meghalaya Tourist & Language Assistant")

mode = st.sidebar.radio(
    "Choose Mode:",
    ["🔤 Translate (English ↔ Khasi)", "🗺️ Explore Meghalaya (Verified Facts)", "📖 Learn Khasi (Phrasebook & Culture)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛡️ Safety & Project Rules")
st.sidebar.info(
    "• **Zero-Hallucination Policy**: We never invent travel facts, opening hours, or ticket rates.\n\n"
    "• **Verification Labels**: Unverified translations are explicitly marked.\n\n"
    "• **Emergency Help**: Dial **112** (Pan-India) for urgent medical/police needs."
)

# -----------------------------------------------------------------------------
# MODE 1: Translate
# -----------------------------------------------------------------------------
if mode == "🔤 Translate (English ↔ Khasi)":
    st.title("🔤 English ↔ Khasi Translation")
    st.write("Reliable, verified communication for travelers and residents in Meghalaya.")

    col1, col2 = st.columns([1, 1])

    with col1:
        direction = st.selectbox("Direction", ["English to Khasi", "Khasi to English"])
        source_lang = "en" if direction == "English to Khasi" else "kha"
        target_lang = "kha" if direction == "English to Khasi" else "en"

        sample_options = [
            "Select a sample phrase...",
            "Hello / Greetings",
            "Thank you very much",
            "How are you?",
            "Please speak slowly.",
            "How much is the fare to Shillong?",
            "I need a doctor / medical help immediately."
        ]
        chosen_sample = st.selectbox("Quick Sample Phrases:", sample_options)
        default_val = chosen_sample if chosen_sample != "Select a sample phrase..." else ""

        user_input = st.text_area("Enter Text:", value=default_val, height=120, placeholder="Type your phrase or sentence here...")
        translate_btn = st.button("Translate", type="primary")

    with col2:
        st.subheader("Translation Result")
        if user_input:
            result = translator.translate(user_input, source_lang=source_lang, target_lang=target_lang)

            if result.get("safety_critical"):
                st.error(
                    "🚨 **SAFETY-CRITICAL EMERGENCY ALERT**\n\n"
                    "Medical, police, or safety requests must **never** rely solely on automated translation.\n\n"
                    "👉 **Call 112 (Pan-India Emergency)** immediately or seek human assistance."
                )

            status = result["verification_status"]
            if status == "verified_native_speaker":
                badge_type = "success"
                badge_label = "Verified by Fluent Native Speaker"
            elif status == "verified_official":
                badge_type = "success"
                badge_label = "Verified Official Source"
            elif status == "needs_review":
                badge_type = "warning"
                badge_label = "Needs Review by Speaker"
            else:
                badge_type = "info"
                badge_label = "Unverified (Not Fabricated)"

            st.caption(f"Verification Status: **{badge_label}**")

            if result["translation"]:
                st.markdown(f"### {result['translation']}")
                if result.get("pronunciation"):
                    st.write(f"🗣️ *Pronunciation*: `{result['pronunciation']}`")
            else:
                st.warning(result.get("message", "Translation withheld per verification policy."))

            if result.get("notes"):
                st.info(f"ℹ️ **Linguistic Note**: {result['notes']}")
        else:
            st.write("Enter text on the left to view verified translations.")

# -----------------------------------------------------------------------------
# MODE 2: Explore Meghalaya (System B Tourism Knowledge Base)
# -----------------------------------------------------------------------------
elif mode == "🗺️ Explore Meghalaya (Verified Facts)":
    st.title("🗺️ Explore Meghalaya (Verified Knowledge Base)")
    st.write(
        "Factual, audited tourism intelligence covering destinations, cultural etiquette, transport, and safety. "
        "Strictly powered by our **Zero-Hallucination Knowledge Base** (System B)."
    )

    categories = ["All Categories"] + retriever.get_categories()
    col_cat, col_search = st.columns([1, 2])
    with col_cat:
        selected_cat = st.selectbox("Category Filter:", categories)
    with col_search:
        search_query = st.text_input("Search (e.g., Nohkalikai, Sacred Grove, 112, Taxi):", placeholder="Type destination or question...")

    cat_arg = None if selected_cat == "All Categories" else selected_cat
    matches = retriever.search(search_query, category=cat_arg)

    if search_query and not matches:
        st.warning(retriever.format_safe_answer(search_query))
    else:
        st.write(f"Showing **{len(matches)}** verified record(s):")
        for rec in matches:
            with st.expander(f"📍 {rec['title']} ({rec.get('location', 'Meghalaya')})", expanded=True):
                st.write(rec.get("content", {}).get("en", ""))

                cols = st.columns(2)
                with cols[0]:
                    if rec.get("opening_hours"):
                        st.markdown(f"🕒 **Hours**: {rec['opening_hours']}")
                    if rec.get("price_info"):
                        st.markdown(f"💵 **Price / Fees**: {rec['price_info']}")
                with cols[1]:
                    if rec.get("safety_notes"):
                        st.markdown(f"⚠️ **Safety**: {rec['safety_notes']}")

                st.markdown("---")
                st.caption(
                    f"**Source**: [{rec.get('source_name', 'Official')}]({rec.get('source_url', '#')}) | "
                    f"**Reviewed**: `{rec.get('last_reviewed', '2026-10-15')}` | "
                    f"**Status**: `{rec.get('verification_status')}`"
                )

# -----------------------------------------------------------------------------
# MODE 3: Learn Khasi
# -----------------------------------------------------------------------------
elif mode == "📖 Learn Khasi (Phrasebook & Culture)":
    st.title("📖 Learn Khasi: Phrases & Culture")
    st.write("Basic conversational vocabulary and essential cultural insights for visitors.")

    tab1, tab2 = st.tabs(["🗣️ Essential Phrasebook", "🌿 Cultural Pillars & Proverbs"])

    with tab1:
        st.subheader("Everyday Conversational Phrases")
        with open("data/phrasebook.json", "r", encoding="utf-8") as f:
            phrase_data = json.load(f)

        for p in phrase_data:
            khasi_text = p.get("khasi") or "*[Translation pending review]*"
            pron = p.get("pronunciation_guide") or "-"
            status_tag = f"`{p.get('verification_status')}`"

            with st.container():
                st.markdown(f"**English**: {p.get('english')}")
                st.markdown(f"**Khasi**: {khasi_text} | *Pronunciation*: {pron} | Status: {status_tag}")
                if p.get("notes"):
                    st.caption(p.get("notes"))
                st.markdown("---")

    with tab2:
        st.subheader("Foundational Khasi Values (*Ki Nongrim*)")
        st.markdown("""
        * **Tip Kur, Tip Kha**: *Knowing maternal and paternal kin relations.* A cornerstone of Khasi matrilineal society and moral conduct.
        * **Kamai ïa ka Hok**: *Earn through righteousness.* The ancient Khasi duty to live with moral integrity and honesty.
        * **Tip Briew, Tip Blei**: *Knowing humanity and knowing God.* Serving fellow human beings with honor and humility.
        """)

        st.subheader("Traditional Khasi Proverbs (*Ki Ktien Tymmen*)")
        st.info("💡 *'Ka burom kaba khraw tam ka long ban kamai ïa ka hok.'* — The highest honor is to live with honesty.")
