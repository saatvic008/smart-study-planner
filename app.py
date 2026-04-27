import streamlit as st
import pandas as pd
import plotly.express as px
from planner import SmartGreedyPlanner

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Smart Study Planner",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. State Management ---
if 'subjects' not in st.session_state:
    st.session_state.subjects = [
        {"name": "Data Structures", "difficulty": 5, "days_left": 3},
        {"name": "Algorithms", "difficulty": 5, "days_left": 4},
        {"name": "Database Systems", "difficulty": 3, "days_left": 7},
        {"name": "Operating Systems", "difficulty": 3, "days_left": 10},
        {"name": "Computer Networks", "difficulty": 2, "days_left": 12},
        {"name": "Software Engineering", "difficulty": 1, "days_left": 15}
    ]
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# --- 3. Exact UI CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0B0E14;
        color: #FFFFFF;
    }
    
    .stApp { background-color: #0B0E14; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #11141C !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        padding-top: 1rem;
    }
    
    .sidebar-brand { margin-bottom: 2rem; display: flex; align-items: center; gap: 12px; padding: 0 16px; }
    .brand-title { font-weight: 700; font-size: 1.1rem; color: #FFFFFF; line-height: 1.2; }
    .brand-sub { font-size: 0.75rem; color: #94A3B8; }

    /* Navigation Buttons */
    div[data-testid="stSidebarNav"] { display: none; } /* Hide default nav */
    
    .stButton>button {
        width: 100%;
        text-align: left;
        background: transparent;
        border: none;
        color: #94A3B8;
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 0.9rem;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.05);
        color: #FFFFFF;
    }
    
    /* Target Active Nav Button */
    button[key*="nav_"] {
        justify-content: flex-start !important;
    }
    
    /* Header Buttons */
    .stDownloadButton>button {
        background: #6366F1 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
    }
    
    .btn-header-outline button {
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }

    /* Sidebar Tip Card */
    .sidebar-tip {
        background: linear-gradient(135deg, #1E1B4B 0%, #2E1065 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 20px 16px;
        position: relative;
        overflow: hidden;
    }
    .sidebar-tip h5 { color: #A78BFA; margin: 0 0 10px 0; font-size: 0.85rem; display: flex; align-items: center; gap: 6px; }
    .sidebar-tip p { font-size: 0.75rem; color: #E2E8F0; line-height: 1.5; margin: 0; }

    /* Stat Cards */
    .stat-box { border-radius: 12px; padding: 18px; display: flex; align-items: center; gap: 15px; border: 1px solid rgba(255, 255, 255, 0.05); background: #11141C; height: 100%; }
    .icon-sq { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; }
    
    .bg-p { background: rgba(139, 92, 246, 0.12); } .ic-p { background: rgba(139, 92, 246, 0.2); color: #A78BFA; }
    .bg-b { background: rgba(59, 130, 246, 0.12); } .ic-b { background: rgba(59, 130, 246, 0.2); color: #60A5FA; }
    .bg-g { background: rgba(16, 185, 129, 0.12); } .ic-g { background: rgba(16, 185, 129, 0.2); color: #34D399; }
    .bg-y { background: rgba(245, 158, 11, 0.12); } .ic-y { background: rgba(245, 158, 11, 0.2); color: #FBBF24; }

    /* Main Cards */
    .card-wrap { background: #11141C; border-radius: 16px; padding: 24px; border: 1px solid rgba(255, 255, 255, 0.05); height: 100%; }
    
    /* Table Styling */
    .study-table { width: 100%; border-collapse: collapse; }
    .study-table th { color: #64748B; font-size: 0.75rem; text-transform: uppercase; padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .study-table td { padding: 12px; font-size: 0.85rem; border-bottom: 1px solid rgba(255,255,255,0.02); }
    
    .badge { padding: 3px 10px; border-radius: 4px; font-size: 0.7rem; font-weight: 600; }
    .badge-high { background: rgba(99, 102, 241, 0.2); color: #818CF8; }
    .badge-medium { background: rgba(59, 130, 246, 0.2); color: #60A5FA; }
    .badge-low { background: rgba(16, 185, 129, 0.2); color: #34D399; }

    .prog-bar { width: 120px; height: 7px; background: #1E293B; border-radius: 4px; overflow: hidden; }
    .prog-val { height: 100%; border-radius: 4px; }

    /* Insight Glow */
    .insight-glow {
        background: #11141C;
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.1);
        display: flex;
        gap: 15px;
        align-items: center;
    }

    /* Explanation Cards */
    .bottom-card { background: #11141C; border-radius: 12px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.05); height: 100%; }
    .bottom-card h4 { font-size: 1rem; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Sidebar Panel (Functional) ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <span style="font-size: 1.8rem;">🧠</span>
            <div>
                <div class="brand-title">Smart Study Planner</div>
                <div class="brand-sub">Plan Smarter. Study Better.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Functional Navigation
    pages = ["Dashboard", "Subjects", "Schedule", "Progress", "Insights", "Settings"]
    icons = ["🏠", "📚", "📅", "📈", "💡", "⚙️"]
    for page, icon in zip(pages, icons):
        active_style = "background-color: rgba(99, 102, 241, 0.15); color: #A78BFA;" if st.session_state.page == page else ""
        if st.button(f"{icon} {page}", key=f"nav_{page}"):
            st.session_state.page = page
            st.rerun()
    
    st.markdown("---")
    daily_h = st.slider("Daily Capacity", 2, 12, 6)
    total_d = st.slider("Planning Horizon", 1, 14, 7)
    
    with st.form("sidebar_form"):
        st.markdown("##### Add Subject")
        s_name = st.text_input("Name", placeholder="Subject Name")
        s_diff = st.select_slider("Difficulty", options=[1, 2, 3, 4, 5], value=3)
        s_days = st.number_input("Days Left", min_value=1, value=5)
        if st.form_submit_button("Add to Syllabus"):
            if s_name:
                st.session_state.subjects.append({"name": s_name, "difficulty": s_diff, "days_left": s_days})
                st.rerun()

    # Tip Card
    st.markdown("""
        <div class="sidebar-tip">
            <h5><span>💡</span> AI Study Tip ✨</h5>
            <p>Consistency beats intensity. Study a little every day!</p>
        </div>
    """, unsafe_allow_html=True)

# --- 5. Algorithm Processing ---
planner = SmartGreedyPlanner(daily_h, total_d)
for s in st.session_state.subjects:
    planner.add_subject(s['name'], s['difficulty'], s['days_left'])
schedule_df, subjects = planner.generate_schedule()
metrics = planner.get_dashboard_metrics()

# --- 6. Header Section (Functional) ---
h_col1, h_col2 = st.columns([2, 1])
with h_col1:
    st.markdown(f"<h2 style='margin:0;'>Hello, Student! 👋</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 0.95rem; margin-top:5px;'>Let's build a personalized study plan that maximizes your performance.</p>", unsafe_allow_html=True)

with h_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        st.markdown('<div class="btn-header-outline">', unsafe_allow_html=True)
        if st.button("ⓘ How it works", key="btn_how"):
            st.toast("Algorithm: Dynamic Greedy. Complexity: O(n log n).", icon="🧠")
        st.markdown('</div>', unsafe_allow_html=True)
    with b_col2:
        csv = schedule_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📤 Export Plan",
            data=csv,
            file_name="nexus_study_plan.csv",
            mime="text/csv",
            key="btn_export"
        )

# --- 7. Main Body View Logic ---
if st.session_state.page == "Dashboard":
    # Metric Row
    st.markdown("<br>", unsafe_allow_html=True)
    m_c1, m_c2, m_c3, m_c4 = st.columns(4)
    
    def draw_m(col, label, val, sub, icon, bg, ic):
        col.markdown(f"""
            <div class="stat-box {bg}">
                <div class="icon-sq {ic}">{icon}</div>
                <div>
                    <div style="color:#94A3B8; font-size:0.75rem;">{label}</div>
                    <div style="font-size:1.4rem; font-weight:700;">{val}</div>
                    <div style="color:#94A3B8; font-size:0.7rem;">{sub}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    draw_m(m_c1, "Total Subjects", metrics['total_subs'], "Subjects Added", "📕", "bg-p", "ic-p")
    draw_m(m_c2, "Daily Study Hours", daily_h, "Hours / Day", "⏱️", "bg-b", "ic-b")
    draw_m(m_c3, "Planning Horizon", total_d, "Days", "🗓️", "bg-g", "ic-g")
    draw_m(m_c4, "Avg. Priority Score", metrics['avg_priority'], "Out of 100", "⭐", "bg-y", "ic-y")

    # Main Split Layout
    st.markdown("<br>", unsafe_allow_html=True)
    c_main_l, c_main_r = st.columns([1.6, 1])

    with c_main_l:
        st.markdown('<div class="card-wrap">', unsafe_allow_html=True)
        st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <h3 style="margin:0; font-size:1.1rem;">📅 Your Optimized Study Plan (Today)</h3>
                <span class="badge badge-high" style="background:rgba(99,102,241,0.1); color:#818CF8;">Day 1 of {total_d}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Render Table
        tbl = """<table class="study-table">
            <tr><th>#</th><th>Subject</th><th>Priority Score</th><th>Study Time</th></tr>"""
        for i, s in enumerate(subjects):
            b_c = f"badge-{s.priority_level.lower()}"
            p_c = "#818CF8" if s.priority_level == "High" else ("#60A5FA" if s.priority_level == "Medium" else "#34D399")
            h_today = s.total_allocated_hours / total_d
            p_w = min((h_today / 2.0) * 100, 100)
            tbl += f"""
            <tr>
                <td style="color:#64748B;">{i+1}</td>
                <td><b>{s.name}</b></td>
                <td><span class="badge {b_c}">{s.priority_level}</span></td>
                <td>
                    <div style="display:flex; align-items:center; gap:12px;">
                        <div class="prog-bar"><div class="prog-val" style="width:{p_w}%; background:{p_c};"></div></div>
                        <span style="font-weight:500;">{h_today:.1f} hrs</span>
                    </div>
                </td>
            </tr>"""
        tbl += "</table>"
        st.markdown(tbl, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="display:flex; justify-content:space-between; margin-top:25px; padding:0 12px;">
                <div><span style="color:#94A3B8;">Total Allocated</span> &nbsp; <b style="color:#A78BFA;">{metrics['total_hours']/total_d:.1f} hrs</b></div>
                <div><span style="color:#94A3B8;">Remaining Time</span> &nbsp; <b style="color:#34D399;">{max(0, daily_h - (metrics['total_hours']/total_d)):.1f} hr</b></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_main_r:
        st.markdown('<div class="card-wrap">', unsafe_allow_html=True)
        st.markdown('### 🔵 Time Distribution')
        pie_df = pd.DataFrame([{"Subject": s.name, "Hours": s.total_allocated_hours} for s in subjects])
        fig = px.pie(pie_df, values='Hours', names='Subject', hole=0.75, color_discrete_sequence=px.colors.qualitative.Prism)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#FFFFFF", margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""
            <div class="insight-glow">
                <div style="background:rgba(139,92,246,0.2); width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:#A78BFA;">🎯</div>
                <div>
                    <b style="color:#A78BFA; font-size:0.9rem;">Focus Suggestion</b><br>
                    <p style="color:#94A3B8; font-size:0.75rem; margin:5px 0 0 0;">Focus more on <b>{metrics['top_subject']}</b> as it has the highest priority score.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Bottom Explanation
    st.markdown("<br>", unsafe_allow_html=True)
    e1, e2, e3 = st.columns(3)
    with e1:
        st.markdown('<div class="bottom-card"><h4>🧠 Why this plan?</h4><p>We calculate a priority score based on Difficulty, Urgency, and Weightage.</p></div>', unsafe_allow_html=True)
    with e2:
        st.markdown('<div class="bottom-card"><h4>📋 How it works</h4><p>1. Rank Subjects<br>2. Allocate Greedily<br>3. Apply Fair Penalties</p></div>', unsafe_allow_html=True)
    with e3:
        st.markdown('<div class="bottom-card"><h4></> Algorithm</h4><p><b>Dynamic Greedy</b><br>Complexity: O(n log n)</p></div>', unsafe_allow_html=True)

else:
    st.markdown(f"### {st.session_state.page}")
    st.info(f"The {st.session_state.page} view is currently active. All scheduling logic is running in the background.")
    if st.button("Return to Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()
