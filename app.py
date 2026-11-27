import json
import streamlit as st

from repoready.scanner import scan_repository
from repoready.scorer import calculate_health_score
from repoready.reporter import (
    export_json_report,
    export_markdown_report,
)
st.set_page_config(
    page_title="RepoReady Dashboard",
    page_icon="🚀",
    layout="wide"
)
st.markdown("""
<style>
    .stApp {
        background-color: #0B1120;
        color: #F1F5F9;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    h1, h2, h3 {
        color: #F8FAFC;
    }

    div[data-testid="stMetric"] {
        background-color: #172554;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #2563EB;
    }
</style>
""", unsafe_allow_html=True)
st.title("🚀 RepoReady")
st.subheader("Open Source Repository Health Dashboard")

st.write(
    "Analyze your repository and discover how ready it is for contributors."
)

st.sidebar.title("🚀 RepoReady")
st.sidebar.caption("Repository Health Checker")

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "About RepoReady", "How to Use"]
)
if page == "About RepoReady":
    st.title("ℹ️ About RepoReady")

    st.markdown("""
    ### What is RepoReady?

    RepoReady is an open-source repository health checker
    designed to evaluate how ready a project is for contributors.

    ### Key Features

    - 🔍 Repository file scanning
    - 📊 Automated health scoring
    - 📁 Repository structure analysis
    - 📥 JSON and Markdown report downloads
    - 💡 Improvement recommendations

    ### Technology Stack

    - Python
    - Streamlit
    - Rich
    - Pytest

    ### Our Mission

    To help developers build cleaner, healthier and
    contributor-friendly open-source repositories.
    """)

    st.info("Built to make open-source contributions easier!")
    st.subheader("🌐 Project Links")

    st.markdown(
    "[⭐ View RepoReady on GitHub](https://github.com/trishahingu/RepoReady)"
)

    st.caption("Open-source project | Built with Python and Streamlit")
    st.stop()
st.divider()
if page == "Dashboard":
    repo_path = st.text_input(
    "📁 Enter your repository path",
    placeholder=r"C:\Users\TRISHA\Documents\RepoReady"
)
if page == "How to Use":
    st.title("📖 How to Use RepoReady")

    st.write(
        "Follow these simple steps to analyze your open-source repository."
    )

    st.subheader("Step 1: Enter Repository Path")
    st.write("Enter the full local path of the repository you want to analyze.")

    st.code(
        r"C:\Users\TRISHA\Documents\RepoReady",
        language="text"
    )

    st.subheader("Step 2: Analyze Repository")
    st.write("Click the Analyze Repository button to start scanning.")

    st.subheader("Step 3: Review Health Score")
    st.write("View your repository health score, files found and missing.")

    st.subheader("Step 4: Check Repository Analysis")
    st.write("Review the status of every required file and folder.")

    st.subheader("Step 5: Download Reports")
    st.write("Download your analysis in JSON or Markdown format.")

    st.subheader("Step 6: Follow Recommendations")
    st.write("Use the improvement recommendations to make your repository contributor-friendly.")

    st.success("You're ready to use RepoReady! 🚀")

    st.stop()
if st.button("🔍 Analyze Repository", type="primary"):

    if not repo_path.strip():
        st.warning("Please enter a repository path.")

    else:
        try:
            results = scan_repository(repo_path)
            health = calculate_health_score(results)

            st.success("Repository analysis completed!")
            st.subheader("📊 Repository Health Overview")
            st.progress(health["score"])
            col1, col2, col3 = st.columns(3)

            col1.metric("Health Score", f"{health['score']}%")
            col2.metric("Files Found", health["found"])
            col3.metric("Files Missing", health["missing"])
            st.subheader("📈 File Status Summary")

            chart_data = {
                "Status": ["Found", "Missing"],
                "Count": [health["found"], health["missing"]]
            }
            col1, col2 = st.columns(2)

            with col1:
                st.metric("✅ Successful Checks", health["found"])

            with col2:
                st.metric("⚠️ Missing Checks", health["missing"])

            if health["missing"] == 0:
                st.success("All repository checks passed!")
            st.subheader("Repository Analysis")

            st.dataframe(
                [
                    {
                        "File / Folder": name,
                        "Description": item["description"],
                        "Status": item["status"]
                    }
                    for name, item in results.items()
                ],
                use_container_width=True
            )

            st.info(f"Repository Grade: {health['grade']}")



            st.subheader("📥 Download Repository Report")

            

            json_report = {
                "health": health,
                "checks": results
            }

            markdown_report = f"""# RepoReady Analysis Report

            ## Repository Health

            - Score: {health['score']}%
            - Grade: {health['grade']}
            - Files Found: {health['found']}
            - Files Missing: {health['missing']}

            ## File Checks

            """ + "\n".join(
                f"- **{name}**: {item['status']} — {item['description']}"
                for name, item in results.items()
            )

            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    "📄 Download JSON Report",
                    data=json.dumps(json_report, indent=4),
                    file_name="repoready_report.json",
                    mime="application/json"
                )

            with col2:
                st.download_button(
                    "📝 Download Markdown Report",
                    data=markdown_report,
                    file_name="repoready_report.md",
                    mime="text/markdown"
                )

            

            st.subheader("💡 Improvement Recommendations")

            missing_items = [
                name for name, item in results.items()
                if not item["exists"]
            ]

            if missing_items:
                st.warning("Your repository needs some improvements:")

                for item in missing_items:
                    st.write(f"⚠️ Add or create: `{item}`")
            else:
                st.success("🎉 Great job! Your repository meets all current checks.")

            
        except (FileNotFoundError, NotADirectoryError, OSError) as error:
            st.error(str(error))
