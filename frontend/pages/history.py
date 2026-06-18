import streamlit as st
from backend.recommendation import get_recommendation_history


def run():
    st.header("Recommendation History")
    st.write("Read past cloud recommendations from the backend database and filter by user or platform.")

    history_result = get_recommendation_history()
    history_records = history_result.get("history", [])

    if not history_records:
        st.info("No recommendation history found yet. Submit a new request on the Recommend page.")
        return

    search_query = st.text_input("Search by user or recommended platform", value="")

    rows = []
    for record in history_records:
        rows.append(
            {
                "User": record.get("user_name", ""),
                "AWS Score": record.get("aws_score", 0.0),
                "Google Cloud Score": record.get("gcp_score", 0.0),
                "ESDS Score": record.get("esds_score", 0.0),
                "Recommended Platform": record.get("recommended_platform", ""),
                "Date": record.get("created_at", ""),
            }
        )

    if search_query:
        query = search_query.strip().lower()
        rows = [
            row
            for row in rows
            if query in str(row["User"]).lower() or query in str(row["Recommended Platform"]).lower()
        ]

    if not rows:
        st.warning("No history records match your search.")
        return

    st.dataframe(rows, use_container_width=True)
