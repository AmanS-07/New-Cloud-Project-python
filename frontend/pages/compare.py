import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def run():
    st.header("Cloud Provider Comparison")
    st.write("Compare AWS, Google Cloud, and ESDS across cost, security, storage, performance, scalability, and AI/ML support.")

    providers = ["AWS", "Google Cloud", "ESDS"]
    metrics = ["Cost", "Security", "Storage", "Performance", "Scalability", "AI/ML Support"]
    scores = {
        "AWS": [3, 5, 5, 5, 5, 5],
        "Google Cloud": [4, 4, 4, 5, 5, 5],
        "ESDS": [5, 3, 4, 3, 4, 2],
    }

    comparison_rows = []
    for provider in providers:
        row = {"Provider": provider}
        row.update({metric: scores[provider][idx] for idx, metric in enumerate(metrics)})
        comparison_rows.append(row)

    st.subheader("Comparison table")
    st.dataframe(comparison_rows, use_container_width=True)

    st.markdown("---")
    st.subheader("Visual comparison")

    x = np.arange(len(metrics))
    width = 0.2

    fig, ax = plt.subplots(figsize=(10, 5))
    for index, provider in enumerate(providers):
        provider_scores = scores[provider]
        ax.bar(x + index * width, provider_scores, width, label=provider)

    ax.set_xticks(x + width)
    ax.set_xticklabels(metrics, rotation=30, ha="right")
    ax.set_ylim(0, 6)
    ax.set_ylabel("Rating (1-5)")
    ax.set_title("Cloud provider comparison by metric")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    st.pyplot(fig)
