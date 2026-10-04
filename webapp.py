import streamlit as st
import os
import html
import requests
from google import genai
from dotenv import load_dotenv

# --- Safe Environment & API Configuration ---
current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, ".env")
load_dotenv(dotenv_path)

API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") 

# Bulletproof fallback: safely check for secrets without crashing the app
if not API_KEY:
    try:
        if "GEMINI_API_KEY" in st.secrets:
            API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass # Safely bypass if st.secrets doesn't exist
def check_github_saturation(title):
    """
    Queries the live GitHub API using title keywords,
    explicitly sorting results by star count to capture the top 10 most popular projects.
    """
    # Filter out short filler words to make the search query accurate
    query_keywords = [word for word in title.split() if len(word) > 2]
    keywords = "+".join(query_keywords) if query_keywords else title
    
    # Sort explicitly by stars in descending order to fetch the most popular matches
    url = f"https://api.github.com/search/repositories?q={keywords}&sort=stars&order=desc"
    
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
        
    try:
        res = requests.get(url, headers=headers, timeout=5).json()
        count = res.get("total_count", 0)
        items = res.get("items", [])[:10]  # ✨ UPDATED: Fetches the top 10 matches instead of 5
        return count, items
    except Exception:
        return 0, []

# --- Custom Premium CSS Styling Canvas ---
st.markdown("""
<style>
    /* 1. Force a subtle cool-gray canvas color across the main background viewport */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #F8FAFC !important;
    }

    /* Automatically adjust background colors cleanly if user runs native Dark Mode */
    @media (prefers-color-scheme: dark) {
        .stApp, [data-testid="stAppViewContainer"] {
            background-color: #0F172A !important;
        }
    }

    /* 2. Format global workspace grid constraints */
    .main .block-container {
        max-width: 1050px;
        padding-top: 4rem;
    }

    /* 3. Responsive Text Adaptive Cards */
    .custom-card {
        background-color: var(--background-color, #FFFFFF);
        border: 1px solid var(--border-color, #E2E8F0);
        border-radius: 12px;
        padding: 28px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
        color: var(--text-color, #0F172A);
    }

    /* 4. Style input fields for clean layout symmetry */
    .stTextInput input, .stTextArea textarea {
        border-radius: 8px !important;
        border: 1px solid #E2E8F0 !important;
    }

    /* 5. Executive Slate Action Control Button with clear transformation hover effects */
    div.stButton > button:first-child {
        background-color: #4F46E5 !important; /* Indigo accent color link */
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.7rem 1.5rem !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #4338CA !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.3) !important;
    }

    /* 6. Refined layout configuration for core numerical metrics */
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #4F46E5 !important;
    }

    button[data-baseweb="tab"] {
        font-size: 15px !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- UI Header Component ---
st.title(":material/token: ProjectPulse AI")
st.markdown("<p style='font-size: 15px; color: #64748B; margin-top: -10px; margin-bottom: 30px;'>A data-backed evaluation engine for modern software architecture.</p>", unsafe_allow_html=True)

# --- Left Sidebar Control Panel Config ---
st.sidebar.markdown("### :material/settings: Configuration Panel")
st.sidebar.write("Define your concept parameters below:")

p_title = st.sidebar.text_input("Project Title", placeholder="e.g., Smart Crop Disease Analyzer")
p_desc = st.sidebar.text_area("Brief Description", placeholder="Describe the core utility and user problem...", height=120)
p_tech = st.sidebar.text_input("Intended Tech Stack", placeholder="e.g., Python, Streamlit, PostgreSQL")

st.sidebar.write("")
submit_btn = st.sidebar.button("Run Validation Engine", use_container_width=True)

# --- Execution & Logic Presentation Canvas ---
if submit_btn:
    if not p_title or not p_desc:
        st.sidebar.error("⚠️ Title and Description are required parameters.")
    else:
        with st.spinner("Analyzing parameters against live data pipelines..."):
            # 1. Fetch live market popularity search arrays
            repo_count, sample_repos = check_github_saturation(p_title)
            
            # 2. Trigger generative validation engine framework
            if not API_KEY:
                st.error("The AI service is not configured right now. Please try again later.")
                st.stop()
            client = genai.Client(api_key=API_KEY)
            
            sample_text = "\n".join([f"- {r['name']} ({r['stargazers_count']} ★): {r['description']}" for r in sample_repos])
            prompt = f"Analyze this proposed project:\nTitle: {p_title}\nDescription: {p_desc}\nTech Stack: {p_tech}\nGitHub found {repo_count} similar repositories. Top samples:\n{sample_text}\nProvide a professional assessment covering:\n1. Market Saturation Verdict\n2. Feasibility & Tech Stack Score\n3. 3 Strategic Improvements/Feature Gaps."
            
            try:
                interaction = client.interactions.create(model="gemini-2.5-flash", input=prompt)
            except Exception:
                st.error("The AI analysis is temporarily unavailable. Please try again in a moment.")
                st.stop()
            
            # 3. Structural Header Card (Inverts styling automatically in Dark Mode)
            st.markdown(f"""
            <div class="custom-card">
                <h3 style="margin-top: 0px; font-weight: 600; color: inherit;">Evaluation Report: {html.escape(p_title)}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # 4. Metrics Dashboard Rows
            m1, m2 = st.columns(2)
            with m1:
                st.metric(label="GitHub Keyword Overlaps", value=f"{repo_count:,} Projects")
            with m2:
                status_label = "Open Niche" if repo_count < 10 else ("Moderate Volume" if repo_count < 50 else "High Density")
                st.metric(label="Market Density Profile", value=status_label)
            
            st.write("---")
            
            # 5. Tabbed Data Navigation (Monochrome Design Icons)
            tab1, tab2 = st.tabs([":material/analytics: Executive Analysis", ":material/folder_open: Market Context (GitHub)"])
            
            with tab1:
                st.markdown(interaction.output_text)
                st.write("")
                st.download_button(label="Export Report (.txt)", data=interaction.output_text, file_name=f"{p_title}_assessment.txt", use_container_width=True)
                
            with tab2:
                if sample_repos:
                    st.markdown("###  Top 10 Popular Alignments on GitHub")
                    st.write("These are the most highly-starred public projects that match your concept keywords:")
                    st.write("")
                    
                    # 💡 Wrap the 10 results in an elegant, scrollable dashboard container box
                    st.markdown('<div style="max-height: 550px; overflow-y: auto; padding-right: 10px;">', unsafe_allow_html=True)
                    
                    for index, repo in enumerate(sample_repos, 1):
                        # Premium custom card element for every popular repo match discovered
                        st.markdown(f"""
                        <div style="background-color: var(--background-color, #FFFFFF); border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; margin-bottom: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 16px; font-weight: 600;">
                                    <span style="color: #94A3B8; margin-right: 4px;">#{index}</span> 🌿 <a href="{html.escape(repo['html_url'])}" target="_blank" style="color: #4F46E5; text-decoration: none;">{html.escape(repo['name'])}</a>
                                </span>
                                <span style="background-color: #FEF3C7; color: #D97706; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;">
                                    ⭐ {repo['stargazers_count']:,} stars
                                </span>
                            </div>
                            <p style="color: #64748B; font-size: 14px; margin-top: 8px; margin-bottom: 4px; line-height: 1.4;">
                                {html.escape(repo['description'] or 'No description provided.')}
                            </p>
                            <div style="font-size: 12px; color: #94A3B8; margin-top: 6px;">
                                Main Language Layer: <b>{html.escape(repo['language'] or 'Not Specified')}</b>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    st.markdown('</div>', unsafe_allow_html=True) # Close scrollable div container
                else:
                    st.info("No direct keyword overlaps detected. Market baseline is entirely clear.")
else:
    # --- Custom Responsive Standby Dashboard Card ---
    st.markdown("""
    <div class="custom-card" style="text-align: center; margin-top: 10px;">
        <h4 style="margin-top: 0px; font-weight: 600; font-size: 18px; color: inherit;">System Status: Standby</h4>
        <p style="font-size: 14px; max-width: 500px; margin: 10px auto 0px auto; line-height: 1.5; color: inherit; opacity: 0.8;">
            Configure your project specifications in the left configuration panel and click <b>Run Validation Engine</b> to generate your structural analysis report.
        </p>
    </div>
    """, unsafe_allow_html=True)
