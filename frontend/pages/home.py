import streamlit as st


def run():
    st.title("AI-Based Multi-Cloud Platform Recommendation System")
    st.write(
        "This platform uses AI to recommend the ideal cloud provider for your workload, budget, storage, compute, security, "
        "AI/ML, and business requirements. Explore provider strengths and use cases next."
    )

    st.markdown("---")

    aws_description = (
        "AWS is a comprehensive cloud platform with a broad service portfolio, global reach, "
        "and enterprise-ready security and governance capabilities."
    )
    gcp_description = (
        "Google Cloud offers strong data analytics and AI/ML tools, high-performance networking, "
        "and a pricing model tailored for cloud-native innovation."
    )
    esds_description = (
        "ESDS provides cost-effective cloud solutions for small and medium enterprises, "
        "with strong local support, compliance focus, and entry-level cloud adoption."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("AWS")
        st.write(aws_description)
        st.markdown("**Strengths:**")
        st.write("- Broad global infrastructure")
        st.write("- Enterprise-grade security and compliance")
        st.write("- Extensive service catalog for compute, storage, AI, and analytics")
        st.markdown("**Use Cases:**")
        st.write("- Large enterprise applications")
        st.write("- Mission-critical workloads")
        st.write("- Hybrid and multi-cloud deployments")

    with col2:
        st.subheader("Google Cloud")
        st.write(gcp_description)
        st.markdown("**Strengths:**")
        st.write("- Best-in-class AI/ML and data analytics")
        st.write("- High-speed network and developer tooling")
        st.write("- Simplified cloud-native application delivery")
        st.markdown("**Use Cases:**")
        st.write("- Machine learning platforms")
        st.write("- Data-driven analytics")
        st.write("- Cloud-native microservices")

    with col3:
        st.subheader("ESDS")
        st.write(esds_description)
        st.markdown("**Strengths:**")
        st.write("- Cost-effective cloud offerings")
        st.write("- Strong local and compliance support")
        st.write("- Easy onboarding for small businesses")
        st.markdown("**Use Cases:**")
        st.write("- Small and medium enterprise hosting")
        st.write("- Entry-level cloud migration")
        st.write("- Budget-sensitive applications")
