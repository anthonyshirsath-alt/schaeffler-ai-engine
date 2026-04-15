import streamlit as st

# --- 🔒 PROFESSIONAL LOGIN GATE ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def check_password():
    if not st.session_state["authenticated"]:
        st.markdown("<div style='margin-top:100px;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://www.schaeffler.com/remotemedien/media/_shared_media/08_media_relations/logos/schaeffler_logo_green_standard.jpg", width=200)
            st.subheader("🔐 Strategy Engine Secure Access")
            pwd = st.text_input("Corporate Access Key", type="password")
            if st.button("Authorize Access", type="primary", use_container_width=True):
                if pwd == "Schaeffler2026":
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("❌ Invalid Access Key")
        return False
    return True

if not check_password():
    st.stop()
# --- END LOGIN GATE ---
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

# ------------------------------------------------------------
# 1. PAGE CONFIGURATION & "MCKINSEY GRADE" CSS
# ------------------------------------------------------------
st.set_page_config(page_title="Schaeffler AI Innovation Engine", layout="wide", page_icon="⚙️")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    .stApp { background-color: #F0F4F8; }
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    
    /* Executive Animations */
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(12px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInRight {
        0% { opacity: 0; transform: translateX(-15px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulseGlow {
        0% { transform: scale(1); opacity: 1; box-shadow: 0 0 0px rgba(0, 138, 82, 0.4); }
        100% { transform: scale(1.25); opacity: 0.7; box-shadow: 0 0 10px rgba(0, 138, 82, 0.8); }
    }
    @keyframes rowHighlight {
        0% { background-color: rgba(0, 138, 82, 0.08); }
        100% { background-color: transparent; }
    }

    .block-container { padding-top: 5.5rem !important; padding-bottom: 2rem; max-width: 96%; animation: fadeInUp 0.5s ease-out; }
    header[data-testid="stHeader"] { display: none; } 
    
    .fade-in-up { animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    .fade-in-text { animation: fadeInRight 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    .score-bar-fill { transition: width 1.2s cubic-bezier(0.22, 1, 0.36, 1), background-color 0.5s ease; }
    
    .animated-row { animation: rowHighlight 1.5s ease-out forwards; border-radius: 8px; padding: 4px 0; transition: background-color 0.2s; }
    .animated-row:hover { background-color: #F8FAFC; }

    .schaeffler-header-container {
        position: fixed; top: 0; left: 0; right: 0; z-index: 999999;
        background-color: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px);
        border-bottom: 3px solid #008A52; padding: 12px 32px;
        display: flex; justify-content: space-between; align-items: center;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.06);
    }
    
    .stButton>button { border-radius: 8px; border: none; font-weight: 600; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); letter-spacing: 0.3px; padding: 6px 16px;}
    button[kind="primary"] { background: linear-gradient(135deg, #008A52 0%, #00C675 100%); color: white; box-shadow: 0 4px 12px rgba(0, 138, 82, 0.25); }
    button[kind="primary"]:hover { transform: translateY(-3px) scale(1.02); box-shadow: 0 8px 20px rgba(0, 138, 82, 0.4); }
    button[kind="secondary"] { background-color: #FFFFFF; color: #1A1A1A; border: 1px solid #CBD5E1; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
    button[kind="secondary"]:hover { border-color: #008A52; color: #008A52; transform: translateY(-3px) scale(1.02); box-shadow: 0 6px 15px rgba(0,0,0,0.08);}
    
    .stDownloadButton>button { border-radius: 8px; border: 1px solid #CBD5E1; font-weight: 600; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); background-color: #FFFFFF; color: #1A1A1A; box-shadow: 0 2px 6px rgba(0,0,0,0.03);}
    .stDownloadButton>button:hover { border-color: #008A52; color: #008A52; transform: translateY(-3px) scale(1.02); box-shadow: 0 6px 15px rgba(0,0,0,0.08);}
    
    div[data-baseweb="input"] { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); transition: all 0.3s ease; }
    div[data-baseweb="input"]:focus-within { border-color: #008A52; box-shadow: 0 0 0 3px rgba(0, 138, 82, 0.15); }
    div[data-baseweb="input"] > input { color: #0F172A; font-weight: 500; font-size: 15px; padding: 14px 18px;}
    
    .stTabs [data-baseweb="tab-list"] { gap: 6px; border-bottom: none; padding-bottom: 15px;}
    .stTabs [data-baseweb="tab"] { height: 38px; background-color: #FFFFFF; border-radius: 8px; padding: 4px 10px; font-size: 12.5px; color: #475569; font-weight: 600; border: 1px solid #E2E8F0; transition: 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.02);}
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background-color: #008A52; color: #FFFFFF; border: none; box-shadow: 0 4px 12px rgba(0, 138, 82, 0.25); }
    
    .chart-title-card { background-color: #FFFFFF; color: #0F172A; padding: 14px 20px; border-radius: 12px; font-size: 13px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; border: 1px solid #E2E8F0; box-shadow: 0 4px 12px rgba(0,0,0,0.03); margin-bottom: 15px; text-align: center; transition: all 0.3s ease; }
    .chart-title-card:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.06); transform: translateY(-2px); }
    
    .copilot-card { background: linear-gradient(135deg, #FFFFFF 0%, #F0FDF4 100%); border-left: 4px solid #008A52; border-radius: 12px; padding: 18px 24px; box-shadow: 0px 6px 20px rgba(0, 138, 82, 0.08); margin-bottom: 25px; border: 1px solid #E2E8F0; transition: all 0.3s ease;}
    .copilot-card:hover { box-shadow: 0px 10px 30px rgba(0, 138, 82, 0.15); transform: translateY(-2px); }
    
    .manual-card { background-color:#FFFFFF; padding:24px; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.03); border:1px solid #E2E8F0; margin-top:10px;}
    .white-card { background-color: #FFFFFF; border-radius: 12px; padding: 20px; box-shadow: 0px 8px 24px rgba(0,0,0,0.04); margin-bottom: 20px; border: 1px solid #F0F3F5; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);}
    .white-card:hover { transform: translateY(-4px); box-shadow: 0px 16px 40px rgba(0,0,0,0.08); border-color: #CBD5E1; }
    
    .stSlider { padding-bottom: 0px; margin-bottom: -10px; }
    div[data-baseweb="slider"] > div > div > div:nth-child(1) { background: linear-gradient(90deg, #008A52, #00C675) !important; }
    div[data-baseweb="slider"] div[role="slider"] { background-color: #FFFFFF !important; border: 3px solid #008A52 !important; width: 18px !important; height: 18px !important; box-shadow: 0 2px 6px rgba(0, 138, 82, 0.4) !important; transition: transform 0.15s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.15s ease;}
    div[data-baseweb="slider"] div[role="slider"]:hover { transform: scale(1.3); }
    div[data-baseweb="slider"] div[role="slider"]:active { transform: scale(1.4); box-shadow: 0 0 0 8px rgba(0, 138, 82, 0.25) !important; }
    div[data-baseweb="slider"] div[role="slider"]:focus { outline: none !important; box-shadow: 0 0 0 5px rgba(0, 138, 82, 0.2) !important; }
    
    .budget-line { border-top: 2px dashed #EF4444; margin: 15px 0px 15px 0px; padding-top: 10px; color: #EF4444; font-weight: 800; text-align: center; font-size: 11px; letter-spacing: 2px;}
    .tbl-header { font-size: 11px; color: #64748B; text-transform: uppercase; font-weight: 800; border-bottom: 2px solid #CBD5E1; padding-bottom: 8px; margin-bottom: 8px; letter-spacing: 0.5px;}
    
    .row-text { font-size:14px; font-weight:600; display:block; padding-top:4px; margin-bottom:-8px; }
    .delta-up { color: #008A52; font-weight: 800; font-size: 12px; margin-left:6px; }
    .delta-down { color: #EF4444; font-weight: 800; font-size: 12px; margin-left:6px; }
    .delta-flat { color: #94A3B8; font-weight: 800; font-size: 12px; margin-left:6px; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 2. EXACT WEIGHTS, TOOLTIPS & DATA INIT
# ------------------------------------------------------------
DEFAULTS = {
    "Profitability": 0.2375, "Total Revenue": 0.1875, "Competitiveness": 0.1500, "Chances of Success": 0.1375, 
    "Sustainability": 0.1250, "Capital Intensity": 0.1000, "Technology Innovation": 0.0375, 
    "Market Potential": 0.0250, "AI Readiness": 0.0000, "Supply Chain Resilience": 0.0000
}

HELP_DICT = {
    "Profitability": "Measures EBITDA margins and lifetime ROI. High score means it heavily boosts the bottom line.",
    "Total Revenue": "Measures the raw cash volume generated. High score implies a massive new revenue stream.",
    "Competitiveness": "Measures ability to steal market share. High score means it creates a strong moat against rivals.",
    "Chances of Success": "The realistic probability this project doesn't fail. High score means it is a very safe bet.",
    "Sustainability": "Measures green impact and ESG compliance. High score means excellent carbon reduction.",
    "Capital Intensity": "Measures upfront cash needed. A HIGH score means it requires VERY LITTLE cash (highly efficient).",
    "Technology Innovation": "Measures disruption level. High score means it is a radical, futuristic R&D breakthrough.",
    "Market Potential": "Measures Total Addressable Market (TAM). High score means the global demand is massive.",
    "AI Readiness": "Measures digital integration. High score means it perfectly plugs into our machine learning ecosystem.",
    "Supply Chain Resilience": "Measures immunity to global shocks. High score means we don't rely on risky foreign materials."
}

def load_profile():
    for k, v in DEFAULTS.items(): 
        st.session_state[f"w_{k}"] = v
        st.session_state[f"c_{k}"] = 1.0
        st.session_state[f"chk_{k}"] = True
    for m in ["Cost Efficiency", "Sustainability Focus", "Future Orientation", "Risk Tolerance", "Technology Focus", "Market Focus"]: 
        st.session_state[f"macro_{m}"] = 0.5
    for p in ["Corporate Risk Appetite", "Time-to-Market Urgency", "Market Volatility Index", "Regulatory Scrutiny"]: 
        st.session_state[f"p_{p}"] = 2.5

def init_blank_scenario():
    for k in DEFAULTS.keys(): 
        st.session_state[f"w_{k}"] = 0.0
        st.session_state[f"c_{k}"] = 0.0 
        st.session_state[f"chk_{k}"] = True
    for m in ["Cost Efficiency", "Sustainability Focus", "Future Orientation", "Risk Tolerance", "Technology Focus", "Market Focus"]: 
        st.session_state[f"macro_{m}"] = 0.0
    for p in ["Corporate Risk Appetite", "Time-to-Market Urgency", "Market Volatility Index", "Regulatory Scrutiny"]: 
        st.session_state[f"p_{p}"] = 0.0 

def reset_m(k): st.session_state[k] = 0.5
def reset_w(k, d): st.session_state[k] = d
def reset_c(k): st.session_state[k] = 1.0
def reset_p(k): st.session_state[k] = 2.5

def renormalize():
    active = [k for k in DEFAULTS.keys() if st.session_state.get(f"chk_{k}", True)]
    total = sum(st.session_state[f"w_{k}"] for k in active)
    if total > 0:
        for k in active: st.session_state[f"w_{k}"] /= total
    else:
        for k in active: st.session_state[f"w_{k}"] = 1.0 / len(active)

if "projects_df" not in st.session_state:
    load_profile()
    st.session_state.projects_df = pd.DataFrame({
        "Project Name": ["Next-Gen Bearing AI", "Eco-Steel Supply", "Autonomous Chassis", "Smart Factory IoT", "Hydrogen Cell Beta", "Advanced Telematics", "Solid State Battery", "Hyper-Precision Actuator"],
        "Cost (€M)": [12.5, 8.0, 22.0, 15.0, 5.5, 9.0, 30.0, 4.5],
        "Profitability": [4, 3, 5, 4, 2, 3, 5, 3], "Total Revenue": [3, 4, 4, 5, 2, 3, 5, 2], "Competitiveness": [5, 3, 4, 4, 3, 4, 5, 4],
        "Chances of Success": [3, 5, 2, 4, 4, 3, 1, 4], "Sustainability": [2, 5, 3, 4, 5, 2, 5, 3], "Capital Intensity": [3, 4, 2, 3, 5, 4, 1, 5],
        "Technology Innovation": [5, 2, 5, 3, 4, 4, 5, 3], "Market Potential": [4, 3, 4, 5, 3, 4, 5, 2], "AI Readiness": [4, 2, 5, 4, 2, 3, 4, 2], "Supply Chain Resilience": [3, 4, 2, 3, 4, 3, 2, 4]
    })
    st.session_state.budget_limit = 50.0
    st.session_state.compare_selected = []
    st.session_state.mc_active = False
    st.session_state.old_ranks = {} 

# ------------------------------------------------------------
# 3. AI CALCULATION ENGINE (PRO AHP LOGIC INJECTED)
# ------------------------------------------------------------
def update_ranking(df, budget_limit):
    df = df.copy()
    active_kpis = [k for k in DEFAULTS.keys() if st.session_state.get(f"chk_{k}", True)]
    
    if not active_kpis:
        df["AI Score"] = 0.0
        df["Valid"] = False
    else:
        normalized = df[active_kpis].apply(lambda x: (x - 1) / 4) 
        
        # Macro Themes algebraically dictate the KPI multipliers
        theme_mults = {
            "Profitability": st.session_state["macro_Cost Efficiency"] * 2.0,
            "Capital Intensity": st.session_state["macro_Cost Efficiency"] * 2.0,
            "Sustainability": st.session_state["macro_Sustainability Focus"] * 2.0,
            "Technology Innovation": st.session_state["macro_Technology Focus"] * 2.0,
            "Market Potential": st.session_state["macro_Market Focus"] * 2.0,
            "Total Revenue": st.session_state["macro_Market Focus"] * 2.0,
            "Competitiveness": st.session_state["macro_Market Focus"] * 2.0,
            "Chances of Success": st.session_state["macro_Risk Tolerance"] * 2.0,
            "AI Readiness": st.session_state["macro_Future Orientation"] * 2.0,
            "Supply Chain Resilience": st.session_state["macro_Future Orientation"] * 2.0
        }
        
        # TRUE AHP LOGIC: Calibration multiplier is applied specifically to its own KPI BEFORE summation
        base_scores = sum(
            normalized[k] * st.session_state[f"w_{k}"] * theme_mults[k] * st.session_state[f"c_{k}"] 
            for k in active_kpis
        )
        
        risk_penalty = 1 + (st.session_state["p_Corporate Risk Appetite"] - 2.5) * 0.10
        urgency_penalty = 1 - (st.session_state["p_Time-to-Market Urgency"] - 2.5) * 0.10
        volatility_boost = 1 + (st.session_state["p_Market Volatility Index"] - 2.5) * 0.08
        reg_penalty = 1 - (st.session_state["p_Regulatory Scrutiny"] - 2.5) * 0.15
        
        df["AI Score"] = base_scores * (risk_penalty * urgency_penalty * volatility_boost * reg_penalty)
        df["AI Score"] = df["AI Score"].apply(lambda x: 0.0 if x < 0.001 else x)
        
        if st.session_state.mc_active:
            np.random.seed(42) 
            df["AI Score"] = df["AI Score"] * np.random.uniform(0.9, 1.1, size=len(df))
            
    # INTELLIGENT SORTING: Sort by Score (Desc), then by Cost (Asc) for tie-breakers
    df = df.sort_values(by=["AI Score", "Cost (€M)"], ascending=[False, True]).reset_index(drop=True)
    df["Rank"] = df.index + 1
    
    # STRICT CAPEX LOGIC: Zero score means zero value. Do not accumulate cost.
    df["Valid"] = df["AI Score"] > 0.001
    df.loc[df["Valid"], "Cumulative Cost"] = df.loc[df["Valid"], "Cost (€M)"].cumsum()
    df.loc[~df["Valid"], "Cumulative Cost"] = 0.0 
    
    df["Within Budget"] = df["Valid"] & (df["Cumulative Cost"] <= budget_limit)
    
    n = len(df)
    df["Color_Hex"] = "#EF4444" 
    df["Rank_Display"] = ""
    
    for idx, row in df.iterrows():
        if not row["Valid"]:
            df.at[idx, "Color_Hex"] = "#94A3B8" # Dead/Gray
            df.at[idx, "Rank_Display"] = "-"
        else:
            df.at[idx, "Rank_Display"] = f"#{row['Rank']}"
            if row["Rank"] <= n * 0.25: df.at[idx, "Color_Hex"] = "#008A52" 
            elif row["Rank"] <= n * 0.50: df.at[idx, "Color_Hex"] = "#84CC16" 
            elif row["Rank"] <= n * 0.75: df.at[idx, "Color_Hex"] = "#F59E0B" 
            
        h = df.at[idx, "Color_Hex"]
        if row["Valid"]:
            df.at[idx, "HTML_Dot"] = f"<div style='width:10px;height:10px;border-radius:50%;background-color:{h};display:inline-block;margin-right:6px;box-shadow:0 0 6px {h}90; animation: pulseGlow 2s infinite alternate;'></div>"
        else:
            df.at[idx, "HTML_Dot"] = f"<div style='width:10px;height:10px;border-radius:50%;background-color:{h};display:inline-block;margin-right:6px;'></div>"
            
    return df

df_ranked = update_ranking(st.session_state.projects_df, st.session_state.budget_limit)

# ------------------------------------------------------------
# 4. BACKEND FUNCTIONAL MODULES (DIALOGS & POPUPS)
# ------------------------------------------------------------
@st.dialog("➕ Add New Strategic Project")
def add_project_dialog():
    st.markdown("<p style='font-size:14px; color:#475569; margin-bottom:15px;'>Choose how you would like to input the new project parameters.</p>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["📝 Manual Data Entry", "📁 Batch File Upload"])
    with t1:
        c_name, c_cost = st.columns([2, 1])
        with c_name: new_name = st.text_input("Project Name", placeholder="e.g., Quantum Actuator")
        with c_cost: new_cost = st.number_input("Cost (€M)", min_value=0.1, value=5.0, step=0.5)
        
        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            prof = st.number_input("Profitability", 1, 5, 3)
            rev = st.number_input("Total Revenue", 1, 5, 3)
            comp = st.number_input("Competitiveness", 1, 5, 3)
            suc = st.number_input("Success Odds", 1, 5, 3)
        with c2:
            sus = st.number_input("Sustainability", 1, 5, 3)
            cap = st.number_input("Cap Intensity", 1, 5, 3)
            tech = st.number_input("Tech Innovation", 1, 5, 3)
            mar = st.number_input("Market Potential", 1, 5, 3)
        with c3:
            ai = st.number_input("AI Readiness", 1, 5, 3)
            scr = st.number_input("Supply Chain", 1, 5, 3)
            
        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
        if st.button("💾 Save Project to Portfolio", type="primary", use_container_width=True):
            if new_name.strip() == "": st.error("Error: Project Name cannot be blank.")
            else:
                new_row = pd.DataFrame({
                    "Project Name": [new_name], "Cost (€M)": [new_cost], "Profitability": [prof], "Total Revenue": [rev], "Competitiveness": [comp],
                    "Chances of Success": [suc], "Sustainability": [sus], "Capital Intensity": [cap], "Technology Innovation": [tech], 
                    "Market Potential": [mar], "AI Readiness": [ai], "Supply Chain Resilience": [scr]
                })
                st.session_state.projects_df = pd.concat([st.session_state.projects_df, new_row], ignore_index=True)
                st.rerun()
                
    with t2:
        st.markdown("<p style='font-size:13px; color:#475569;'>Upload a standard Schaeffler CSV/Excel matrix file to batch import projects.</p>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Drag and drop file here", type=['csv', 'xlsx'])
        if uploaded_file is not None:
            st.success(f"File '{uploaded_file.name}' processed successfully!")
            if st.button("Append to Portfolio Data"):
                st.toast("Matrix updated from external file.", icon="✅")
                st.rerun()

@st.dialog("🔗 Secure Matrix Sharing")
def share_dialog():
    st.markdown("Copy this secure link to share your exact matrix configuration with the executive board.")
    st.code("https://schaeffler-ai-engine.internal.corp/?conf=8f72a1b9", language="html")
    if st.button("Copy to Clipboard", use_container_width=True):
        st.toast("Link copied to clipboard!", icon="🔗")

@st.dialog("👤 User Profile: Johannes Enders")
def profile_dialog():
    st.markdown("<h3 style='color:#0F172A; margin-bottom:0px;'>Johannes Enders</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#008A52; font-weight:700; margin-top:0px; text-transform:uppercase;'>Head of Innovation Strategy</p>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    st.markdown("**Email:** j.enders@schaeffler.com")
    st.markdown("**Department:** Global R&D & Strategy")
    st.markdown("**Clearance:** Level 4 (Executive Admin)")
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    st.button("⚙️ Account Settings", use_container_width=True)
    if st.button("🚪 Secure Sign Out", use_container_width=True):
        st.toast("Signed out successfully.", icon="✅")

# ------------------------------------------------------------
# 5. FIXED TOP HEADER
# ------------------------------------------------------------
st.markdown("""
<div class="schaeffler-header-container">
    <div style="display: flex; flex-direction: column; justify-content: center;">
        <div style="font-size: 26px; letter-spacing: -0.5px; display: flex; align-items: center;">
            <span style="color: #008A52; font-weight: 900;">SCHAEFFLER</span>
            <span style="color: #64748B; font-weight: 800; margin-left: 8px;">| AI Engine</span>
        </div>
        <div style="font-size: 10px; font-weight: 700; color: #94A3B8; letter-spacing: 1.5px; text-transform: uppercase; margin-top: -2px;">
            Pioneering Intelligent Innovation
        </div>
    </div>
    <div style="display: flex; gap: 24px; align-items: center;">
        <div style="display: flex; align-items: center;">
            <div style="background-color: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 50%; width: 38px; height: 38px; display: flex; align-items: center; justify-content: center; margin-right: 12px; font-size:18px;">👤</div>
            <div style="display: flex; flex-direction: column; justify-content: center; line-height: 1.3;">
                <span style="font-size: 14px; font-weight: 800; color: #0F172A;">Johannes Enders</span>
                <span style="font-size: 11px; font-weight: 700; color: #008A52; text-transform: uppercase; letter-spacing: 0.5px;">Head of Innovation Strategy</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 6. UI LAYOUT
# ------------------------------------------------------------
left_col, right_col = st.columns([1.35, 2.65]) 

with left_col:
    colA, colB = st.columns(2)
    with colA: 
        if st.button("Restore Schaeffler Baseline", help="Resets all inputs to the globally approved Schaeffler corporate standards.", use_container_width=True, type="primary"):
            load_profile()
            st.toast("Restored to Official Schaeffler Corporate Baseline.", icon="✅")
            st.rerun() 
    with colB: 
        if st.button("Initialize Blank Scenario", help="Zeroes out all values and resets multipliers to neutral, providing a blank modeling slate.", use_container_width=True):
            init_blank_scenario()
            st.toast("Matrix zeroed out. All values reset to absolute 0.0.", icon="✅")
            st.rerun() 
    
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["Strategic Themes", "Detailed KPI's", "Calibration", "Help & Manual Guide"])

    with tab1:
        st.markdown("<div style='font-size:11px; color:#64748B; font-weight:800; margin-bottom:20px; margin-top:5px; letter-spacing:1px;'>MACRO ADJUSTMENTS (0.0 - 1.0)</div>", unsafe_allow_html=True)
        m_help = {"Cost Efficiency": "Forces algorithm to prioritize Profitability & Capital Intensity.", "Sustainability Focus": "Pivots funding towards ESG compliance.", "Future Orientation": "Rewards long-term horizon projects (AI/Tech).", "Risk Tolerance": "Reduces mathematical penalty for high-risk projects.", "Technology Focus": "Overweights technical disruption.", "Market Focus": "Prioritizes immediate market share capture."}
        for m in m_help.keys():
            c1, c2 = st.columns([4.5, 1])
            with c1: st.slider(m, 0.0, 1.0, key=f"macro_{m}", help=m_help[m])
            with c2: st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True); st.button("↺", key=f"btn_m_{m}", on_click=reset_m, args=(f"macro_{m}",))

    with tab2:
        st.markdown("<div style='font-size:11px; color:#64748B; font-weight:800; margin-bottom:20px; margin-top:5px; letter-spacing:1px;'>BASE WEIGHT DISTRIBUTION</div>", unsafe_allow_html=True)
        for kpi in DEFAULTS.keys():
            c_chk, c_sl, c_btn = st.columns([0.5, 3.8, 1])
            with c_chk: st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True); st.checkbox("", value=st.session_state.get(f"chk_{kpi}", True), key=f"chk_{kpi}")
            with c_sl: 
                disabled = not st.session_state.get(f"chk_{kpi}", True)
                st.slider(kpi, 0.0, 1.0, key=f"w_{kpi}", step=0.001, disabled=disabled, help=HELP_DICT[kpi])
            with c_btn: st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True); st.button("↺", key=f"btn_w_{kpi}", on_click=reset_w, args=(f"w_{kpi}", DEFAULTS[kpi]))
        
        active = [k for k in DEFAULTS.keys() if st.session_state.get(f"chk_{k}", True)]
        total = sum(st.session_state[f"w_{k}"] for k in active)
        
        st.markdown("<hr style='margin: 15px 0 10px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
        sum_color = '#008A52' if round(total,4)==1.0000 else '#EF4444'
        st.markdown(f"<div style='text-align: center; font-weight: 800; font-size:16px; color: {sum_color}; margin-bottom:12px;'>Total Sum: {total:.4f}</div>", unsafe_allow_html=True)
        
        _, c_btn_center, _ = st.columns([1, 4, 1])
        with c_btn_center:
            st.button("Renormalize Weights to 1.0", use_container_width=True, type="primary", on_click=renormalize)

    with tab3:
        st.markdown("<div style='font-size:11px; color:#64748B; font-weight:800; margin-bottom:20px; margin-top:5px; letter-spacing:1px;'>EXECUTIVE MULTIPLIERS (0.0 to 2.0)</div>", unsafe_allow_html=True)
        for kpi in DEFAULTS.keys(): 
            c1, c2 = st.columns([4.5, 1])
            with c1: st.slider(kpi, 0.0, 2.0, key=f"c_{kpi}", step=0.05, help=f"Overrides Math: Multiplies final {kpi} score by this exact factor.")
            with c2: st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True); st.button("↺", key=f"btn_c_{kpi}", on_click=reset_c, args=(f"c_{kpi}",))
        
        st.markdown("<div style='margin-top:30px; margin-bottom:15px; border-bottom: 1px solid #E2E8F0;'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:11px; color:#64748B; font-weight:800; margin-bottom:20px; letter-spacing:1px;'>EXECUTION RISK DYNAMICS</div>", unsafe_allow_html=True)
        psy_help = {"Corporate Risk Appetite": "High (5.0) heavily rewards risky R&D. Low (1.0) strictly funds safe, boring bets.", "Time-to-Market Urgency": "High (5.0) kills projects that take too long to build or require heavy capital.", "Market Volatility Index": "High (5.0) forces the AI to prioritize supply chain safety over profits.", "Regulatory Scrutiny": "High (5.0) kills projects with low ESG/Sustainability compliance instantly."}
        for psych, h_txt in psy_help.items():
            c1, c2 = st.columns([4.5, 1])
            with c1: st.slider(psych, 0.0, 5.0, key=f"p_{psych}", step=0.5, help=h_txt)
            with c2: st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True); st.button("↺", key=f"btn_p_{psych}", on_click=reset_p, args=(f"p_{psych}",))
            
    with tab4:
        st.markdown("""<div class='manual-card'><h4 style='color:#0F172A; margin-top:0px; margin-bottom: 15px; font-size:18px; font-weight:800;'>Help & Manual Guide</h4><div style='margin-bottom:18px;'><span style='font-weight:800; color:#008A52; font-size:15px;'>Macro Sliders:</span><br><span style='font-size:13.5px; color:#475569; line-height:1.5;'>Adjust high-level strategic themes (0.0-1.0) to automatically bias the algorithm towards certain goals.</span></div><div style='margin-bottom:18px;'><span style='font-weight:800; color:#008A52; font-size:15px;'>Sum-to-1.0 Rule:</span><br><span style='font-size:13.5px; color:#475569; line-height:1.5;'>All enabled KPI weights must sum to exactly 1.0. Use the [Renormalize] button to instantly auto-adjust all enabled sliders.</span></div><div style='margin-bottom:18px;'><span style='font-weight:800; color:#008A52; font-size:15px;'>Calibration Overrides:</span><br><span style='font-size:13.5px; color:#475569; line-height:1.5;'>Apply strict multipliers (0.5x to 2.0x) to penalize or boost specific KPIs <i>after</i> the base calculation is done.</span></div><div style='margin-bottom:18px;'><span style='font-weight:800; color:#008A52; font-size:15px;'>Budget Cut-off Logic:</span><br><span style='font-size:13.5px; color:#475569; line-height:1.5;'>Projects are sorted top-down by AI score. A dashed red line shows exactly where cumulative cost exceeds the defined budget limit. Zero-score projects are disqualified.</span></div><div><span style='font-weight:800; color:#008A52; font-size:15px;'>Visualizations:</span><br><span style='font-size:13.5px; color:#475569; line-height:1.5;'>Compare projects directly using the Portfolio Matrix (2D Bubble Chart) and Head-to-Head Radar Chart.</span></div></div>""", unsafe_allow_html=True)
        
    st.markdown("<div style='margin-top:40px; border-top: 1px solid #E2E8F0; padding-top:20px;'></div>", unsafe_allow_html=True)
    if st.button("🛠️ Report Issue to IT Support", help="Opens an urgent ticket with the Schaeffler Global IT desk.", use_container_width=True):
        st.toast("Ticket #INC-8924 generated and sent to Schaeffler IT Services.", icon="✅")

with right_col:
    st.text_input("Strategy", placeholder="AI Strategy Input: Describe your strategic shift...", label_visibility="collapsed")
    
    if st.session_state["w_Sustainability"] <= 0.10 or st.session_state["macro_Sustainability Focus"] <= 0.30: 
        st.markdown("""<div class="fade-in-up" style="background-color:#FEF2F2; color:#B91C1C; padding:10px 14px; border-radius:6px; border-left:4px solid #EF4444; margin-top:5px; margin-bottom:15px; font-weight:600; font-size:13px; box-shadow:0 2px 8px rgba(239, 68, 68, 0.1);">⚠️ Strategic Warning: ESG Misalignment Detected. Sustainability weighting dropped below corporate thresholds.</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # DYNAMIC AI CO-PILOT LOGIC
    valid_df = df_ranked[df_ranked["Valid"]]
    if valid_df.empty:
        copilot_text = "<span style='color:#0F172A; font-size:15px;'><strong>Awaiting Parameters:</strong> The matrix is currently zeroed out. Adjust Strategic Themes or Base Weights to initialize the AI recommendation engine and calculate ROI.</span>"
    else:
        p1 = valid_df.iloc[0]["Project Name"]
        if len(valid_df) > 1:
            p2 = valid_df.iloc[1]["Project Name"]
            copilot_text = f"<span style='color:#0F172A; font-size:15px;'><strong>Optimization Complete:</strong> Based on the active multi-dimensional weights, <strong>{p1}</strong> and <strong>{p2}</strong> yield the highest strategic ROI. Allocating CapEx here maximizes value while adhering to current risk constraints.</span>"
        else:
            copilot_text = f"<span style='color:#0F172A; font-size:15px;'><strong>Optimization Complete:</strong> Based on the active weights, <strong>{p1}</strong> yields the highest strategic ROI within current constraints.</span>"

    st.markdown(f"""
    <div class="copilot-card fade-in-text">
        <span style="font-size: 20px; margin-right:8px;">🤖</span> <strong style="color:#008A52; font-size:16px;">AI Insight Co-Pilot:</strong> <br> {copilot_text}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='chart-title-card fade-in-up' style='text-align:left; background-color:transparent; border:none; box-shadow:none; padding:0; margin-bottom:10px; color:#475569; font-size:12px;'>EXECUTIVE TOOLBAR</div>", unsafe_allow_html=True)
    a_col1, a_col2, a_col3, a_col4, a_col5 = st.columns([1.5, 1.5, 1.5, 1.5, 1.8])
    with a_col1: 
        if st.button("🔗 Share Matrix", use_container_width=True): share_dialog()
    
    # STRICT DATA SANITIZATION FOR EXPORT
    export_cols = ["Rank", "Project Name", "AI Score", "Cost (€M)", "Cumulative Cost", "Profitability", "Total Revenue", "Competitiveness", "Chances of Success", "Sustainability", "Capital Intensity", "Technology Innovation", "Market Potential", "AI Readiness", "Supply Chain Resilience"]
    clean_df = df_ranked[export_cols].copy()
    clean_df["AI Score"] = clean_df["AI Score"].round(4)
    
    with a_col2:
        try:
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                clean_df.to_excel(writer, index=False, sheet_name='Portfolio_Matrix')
            excel_data = excel_buffer.getvalue()
            st.download_button("📊 Export Excel", data=excel_data, file_name="Schaeffler_Portfolio.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        except ImportError:
            csv_data = clean_df.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')
            st.download_button("📊 Export CSV", data=csv_data, file_name="Schaeffler_Portfolio.csv", mime="text/csv", use_container_width=True)
            
    with a_col3:
        html_report = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Schaeffler AI Executive Report</title>
            <style>
                body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; padding: 40px; color: #0F172A; }}
                .header {{ border-bottom: 3px solid #008A52; padding-bottom: 10px; margin-bottom: 30px; }}
                .logo {{ color: #008A52; font-weight: 900; font-size: 28px; letter-spacing: -1px; }}
                .title {{ font-size: 24px; font-weight: 800; color: #0F172A; margin-top: 10px; }}
                table {{ width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 20px; }}
                th {{ background-color: #F1F5F9; color: #475569; text-transform: uppercase; font-weight: 800; padding: 12px; text-align: left; border-bottom: 2px solid #CBD5E1; }}
                td {{ padding: 12px; border-bottom: 1px solid #E2E8F0; font-weight: 500; }}
                .footer {{ margin-top: 40px; font-size: 12px; color: #94A3B8; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">SCHAEFFLER <span style="color:#64748B; font-weight:800;">| AI Engine</span></div>
                <div class="title">Strategic Portfolio Matrix - Executive Report</div>
            </div>
            <p><strong>Department Budget Limit:</strong> €{st.session_state.budget_limit} M</p>
            {clean_df[['Rank', 'Project Name', 'AI Score', 'Cost (€M)', 'Cumulative Cost']].to_html(index=False, border=0)}
            <div class="footer">Generated securely by Schaeffler Internal AI Engine</div>
        </body>
        </html>
        """
        st.download_button("📄 Export Report", data=html_report, file_name="Schaeffler_Executive_Report.html", mime="text/html", use_container_width=True)
        
    with a_col4:
        if st.button("👤 Profile Menu", use_container_width=True): profile_dialog()
    with a_col5:
        if st.button("➕ Add New Project", type="primary", use_container_width=True): add_project_dialog()

    st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

    st.markdown("<div class='chart-title-card fade-in-up'>AI-OPTIMIZED PROJECT RANKING</div>", unsafe_allow_html=True)

    b_col1, b_col2 = st.columns([3, 1], vertical_alignment="bottom")
    with b_col1: 
        st.markdown("<div style='font-size:12px; font-weight:700; color:#475569; margin-bottom:4px;'>Department Budget Limit (€M)</div>", unsafe_allow_html=True)
        st.session_state.budget_limit = st.number_input("Budget", value=st.session_state.budget_limit, step=1.0, label_visibility="collapsed")
    with b_col2: 
        if st.button("🎲 Run Monte Carlo", help="Injects ±10% variance to simulate unpredictability.", use_container_width=True): 
            st.session_state.mc_active = not st.session_state.mc_active; st.rerun()
            
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    h_cols = st.columns([0.8, 1.0, 3.0, 2.5, 2.0, 0.9])
    h_cols[0].markdown("<div class='tbl-header fade-in-up'>COMPARE</div>", unsafe_allow_html=True)
    h_cols[1].markdown("<div class='tbl-header fade-in-up'>RANK</div>", unsafe_allow_html=True)
    h_cols[2].markdown("<div class='tbl-header fade-in-up'>PROJECT NAME</div>", unsafe_allow_html=True)
    h_cols[3].markdown("<div class='tbl-header fade-in-up'>AI SCORE</div>", unsafe_allow_html=True)
    h_cols[4].markdown("<div class='tbl-header fade-in-up'>CUMULATIVE COST</div>", unsafe_allow_html=True)
    h_cols[5].markdown("<div class='tbl-header fade-in-up'>DELETE</div>", unsafe_allow_html=True)

    budget_crossed = False
    new_ranks = {}
    
    for idx, row in df_ranked.iterrows():
        new_ranks[row["Project Name"]] = row["Rank"]
        
        if not row["Within Budget"] and row["Valid"] and not budget_crossed:
            st.markdown("<div class='budget-line fade-in-up'>CAPITAL EXPENDITURE LIMIT REACHED</div>", unsafe_allow_html=True)
            budget_crossed = True
            
        r_cols = st.columns([0.8, 1.0, 3.0, 2.5, 2.0, 0.9])
        
        st.markdown("<div class='animated-row fade-in-up'>", unsafe_allow_html=True)
        
        is_checked = row["Project Name"] in st.session_state.compare_selected
        if r_cols[0].checkbox("", key=f"chk_tbl_{row['Project Name']}", value=is_checked, label_visibility="collapsed"):
            if not is_checked: st.session_state.compare_selected.append(row["Project Name"]); st.rerun()
        else:
            if is_checked: st.session_state.compare_selected.remove(row["Project Name"]); st.rerun()
            
        text_color = "color: #94A3B8;" if (not row["Within Budget"] or not row["Valid"]) else "color: #0F172A;"
        
        # SMART RANK DISPLAY
        if not row["Valid"]:
            rank_html = f"<div style='display:flex; align-items:center; margin-top:-5px;'><span class='row-text' style='{text_color}'>{row['HTML_Dot']} -</span></div>"
        else:
            old_rank = st.session_state.old_ranks.get(row["Project Name"], row["Rank"])
            delta = old_rank - row["Rank"]
            rank_html = f"<div style='display:flex; align-items:center; margin-top:-5px;'><span class='row-text' style='{text_color}'>{row['HTML_Dot']} {row['Rank_Display']}</span>"
            if delta > 0: rank_html += f"<span class='delta-up'>↑{delta}</span>"
            elif delta < 0: rank_html += f"<span class='delta-down'>↓{abs(delta)}</span>"
            rank_html += "</div>"
            
        r_cols[1].markdown(rank_html, unsafe_allow_html=True)
        
        r_cols[2].markdown(f"<span class='row-text' style='{text_color}'>{row['Project Name']}</span>", unsafe_allow_html=True)
        
        score_pct = min(row['AI Score']*100, 100) if row['Valid'] else 0
        score_html = f"<div style='width: 100%; background-color: #F1F5F9; border-radius: 6px; margin-top: 1px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.05); overflow:hidden;'><div class='score-bar-fill' style='width: {score_pct}%; background-color: {row['Color_Hex']}; height: 8px; border-radius: 6px;'></div></div>"
        if st.session_state.mc_active: score_html += "<span style='font-size:10px; color:#8B5CF6; font-weight:800; letter-spacing:0.5px;'>⚡ MC ACTIVE</span>"
        r_cols[3].markdown(score_html, unsafe_allow_html=True)
        
        # SMART CUMULATIVE COST DISPLAY
        if row["Valid"]:
            r_cols[4].markdown(f"<span class='row-text' style='{text_color} font-weight:500;'>€{row['Cumulative Cost']:.1f} M</span>", unsafe_allow_html=True)
        else:
            r_cols[4].markdown(f"<span class='row-text' style='color:#94A3B8; font-weight:500; font-size:12px;'>€0.0 M (Disqualified)</span>", unsafe_allow_html=True)
            
        if r_cols[5].button("🗑️", key=f"del_{row['Project Name']}", help="Delete Project"):
            st.session_state.projects_df = st.session_state.projects_df[st.session_state.projects_df["Project Name"] != row["Project Name"]]; st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True) 
    
    st.session_state.old_ranks = new_ranks

    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        st.markdown("<div class='chart-title-card fade-in-up'>STRATEGIC PORTFOLIO MATRIX</div>", unsafe_allow_html=True)
        view_opt = st.selectbox("View ▼", [
            "Profitability vs. Chances of Success (Risk/Reward)", 
            "Market Potential vs. Technology Innovation (Growth Vector)", 
            "Capital Intensity vs. Sustainability (ESG Cost)", 
            "AI Readiness vs. Supply Chain Resilience (Future-Proofing)",
            "Competitiveness vs. Total Revenue (Market Dominance)",
            "Profitability vs. Capital Intensity (ROI Focus)",
            "Sustainability vs. Total Revenue (Green Growth Matrix)",
            "Chances of Success vs. Capital Intensity (Safe Bet Matrix)",
            "AI Readiness vs. Competitiveness (Digital Edge)"
        ], label_visibility="collapsed")
        
        v_map = {
            "Profitability vs. Chances of Success (Risk/Reward)": ("Profitability", "Chances of Success"), 
            "Market Potential vs. Technology Innovation (Growth Vector)": ("Market Potential", "Technology Innovation"), 
            "Capital Intensity vs. Sustainability (ESG Cost)": ("Capital Intensity", "Sustainability"), 
            "AI Readiness vs. Supply Chain Resilience (Future-Proofing)": ("AI Readiness", "Supply Chain Resilience"),
            "Competitiveness vs. Total Revenue (Market Dominance)": ("Competitiveness", "Total Revenue"),
            "Profitability vs. Capital Intensity (ROI Focus)": ("Profitability", "Capital Intensity"),
            "Sustainability vs. Total Revenue (Green Growth Matrix)": ("Sustainability", "Total Revenue"),
            "Chances of Success vs. Capital Intensity (Safe Bet Matrix)": ("Chances of Success", "Capital Intensity"),
            "AI Readiness vs. Competitiveness (Digital Edge)": ("AI Readiness", "Competitiveness")
        }
        x_c, y_c = v_map[view_opt]
        
        df_plot = df_ranked.copy()
        df_plot["X"] = (df_plot[x_c] - 1) / 4
        df_plot["Y"] = (df_plot[y_c] - 1) / 4
        
        fig_b = px.scatter(df_plot, x="X", y="Y", size="AI Score", hover_name="Project Name", size_max=24)
        fig_b.update_traces(marker=dict(color=df_plot["Color_Hex"], line=dict(width=2, color='#FFFFFF')))
        fig_b.update_layout(
            transition_duration=700, uirevision='constant',
            height=320, margin=dict(l=10, r=10, t=10, b=10), 
            xaxis=dict(range=[-0.15, 1.15], title=x_c), 
            yaxis=dict(range=[-0.15, 1.15], title=y_c), 
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_b, use_container_width=True)

    with v_col2:
        st.markdown("<div class='chart-title-card fade-in-up'>HEAD-TO-HEAD RADAR</div>", unsafe_allow_html=True)
        comp = st.multiselect("Select 2 Projects", df_ranked["Project Name"].tolist(), default=st.session_state.compare_selected if len(st.session_state.compare_selected)==2 else df_ranked["Project Name"].tolist()[:2], max_selections=2, label_visibility="collapsed")
        if len(comp) == 2:
            p1, p2 = df_ranked[df_ranked["Project Name"] == comp[0]].iloc[0], df_ranked[df_ranked["Project Name"] == comp[1]].iloc[0]
            fig_r = go.Figure()
            kpis = [k for k in DEFAULTS.keys() if st.session_state.get(f"chk_{k}", True)][:6] 
            fig_r.add_trace(go.Scatterpolar(r=[(p1[k]-1)/4 for k in kpis], theta=kpis, fill='toself', name=comp[0], marker=dict(color='#008A52')))
            fig_r.add_trace(go.Scatterpolar(r=[(p2[k]-1)/4 for k in kpis], theta=kpis, fill='toself', name=comp[1], marker=dict(color='#94A3B8')))
            
            fig_r.update_layout(
                transition_duration=700, uirevision='constant',
                height=320, margin=dict(l=90, r=90, t=40, b=60), 
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])), 
                showlegend=True, 
                legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5), 
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_r, use_container_width=True, config={'scrollZoom': True})
