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

st.markdown("""
<style>
    .main-header { font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 0; }
    .sub-header  { color: #888; font-size: 0.95rem; margin-top: 0; margin-bottom: 2rem; }
    .role-pill   { display:inline-block; padding: 0.3rem 0.9rem; border-radius: 20px;
                   font-size: 0.82rem; margin: 0.2rem 0.2rem; }
    .done    { background:#1a3a1a; color:#4caf50; }
    .running { background:#1a2a3a; color:#64b5f6; }
    .pending { background:#2a2a2a; color:#666; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ROLE SEQUENCE — order, label, progress value after completion
# ─────────────────────────────────────────────────────────────────────────────

ROLE_SEQUENCE = [
    ("role1", "Signal Gathering",            10),
    ("role2", "Founder Analysis",            20),
    ("role3", "Market Analysis",             30),
    ("role4", "Competitor Analysis",         40),
    ("role5", "Capital & Syndicate",         50),
    ("role6", "Traction Stack",              60),
    ("role7", "Synthesis",                   72),
    ("role8", "Adversarial Panel",           85),
    ("role9", "Editorial Assembly",          98),
    ("done",  "Complete",                   100),
]

ROLE_ORDER = [r[0] for r in ROLE_SEQUENCE]

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────

defaults = {
    "running":            False,
    "complete":           False,
    "current_role":       "role1",
    "progress":           0,
    "company_name":       "",
    "company_url":        "",
    "brief_type":         "Funder Brief",
    "additional_context": "",
    "website_content":    "",
    "signal_file":        None,
    "founder_output":     None,
    "market_output":      None,
    "competitor_output":  None,
    "capital_output":     None,
    "traction_output":    None,
    "synthesis_output":   None,
    "adversarial_output": None,
    "final_brief":        None,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

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


def call_claude(system_prompt, user_content, model="claude-sonnet-4-6", max_tokens=4000):
    client = get_client()
    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}],
        )
        return response.content[0].text
    except Exception as e:
        return f"[ERROR — {str(e)}]"


def fetch_website(url):
    try:
        if not url.startswith("http"):
            url = "https://" + url
        headers = {"User-Agent": "Mozilla/5.0 (compatible; VantageBot/1.0)"}
        resp = requests.get(url, headers=headers, timeout=12)
        soup = BeautifulSoup(resp.content, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text[:6000]
    except Exception as e:
        return f"Website fetch failed: {str(e)}"


def reset():
    for k, v in defaults.items():
        st.session_state[k] = v
    st.rerun()


def role_progress_display():
    """Render pill-style role progress indicators."""
    pills_html = ""
    for role_key, label, done_at in ROLE_SEQUENCE[:-1]:  # skip "done"
        current = st.session_state.current_role
        progress = st.session_state.progress
        role_done_at = done_at

        if progress >= role_done_at:
            css = "done"
            icon = "✓"
        elif current == role_key:
            css = "running"
            icon = "⟳"
        else:
            css = "pending"
            icon = "○"

        pills_html += f'<span class="role-pill {css}">{icon} {label}</span>'

    st.markdown(pills_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SINGLE-ROLE EXECUTION (one role per Streamlit rerun cycle)
# ─────────────────────────────────────────────────────────────────────────────

def execute_current_role():
    """Run whichever role is currently queued, save output, advance the pointer."""
    role = st.session_state.current_role
    s = st.session_state  # shorthand

    if role == "role1":
        website = fetch_website(s.company_url)
        s.website_content = website
        user_input = f"""Company name: {s.company_name}
Company URL: {s.company_url}
Brief type: {s.brief_type}
Additional context: {s.additional_context or 'None'}

WEBSITE CONTENT (Tier 1 — fetched from {s.company_url}):
{website}

Use the above as your primary Tier 1 source. Apply the full five-tier protocol
for all other tiers using your knowledge of this company."""
        s.signal_file = call_claude(ROLE_1_INGESTION, user_input, max_tokens=5000)
        s.progress = 10
        s.current_role = "role2"

    elif role == "role2":
        s.founder_output = call_claude(
            ROLE_2_FOUNDER,
            f"VANTAGE SIGNAL FILE:\n\n{s.signal_file}",
            max_tokens=1500
        )
        s.progress = 20
        s.current_role = "role3"

    elif role == "role3":
        s.market_output = call_claude(
            ROLE_3_MARKET,
            f"VANTAGE SIGNAL FILE:\n\n{s.signal_file}",
            max_tokens=1000
        )
        s.progress = 30
        s.current_role = "role4"

    elif role == "role4":
        s.competitor_output = call_claude(
            ROLE_4_COMPETITOR,
            f"VANTAGE SIGNAL FILE:\n\n{s.signal_file}",
            max_tokens=1200
        )
        s.progress = 40
        s.current_role = "role5"

    elif role == "role5":
        s.capital_output = call_claude(
            ROLE_5_CAPITAL,
            f"VANTAGE SIGNAL FILE:\n\n{s.signal_file}",
            max_tokens=1500
        )
        s.progress = 50
        s.current_role = "role6"

    elif role == "role6":
        s.traction_output = call_claude(
            ROLE_6_TRACTION,
            f"VANTAGE SIGNAL FILE:\n\n{s.signal_file}",
            max_tokens=1200
        )
        s.progress = 60
        s.current_role = "role7"

    elif role == "role7":
        synthesis_input = f"""VANTAGE SIGNAL FILE:\n{s.signal_file}

ROLE 2 — FOUNDER ANALYST:\n{s.founder_output}

ROLE 3 — MARKET ANALYST:\n{s.market_output}

ROLE 4 — COMPETITOR ANALYST:\n{s.competitor_output}

ROLE 5 — CAPITAL ANALYST:\n{s.capital_output}

ROLE 6 — TRACTION ANALYST:\n{s.traction_output}"""
        s.synthesis_output = call_claude(
            ROLE_7_SYNTHESIS, synthesis_input,
            model="claude-opus-4-6", max_tokens=2500
        )
        s.progress = 72
        s.current_role = "role8"

    elif role == "role8":
        s.adversarial_output = call_claude(
            ROLE_8_ADVERSARIAL,
            f"VANTAGE SIGNAL FILE (only input):\n\n{s.signal_file}",
            model="claude-opus-4-6", max_tokens=3000
        )
        s.progress = 85
        s.current_role = "role9"

    elif role == "role9":
        editor_input = f"""SIGNAL FILE:\n{s.signal_file}

ROLE 2 — FOUNDER:\n{s.founder_output}

ROLE 3 — MARKET:\n{s.market_output}

ROLE 4 — COMPETITOR:\n{s.competitor_output}

ROLE 5 — CAPITAL:\n{s.capital_output}

ROLE 6 — TRACTION:\n{s.traction_output}

ROLE 7 — SYNTHESIS:\n{s.synthesis_output}

ROLE 8 — ADVERSARIAL:\n{s.adversarial_output}"""
        s.final_brief = call_claude(
            ROLE_9_EDITOR, editor_input,
            max_tokens=8000
        )
        s.progress = 100
        s.current_role = "done"
        s.running = False
        s.complete = True


# ─────────────────────────────────────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────────────────────────────────────

st.markdown('<p class="main-header">⚡ Vantage Intelligence</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-assisted investor-grade decision briefing — frontier markets</p>', unsafe_allow_html=True)
st.divider()

# ── INPUT FORM ────────────────────────────────────────────────────────────────
if not st.session_state.running and not st.session_state.complete:
    with st.form("brief_form"):
        st.markdown("#### Request a Vantage Brief")
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name *", placeholder="e.g. littlefish")
            company_url  = st.text_input("Company URL *",  placeholder="e.g. littlefishapp.com")
        with col2:
            brief_type = st.selectbox("Brief Type", ["Funder Brief", "Founder Brief"])
            additional_context = st.text_area(
                "Additional context (optional)",
                placeholder="Paste any relevant info — funding announcement, deck, press...",
                height=105
            )
        st.caption("ℹ️ The app fetches the company website automatically. Add additional context for higher signal quality.")
        submitted = st.form_submit_button("▶ Run Vantage Brief", type="primary", use_container_width=True)

    if submitted:
        if not company_name.strip():
            st.error("Company name is required.")
        elif not company_url.strip():
            st.error("Company URL is required.")
        else:
            st.session_state.company_name       = company_name.strip()
            st.session_state.company_url        = company_url.strip()
            st.session_state.brief_type         = brief_type
            st.session_state.additional_context = additional_context.strip()
            st.session_state.running            = True
            st.session_state.current_role       = "role1"
            st.session_state.progress           = 0
            st.rerun()

# ── PIPELINE — one role per rerun ─────────────────────────────────────────────
if st.session_state.running:
    st.markdown(f"#### Running Brief — **{st.session_state.company_name}**")
    st.progress(st.session_state.progress / 100)
    role_progress_display()

    # Show which role is currently running
    current_label = next(
        (label for key, label, _ in ROLE_SEQUENCE if key == st.session_state.current_role),
        "Processing"
    )
    with st.spinner(f"Running: {current_label}…"):
        execute_current_role()

    st.rerun()

# ── BRIEF OUTPUT ──────────────────────────────────────────────────────────────
if st.session_state.complete and st.session_state.final_brief:

    col_title, col_dl, col_new = st.columns([4, 1, 1])
    with col_title:
        st.markdown(f"#### Vantage Brief — {st.session_state.company_name}")
        st.caption(f"Generated {datetime.now().strftime('%d %B %Y, %H:%M')} UTC")
    with col_dl:
        st.download_button(
            label="⬇ Download",
            data=st.session_state.final_brief,
            file_name=f"Vantage_Brief_{st.session_state.company_name.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True,
            key="download_btn"
        )
    with col_new:
        if st.button("↺ New Brief", use_container_width=True, key="reset_top"):
            reset()

    st.divider()
    st.markdown(st.session_state.final_brief)

    with st.expander("View Signal File (Role 1 raw output)", expanded=False):
        st.text(st.session_state.signal_file or "Not available")

    # ── FEEDBACK ──────────────────────────────────────────────────────────────
    st.divider()
    st.markdown("#### Tester Feedback")
    st.caption("Your feedback goes directly to the Vantage team and improves the system.")

    with st.form("feedback_form"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            call_accuracy = st.radio(
                "Was the investment call accurate?",
                ["Yes — I agree", "Direction right, confidence wrong",
                 "No — I would call this differently", "Can't assess"],
                index=3
            )
            adv_quality = st.radio(
                "Were the Risks & Unknowns specific to this company?",
                ["Yes — specific and non-obvious", "Partially",
                 "No — too generic", "Can't assess"],
                index=3
            )
        with col_f2:
            most_useful = st.selectbox(
                "Most useful section?",
                ["60-Second View", "Founder Analysis", "Market Analysis",
                 "Competitive Landscape", "Capital & Syndicate", "Traction Stack",
                 "Pattern Recognition", "Risks & Unknowns",
                 "Suggested Questions", "Investment Perspective"]
            )
            needs_work = st.selectbox(
                "Section most needing improvement?",
                ["60-Second View", "Founder Analysis", "Market Analysis",
                 "Competitive Landscape", "Capital & Syndicate", "Traction Stack",
                 "Pattern Recognition", "Risks & Unknowns",
                 "Suggested Questions", "Investment Perspective"]
            )

        missing = st.text_area(
            "What signal was missing that you know to be important?",
            placeholder="e.g. The brief didn't surface that the CEO previously failed a company in Nigeria..."
        )
        override = st.text_area(
            "If you'd change the call or any finding — what and why?",
            placeholder="e.g. I'd call Monitor not Investigate because the exit mechanism is structurally illiquid..."
        )
        general = st.text_area("Any other feedback?")

        if st.form_submit_button("Submit Feedback", use_container_width=True):
            st.session_state["last_feedback"] = {
                "company": st.session_state.company_name,
                "date": datetime.now().isoformat(),
                "call_accuracy": call_accuracy,
                "adversarial_quality": adv_quality,
                "most_useful": most_useful,
                "needs_work": needs_work,
                "missing_signal": missing,
                "override": override,
                "general": general,
            }
            st.success("✓ Feedback recorded. Thank you.")

