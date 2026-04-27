import streamlit as st
from analyzer import analyze_review

# --- Page Config ---
st.set_page_config(
    page_title="Product Review Analyzer",
    page_icon="🔍",
    layout="centered"
)

# --- Title ---
st.title("🔍 Product Review Sentiment Analyzer")
st.markdown("Paste a customer review to extract sentiment, score, key points, and summary.")
st.divider()

# --- Test Cases ---
st.markdown("**Try a test case:**")

col1, col2, col3 = st.columns(3)

POSITIVE = "Absolutely love this laptop! The display is stunning, performance is blazing fast, and the keyboard feels amazing to type on. Battery lasts a full day easily. Best purchase I've made this year."
NEGATIVE = "Terrible experience. The product arrived broken, customer support was completely unhelpful, and the build quality is cheap plastic. Returned it immediately. Total waste of money."
MIXED = "The camera quality is outstanding and takes really sharp photos. However, the phone gets very hot during gaming and the charging speed is disappointingly slow for a 2024 device."

if col1.button("✅ Positive"):
    st.session_state.review_input = POSITIVE

if col2.button("❌ Negative"):
    st.session_state.review_input = NEGATIVE

if col3.button("⚖️ Mixed"):
    st.session_state.review_input = MIXED

# --- Input Area ---
review_text = st.text_area(
    label="Customer Review",
    placeholder="e.g. The phone looks good but battery drains quickly...",
    height=120,
    value=st.session_state.get("review_input", ""),
    key="review_input"
)

analyze_btn = st.button("Analyze Review", type="primary", use_container_width=True)

# --- Analysis + Output ---
if analyze_btn:
    if not review_text.strip():
        st.warning("Please enter a review before analyzing.")
    else:
        with st.spinner("Analyzing review..."):
            try:
                result = analyze_review(review_text)

                st.divider()
                st.markdown("### Results")

                # Row 1 — Sentiment + Score
                col_a, col_b = st.columns(2)

                with col_a:
                    sentiment = result["sentiment"]

                    color_map = {
                        "Positive": "green",
                        "Negative": "red",
                        "Mixed": "orange",
                        "Neutral": "gray"
                    }
                    color = color_map.get(sentiment, "gray")
                    st.markdown(f"**Sentiment**")
                    st.markdown(
                        f"<span style='background-color:{color};color:white;"
                        f"padding:4px 14px;border-radius:20px;font-size:14px'>"
                        f"{sentiment}</span>",
                        unsafe_allow_html=True
                    )

                with col_b:
                    st.metric(
                        label="Sentiment Score",
                        value=f"{result['sentiment_score']:.2f} / 1.00"
                    )

                st.divider()

                # Row 2 — Key Points
                st.markdown("**Key Points**")
                for point in result["key_points"]:
                    st.markdown(f"- {point}")

                st.divider()

                # Row 3 — Summary
                st.markdown("**Summary**")
                st.info(result["summary"])

            except ValueError as e:
                st.error(f"Input error: {e}")
            except KeyError as e:
                st.error(f"Unexpected response structure: {e}")
            except Exception as e:
                st.error(f"Something went wrong: {e}")