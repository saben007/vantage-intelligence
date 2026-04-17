import streamlit as st
import anthropic
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

from prompts import (
    ROLE_1_INGESTION,
    ROLE_2_FOUNDER,
    ROLE_3_MARKET,
    ROLE_4_COMPETITOR,
    ROLE_5_CAPITAL,
    ROLE_6_TRACTION,
    ROLE_7_SYNTHESIS,
    ROLE_8_ADVERSARIAL,
    ROLE_9_EDITOR,
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Vantage Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0;
    }
    .sub-header {
        color: #888;
        font-size: 0.95rem;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .role-status {
        padding: 0.4rem 0.8rem;
        border-radius: 4px;
        font-size: 0.85rem;
        margin: 0.2rem 0;
    }
    .role-complete { background-color: #1a3a1a; color: #4caf50; }
    .role-running  { background-color: #1a2a3a; color: #64b5f6; }
    .role-pending  { background-color: #2a2a2a; color: #888; }
    .brief-container {
        background-color: #0e1117;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 2rem;
        margin-top: 1rem;
    }
    .feedback-box {
        background-color: #111;
        border: 1px solid #222;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 2rem;
    }
    .stProgress > div > div { background-color: #64b5f6; }
    div[data-testid="stForm"] { border: none; padding: 0; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────

defaults = {
    "running": False,
    "complete": False,
    "current_role": None,
    "progress": 0,
    "signal_file": None,
    "founder_output": None,
    "market_output": None,
    "competitor_output": None,
    "capital_output": None,
    "traction_output": None,
    "synthesis_output": None,
    "adversarial_output": None,
    "final_brief": None,
    "company_name": "",
    "company_url": "",
    "errors": [],
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def get_client():
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        return anthropic.Anthropic(api_key=api_key)
    except Exception:
        st.error("⚠️ API key not found. Add ANTHROPIC_API_KEY to your Streamlit secrets.")
        st.stop()


def call_claude(client, system_prompt, user_content, model="claude-sonnet-4-6", max_tokens=4000):
    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}],
        )
        return response.content[0].text
    except Exception as e:
        return f"[ERROR — role failed: {str(e)}]"


def fetch_website(url):
    """Fetch homepage content for Tier 1 signal enrichment."""
    try:
        if not url.startswith("http"):
            url = "https://" + url
        headers = {"User-Agent": "Mozilla/5.0 (compatible; VantageBot/1.0)"}
        resp = requests.get(url, headers=headers, timeout=12)
        soup = BeautifulSoup(resp.content, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        # Remove excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text[:6000]
    except Exception as e:
        return f"Website fetch failed: {str(e)}"


def reset():
    for key, val in defaults.items():
        st.session_state[key] = val
    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE
# ─────────────────────────────────────────────────────────────────────────────

ROLES = [
    ("role1",  "Signal Intelligence — Ingestion Analyst",    10),
    ("role2",  "Founder Analysis",                            20),
    ("role3",  "Market Analysis",                             30),
    ("role4",  "Competitor Analysis",                         40),
    ("role5",  "Capital & Syndicate Analysis",                50),
    ("role6",  "Traction Analysis",                           60),
    ("role7",  "Synthesis",                                   70),
    ("role8",  "Adversarial Panel — Independent Challenge",   82),
    ("role9",  "Editorial Assembly — Final Brief",            95),
    ("done",   "Complete",                                   100),
]


def run_pipeline(company_name, url, brief_type, additional_context):
    client = get_client()

    # ── Role 1 — Ingestion ────────────────────────────────────────────────
    st.session_state.current_role = "role1"
    website_content = fetch_website(url)

    user_input_r1 = f"""Company name: {company_name}
Company URL: {url}
Brief type: {brief_type}
Additional context provided by requester: {additional_context if additional_context else 'None'}

WEBSITE CONTENT (Tier 1 — fetched from {url}):
{website_content}

Use the above website content as your primary Tier 1 source. Apply the full
five-tier protocol for all other tiers using your knowledge of this company."""

    st.session_state.signal_file = call_claude(
        client, ROLE_1_INGESTION, user_input_r1, max_tokens=5000
    )
    st.session_state.progress = 10

    # ── Role 2 — Founder ──────────────────────────────────────────────────
    st.session_state.current_role = "role2"
    st.session_state.founder_output = call_claude(
        client, ROLE_2_FOUNDER,
        f"VANTAGE SIGNAL FILE:\n\n{st.session_state.signal_file}",
        max_tokens=1500
    )
    st.session_state.progress = 20

    # ── Role 3 — Market ───────────────────────────────────────────────────
    st.session_state.current_role = "role3"
    st.session_state.market_output = call_claude(
        client, ROLE_3_MARKET,
        f"VANTAGE SIGNAL FILE:\n\n{st.session_state.signal_file}",
        max_tokens=1000
    )
    st.session_state.progress = 30

    # ── Role 4 — Competitor ───────────────────────────────────────────────
    st.session_state.current_role = "role4"
    st.session_state.competitor_output = call_claude(
        client, ROLE_4_COMPETITOR,
        f"VANTAGE SIGNAL FILE:\n\n{st.session_state.signal_file}",
        max_tokens=1200
    )
    st.session_state.progress = 40

    # ── Role 5 — Capital ──────────────────────────────────────────────────
    st.session_state.current_role = "role5"
    st.session_state.capital_output = call_claude(
        client, ROLE_5_CAPITAL,
        f"VANTAGE SIGNAL FILE:\n\n{st.session_state.signal_file}",
        max_tokens=1500
    )
    st.session_state.progress = 50

    # ── Role 6 — Traction ─────────────────────────────────────────────────
    st.session_state.current_role = "role6"
    st.session_state.traction_output = call_claude(
        client, ROLE_6_TRACTION,
        f"VANTAGE SIGNAL FILE:\n\n{st.session_state.signal_file}",
        max_tokens=1200
    )
    st.session_state.progress = 60

    # ── Role 7 — Synthesis ────────────────────────────────────────────────
    st.session_state.current_role = "role7"
    synthesis_input = f"""VANTAGE SIGNAL FILE:
{st.session_state.signal_file}

ROLE 2 — FOUNDER ANALYST OUTPUT:
{st.session_state.founder_output}

ROLE 3 — MARKET ANALYST OUTPUT:
{st.session_state.market_output}

ROLE 4 — COMPETITOR ANALYST OUTPUT:
{st.session_state.competitor_output}

ROLE 5 — CAPITAL ANALYST OUTPUT:
{st.session_state.capital_output}

ROLE 6 — TRACTION ANALYST OUTPUT:
{st.session_state.traction_output}"""

    st.session_state.synthesis_output = call_claude(
        client, ROLE_7_SYNTHESIS, synthesis_input,
        model="claude-opus-4-6", max_tokens=2500
    )
    st.session_state.progress = 70

    # ── Role 8 — Adversarial (isolation: signal file only) ────────────────
    st.session_state.current_role = "role8"
    st.session_state.adversarial_output = call_claude(
        client, ROLE_8_ADVERSARIAL,
        f"VANTAGE SIGNAL FILE (this is the only input you receive):\n\n{st.session_state.signal_file}",
        model="claude-opus-4-6", max_tokens=3000
    )
    st.session_state.progress = 82

    # ── Role 9 — Editor ───────────────────────────────────────────────────
    st.session_state.current_role = "role9"
    editor_input = f"""VANTAGE SIGNAL FILE:
{st.session_state.signal_file}

ROLE 2 — FOUNDER ANALYST:
{st.session_state.founder_output}

ROLE 3 — MARKET ANALYST:
{st.session_state.market_output}

ROLE 4 — COMPETITOR ANALYST:
{st.session_state.competitor_output}

ROLE 5 — CAPITAL ANALYST:
{st.session_state.capital_output}

ROLE 6 — TRACTION ANALYST:
{st.session_state.traction_output}

ROLE 7 — SYNTHESIS ANALYST:
{st.session_state.synthesis_output}

ROLE 8 — ADVERSARIAL PANEL:
{st.session_state.adversarial_output}"""

    st.session_state.final_brief = call_claude(
        client, ROLE_9_EDITOR, editor_input,
        max_tokens=8000
    )
    st.session_state.progress = 100
    st.session_state.current_role = "done"
    st.session_state.complete = True
    st.session_state.running = False


# ─────────────────────────────────────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────────────────────────────────────

# Header
col_title, col_reset = st.columns([5, 1])
with col_title:
    st.markdown('<p class="main-header">⚡ Vantage Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-assisted investor-grade decision briefing — frontier markets</p>', unsafe_allow_html=True)
with col_reset:
    if st.session_state.complete or st.session_state.running:
        st.write("")
        st.write("")
        if st.button("↺ New Brief", use_container_width=True):
            reset()

st.divider()

# ── INPUT FORM (hidden while running or complete) ─────────────────────────────
if not st.session_state.running and not st.session_state.complete:
    with st.form("brief_form"):
        st.markdown("#### Request a Vantage Brief")

        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input(
                "Company Name *",
                placeholder="e.g. littlefish"
            )
            company_url = st.text_input(
                "Company URL *",
                placeholder="e.g. littlefishapp.com"
            )
        with col2:
            brief_type = st.selectbox(
                "Brief Type",
                ["Funder Brief", "Founder Brief"],
                help="Funder Brief: investment decision tool. Founder Brief: raise readiness assessment."
            )
            additional_context = st.text_area(
                "Additional context (optional)",
                placeholder="Any documents, context, or specific areas to focus on...",
                height=105
            )

        st.caption("ℹ️ Signal gathering uses the company website plus model knowledge. Provide additional context for higher signal quality.")

        submitted = st.form_submit_button(
            "▶ Run Vantage Brief",
            type="primary",
            use_container_width=True
        )

    if submitted:
        if not company_name.strip():
            st.error("Company name is required.")
        elif not company_url.strip():
            st.error("Company URL is required.")
        else:
            st.session_state.company_name = company_name.strip()
            st.session_state.company_url = company_url.strip()
            st.session_state.running = True
            st.rerun()

# ── PIPELINE PROGRESS ─────────────────────────────────────────────────────────
if st.session_state.running:
    st.markdown(f"#### Running Brief — {st.session_state.company_name}")
    progress_bar = st.progress(st.session_state.progress / 100)
    status_placeholder = st.empty()

    role_display = {
        "role1": "Gathering signals — Ingestion Analyst",
        "role2": "Analysing founding team",
        "role3": "Analysing market formation",
        "role4": "Mapping competitive landscape",
        "role5": "Assessing capital and syndicate",
        "role6": "Building traction stack",
        "role7": "Synthesising analyst outputs",
        "role8": "Running adversarial panel — independent challenge",
        "role9": "Assembling final Brief",
        "done":  "Brief complete",
    }

    for key, val in defaults.items():
        if key not in ["company_name", "company_url", "running"]:
            pass

    with st.spinner(""):
        # Role status display
        cols = st.columns(3)
        role_keys = ["role1","role2","role3","role4","role5","role6","role7","role8","role9"]
        for i, rk in enumerate(role_keys):
            label = role_display[rk]
            if st.session_state.current_role == rk:
                cols[i % 3].markdown(
                    f'<div class="role-status role-running">⟳ {label}</div>',
                    unsafe_allow_html=True
                )
            elif st.session_state.progress >= [10,20,30,40,50,60,70,82,95][i]:
                cols[i % 3].markdown(
                    f'<div class="role-status role-complete">✓ {label}</div>',
                    unsafe_allow_html=True
                )
            else:
                cols[i % 3].markdown(
                    f'<div class="role-status role-pending">○ {label}</div>',
                    unsafe_allow_html=True
                )

        # Execute pipeline
        run_pipeline(
            st.session_state.company_name,
            st.session_state.company_url,
            "Funder Brief",
            ""
        )

    st.rerun()

# ── BRIEF OUTPUT ──────────────────────────────────────────────────────────────
if st.session_state.complete and st.session_state.final_brief:

    # Summary bar
    col_a, col_b, col_c = st.columns([3, 1, 1])
    with col_a:
        st.markdown(f"#### Vantage Brief — {st.session_state.company_name}")
        st.caption(f"Generated {datetime.now().strftime('%d %B %Y, %H:%M')} UTC")
    with col_b:
        brief_md = st.session_state.final_brief
        st.download_button(
            label="⬇ Download (.md)",
            data=brief_md,
            file_name=f"Vantage_Brief_{st.session_state.company_name.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col_c:
        if st.button("↺ New Brief", use_container_width=True):
            reset()

    st.divider()

    # Brief display
    st.markdown(
        f'<div class="brief-container">{brief_md}</div>',
        unsafe_allow_html=True
    )

    # Signal file expander (for transparency)
    with st.expander("View Signal File (Role 1 output)", expanded=False):
        st.text(st.session_state.signal_file or "Not available")

    # ── FEEDBACK ──────────────────────────────────────────────────────────
    st.divider()
    st.markdown("#### Feedback")
    st.caption("This helps improve the system. Your feedback goes directly to the Vantage team.")

    with st.form("feedback_form"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            call_accuracy = st.radio(
                "Was the investment call (Investigate / Monitor / Pass) accurate?",
                ["Yes — I agree with the call",
                 "Partially — direction right but confidence wrong",
                 "No — I would have called this differently",
                 "Can't assess"],
                index=3
            )
            adv_quality = st.radio(
                "Was the adversarial section (Risks & Unknowns) specific to this company?",
                ["Yes — findings were specific and non-obvious",
                 "Partially — some specific, some generic",
                 "No — too generic",
                 "Can't assess"],
                index=3
            )
        with col_f2:
            most_useful = st.selectbox(
                "Which section was most useful?",
                ["60-Second View", "Founder Analysis", "Market Analysis",
                 "Competitive Landscape", "Capital & Syndicate",
                 "Traction Stack", "Pattern Recognition",
                 "Risks & Unknowns", "Suggested Questions",
                 "Investment Perspective"]
            )
            least_useful = st.selectbox(
                "Which section needs the most improvement?",
                ["60-Second View", "Founder Analysis", "Market Analysis",
                 "Competitive Landscape", "Capital & Syndicate",
                 "Traction Stack", "Pattern Recognition",
                 "Risks & Unknowns", "Suggested Questions",
                 "Investment Perspective"]
            )

        missing_signal = st.text_area(
            "What signal was missing that you know to be important?",
            placeholder="e.g. The brief didn't surface that the CEO previously failed a company in Nigeria..."
        )
        override = st.text_area(
            "If you would change the call or any finding — what and why?",
            placeholder="e.g. I would call Monitor not Investigate because the exit mechanism is structurally illiquid..."
        )
        general = st.text_area(
            "Any other feedback?",
            placeholder="..."
        )

        fb_submitted = st.form_submit_button("Submit Feedback", use_container_width=True)

    if fb_submitted:
        # Store feedback in session state (operator reviews via session logs)
        feedback_text = f"""VANTAGE BRIEF FEEDBACK
Company: {st.session_state.company_name}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Call accuracy: {call_accuracy}
Adversarial quality: {adv_quality}
Most useful section: {most_useful}
Needs most improvement: {least_useful}

Missing signal:
{missing_signal}

Override / adjustment:
{override}

General feedback:
{general}
"""
        st.session_state["last_feedback"] = feedback_text
        st.success("✓ Feedback recorded. Thank you.")
