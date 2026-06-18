import streamlit as st
from backend.recommendation import recommend


def run():
    st.header("Cloud Recommendation")
    st.write("Complete the form below and receive the recommended cloud platform with scores and confidence.")

    with st.form("recommend_form"):
        user_name = st.text_input("User Name")
        budget = st.number_input("Budget (USD)", min_value=100.0, max_value=100000.0, value=1200.0, step=100.0)
        storage = st.selectbox("Storage", ["HDD", "SSD", "NVMe"])
        compute_requirement = st.selectbox("Compute Requirement", ["Light", "Standard", "Heavy"])
        security_requirement = st.selectbox("Security Requirement", ["Standard", "High", "Critical"])
        aiml_requirement = st.selectbox("AI/ML Requirement", ["None", "Basic", "Advanced"])
        business_type = st.selectbox(
            "Business Type",
            ["Small", "Startup", "Enterprise", "Analytics", "SaaS" ,"Government"],
        )
        submit = st.form_submit_button("Submit Recommendation")

    if submit:
        if not user_name.strip():
            st.error("Please enter a User Name before submitting.")
            return

        result = recommend(
            user_name=user_name,
            budget=budget,
            storage=storage,
            compute_requirement=compute_requirement,
            security_requirement=security_requirement,
            aiml_requirement=aiml_requirement,
            business_type=business_type,
        )

        st.success(f"Recommended platform: {result.get('predicted_platform', 'Unknown')}")

        score_col, confidence_col = st.columns([2, 1])
        with score_col:
            st.subheader("Provider Scores")
            st.write(f"AWS: {result.get('aws_score', 0.0)}")
            st.write(f"Google Cloud: {result.get('gcp_score', 0.0)}")
            st.write(f"ESDS: {result.get('esds_score', 0.0)}")

        with confidence_col:
            st.subheader("Confidence")
            st.metric("Confidence score", f"{result.get('confidence_score', 0.0):.2f}")

        st.markdown("---")
        st.subheader("Explanation")
        st.write(result.get("explanation", "No explanation available."))
        st.markdown("---")
        st.subheader("Recommendation saved")
        st.write(f"Recommendation saved for **{result.get('user_name')}**.")
