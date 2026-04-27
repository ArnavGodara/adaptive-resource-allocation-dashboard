# =============================================================================
# Adaptive Resource Allocation in Multiprogramming Systems
# ═══════════════════════════════════════════════════════════════════════════════
# ULTIMATE EDITION — Streamlit + Q-Learning RL + psutil + Rich PDF Report
# =============================================================================
# Run:
#   pip install streamlit psutil pandas numpy plotly reportlab
#   streamlit run app2.py
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import psutil
import random
import os
import pickle
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Adaptive Resource Allocator — Ultimate",
    layout="wide",
    page_icon="⚙️",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# PREMIUM CSS — Glassmorphism + Neon Glow + Animated Gradients
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ═══ GLOBAL ═══ */
    .stApp {
        background: linear-gradient(145deg, #060614 0%, #0a0a1f 30%, #0e0e2a 60%, #0a0a1f 100%);
        color: #e0e0f0;
        font-family: 'Inter', sans-serif;
    }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ═══ SIDEBAR ═══ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0c0c22 0%, #12123a 50%, #0c0c22 100%) !important;
        border-right: 1px solid rgba(100, 100, 255, 0.15);
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        background: linear-gradient(90deg, #00d4ff, #7c5cbf, #ff6bcb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: 0.5px;
    }

    /* ═══ METRIC CARDS — Glassmorphism ═══ */
    div[data-testid="metric-container"] {
        background: rgba(20, 20, 60, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(120, 120, 255, 0.15);
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    div[data-testid="metric-container"]:hover {
        border-color: rgba(0, 212, 255, 0.4);
        box-shadow: 0 4px 40px rgba(0, 212, 255, 0.1);
        transform: translateY(-2px);
    }
    div[data-testid="metric-container"] label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        white-space: nowrap;
        overflow: visible;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        white-space: nowrap;
        overflow: visible;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
        font-size: 0.7rem !important;
    }

    /* ═══ BUTTONS — Gradient Neon ═══ */
    .stButton > button {
        background: linear-gradient(135deg, #1a1a4e 0%, #2a1a5e 50%, #1a2a5e 100%);
        color: #e0e0ff;
        border: 1px solid rgba(100, 100, 255, 0.25);
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.85rem;
        width: 100%;
        padding: 0.5rem 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.3px;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2a2a6e 0%, #4a2a8e 50%, #2a4a8e 100%);
        border-color: rgba(0, 212, 255, 0.5);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.15), 0 0 40px rgba(124, 92, 191, 0.1);
        transform: translateY(-1px);
        color: #ffffff;
    }
    .stButton > button:active {
        transform: translateY(0px);
    }

    /* ═══ DATAFRAME ═══ */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(100, 100, 255, 0.12);
    }

    /* ═══ HEADERS ═══ */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }
    h1 { color: #e8e8ff !important; }
    h2 { color: #c8d8ff !important; }
    h3 { color: #a0b8e0 !important; }

    /* ═══ SELECTBOX ═══ */
    .stSelectbox > div > div {
        background-color: rgba(20, 20, 50, 0.7);
        border-color: rgba(100, 100, 255, 0.2);
        border-radius: 8px;
    }

    /* ═══ EXPANDER ═══ */
    .streamlit-expanderHeader {
        background: rgba(20, 20, 60, 0.4);
        border-radius: 10px;
        font-weight: 600;
    }

    /* ═══ CUSTOM SECTIONS ═══ */
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.85rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00d4ff 0%, #7c5cbf 40%, #ff6bcb 80%, #ffa94d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
        margin-bottom: 0;
        animation: gradientShift 4s ease-in-out infinite;
        background-size: 200% auto;
    }
    @keyframes gradientShift {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 100% center; }
    }

    .hero-subtitle {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #6a6a9a;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 2px;
    }

    .section-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: #8aa8d0;
        border-bottom: 1px solid rgba(100, 140, 255, 0.15);
        padding-bottom: 8px;
        margin-bottom: 14px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* ═══ ALERTS ═══ */
    .bottleneck-alert {
        background: linear-gradient(135deg, rgba(255,50,50,0.12), rgba(255,50,50,0.05));
        border: 1px solid rgba(255, 80, 80, 0.4);
        border-left: 4px solid #ff4444;
        border-radius: 10px;
        padding: 12px 20px;
        color: #ff9999;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        animation: alertPulse 2s ease-in-out infinite;
        backdrop-filter: blur(8px);
    }
    .stable-alert {
        background: linear-gradient(135deg, rgba(40,200,80,0.08), rgba(40,200,80,0.03));
        border: 1px solid rgba(80, 200, 100, 0.25);
        border-left: 4px solid #44cc66;
        border-radius: 10px;
        padding: 12px 20px;
        color: #88ddaa;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        backdrop-filter: blur(8px);
    }
    .info-alert {
        background: linear-gradient(135deg, rgba(0,180,255,0.08), rgba(0,180,255,0.03));
        border: 1px solid rgba(0, 180, 255, 0.25);
        border-left: 4px solid #00b4ff;
        border-radius: 10px;
        padding: 12px 20px;
        color: #88ccff;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        backdrop-filter: blur(8px);
    }
    @keyframes alertPulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 15px rgba(255, 50, 50, 0.1); }
        50% { opacity: 0.85; box-shadow: 0 0 25px rgba(255, 50, 50, 0.2); }
    }

    /* ═══ HEALTH SCORE BADGE ═══ */
    .health-badge {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.4rem;
        font-weight: 800;
        padding: 6px 18px;
        border-radius: 14px;
        text-align: center;
        min-width: 90px;
    }
    .health-excellent {
        color: #00ff88;
        background: rgba(0, 255, 136, 0.08);
        border: 2px solid rgba(0, 255, 136, 0.3);
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    }
    .health-good {
        color: #88dd44;
        background: rgba(136, 221, 68, 0.08);
        border: 2px solid rgba(136, 221, 68, 0.3);
        text-shadow: 0 0 20px rgba(136, 221, 68, 0.3);
    }
    .health-moderate {
        color: #ffc040;
        background: rgba(255, 192, 64, 0.08);
        border: 2px solid rgba(255, 192, 64, 0.3);
        text-shadow: 0 0 20px rgba(255, 192, 64, 0.3);
    }
    .health-critical {
        color: #ff5050;
        background: rgba(255, 80, 80, 0.08);
        border: 2px solid rgba(255, 80, 80, 0.3);
        text-shadow: 0 0 20px rgba(255, 80, 80, 0.3);
        animation: alertPulse 2s ease-in-out infinite;
    }

    /* ═══ PROGRESS BAR ═══ */
    .custom-progress-container {
        background: rgba(10, 10, 30, 0.6);
        border-radius: 8px;
        height: 10px;
        overflow: hidden;
        margin: 4px 0 8px 0;
        border: 1px solid rgba(100, 100, 255, 0.1);
    }
    .custom-progress-bar {
        height: 100%;
        border-radius: 8px;
        transition: width 0.5s ease;
    }
    .progress-cyan { background: linear-gradient(90deg, #00a8cc, #00d4ff); box-shadow: 0 0 10px rgba(0,212,255,0.3); }
    .progress-purple { background: linear-gradient(90deg, #7c4cbf, #b06aff); box-shadow: 0 0 10px rgba(176,106,255,0.3); }
    .progress-green { background: linear-gradient(90deg, #28a745, #51cf66); box-shadow: 0 0 10px rgba(81,207,102,0.3); }
    .progress-red { background: linear-gradient(90deg, #cc3333, #ff5555); box-shadow: 0 0 10px rgba(255,85,85,0.3); }
    .progress-orange { background: linear-gradient(90deg, #cc8800, #ffaa33); box-shadow: 0 0 10px rgba(255,170,51,0.3); }

    /* ═══ SCENARIO BUTTONS ═══ */
    .scenario-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #6a6a9a;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }

    /* ═══ TAB STYLING ═══ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(15, 15, 40, 0.5);
        border-radius: 10px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.82rem;
        color: #8888bb;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(40, 40, 100, 0.5);
        color: #00d4ff !important;
    }

    /* ═══ SEPARATOR ═══ */
    hr { border-color: rgba(100, 100, 255, 0.1) !important; }

    /* ═══ HIDE DEFAULT STREAMLIT ═══ */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
LOG_FILE    = "allocation_logs.csv"   # single active log file
MODEL_FILE  = "qtable.pkl"
MAX_PROC    = 8
MAX_HISTORY = 80

TOTAL_MEMORY_GB = psutil.virtual_memory().total / (1024 ** 3)

ACTION_LABELS = {
    0: "⏸ No Change",
    1: "⬆ Boost CPU",
    2: "⬆ Boost Memory",
    3: "⬇ Reduce CPU",
    4: "⬇ Reduce Memory",
}

PROCESS_NAMES = [
    "WebServer", "Compiler", "Database", "AI Trainer",
    "CacheEngine", "VideoRender", "BackupTask", "Analytics"
]

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────────────────
def _init_state():
    """Initialise all session state keys with defaults."""
    defaults = {
        "started":       False,
        "history":       [],
        "processes":     [],
        "qtable":        np.zeros((100, 5)),
        "mode":          "RL (Q-Learning)",
        "epsilon":       0.20,
        "alpha":         0.10,
        "step_count":    0,
        "last_action":   0,
        "last_reward":   0.0,
        "bottleneck":    False,
        "cumulative_reward": 0.0,
        "deadlock_flags": [],
        "health_score":  100,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ─────────────────────────────────────────────────────────────────────────────
# Q-LEARNING ENGINE (Enhanced)
# ─────────────────────────────────────────────────────────────────────────────
def encode_state(cpu, mem):
    """Map continuous CPU/MEM percentages into a discrete state index [0..99]."""
    c = min(int(cpu / 10), 9)
    m = min(int(mem / 10), 9)
    return c * 10 + m

def choose_action(cpu, mem):
    """Epsilon-greedy action selection from Q-table."""
    eps = st.session_state.epsilon
    s   = encode_state(cpu, mem)
    if random.random() < eps:
        return random.randint(0, 4)
    return int(np.argmax(st.session_state.qtable[s]))

def compute_reward(cpu, mem):
    """Custom reward function penalising bottlenecks and idle waste."""
    r  = -abs(cpu - 60) / 60
    r += -abs(mem - 60) / 60
    if cpu > 90 or mem > 90:
        r -= 5       # heavy bottleneck penalty
    if cpu < 10 or mem < 5:
        r -= 2       # idle waste penalty
    if 40 <= cpu <= 75 and 40 <= mem <= 75:
        r += 1.5     # bonus for ideal zone
    return round(r, 4)

def q_learn(cpu1, mem1, action, cpu2, mem2):
    """Update Q-table via Bellman equation with decaying alpha and epsilon."""
    q     = st.session_state.qtable
    alpha = st.session_state.alpha
    gamma = 0.9
    s     = encode_state(cpu1, mem1)
    s2    = encode_state(cpu2, mem2)
    r     = compute_reward(cpu2, mem2)
    q[s, action] += alpha * (r + gamma * np.max(q[s2]) - q[s, action])
    st.session_state.qtable = q
    # Decay epsilon (exploration → exploitation)
    st.session_state.epsilon = max(0.05, st.session_state.epsilon * 0.9995)
    # Decay alpha (learning rate annealing)
    st.session_state.alpha = max(0.01, st.session_state.alpha * 0.9998)
    return r

def save_model():
    """Persist Q-table to disk."""
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(st.session_state.qtable, f)

def load_model():
    """Load Q-table from disk if available."""
    if os.path.exists(MODEL_FILE):
        with open(MODEL_FILE, "rb") as f:
            st.session_state.qtable = pickle.load(f)
        return True
    return False

# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM HEALTH SCORE
# ─────────────────────────────────────────────────────────────────────────────
def compute_health(cpu, mem, reward_val):
    """Compute a composite system health score from 0-100."""
    cpu_score = max(0, 100 - abs(cpu - 55) * 1.8)
    mem_score = max(0, 100 - abs(mem - 55) * 1.8)
    rew_score = min(100, max(0, (reward_val + 3) * 25))
    # Weighted composite
    health = int(cpu_score * 0.35 + mem_score * 0.35 + rew_score * 0.30)
    return max(0, min(100, health))

def health_class(score):
    """Return CSS class for health badge."""
    if score >= 80: return "health-excellent"
    if score >= 60: return "health-good"
    if score >= 35: return "health-moderate"
    return "health-critical"

def health_label(score):
    """Return human-readable health label."""
    if score >= 80: return "EXCELLENT"
    if score >= 60: return "GOOD"
    if score >= 35: return "MODERATE"
    return "CRITICAL"

# ─────────────────────────────────────────────────────────────────────────────
# DEADLOCK DETECTION
# ─────────────────────────────────────────────────────────────────────────────
def detect_deadlocks():
    """Flag processes with near-zero CPU (starving) as potential deadlocks."""
    flags = []
    for p in st.session_state.processes:
        if p["cpu"] < 2 and p["state"] == "Running":
            flags.append(p["name"])
    st.session_state.deadlock_flags = flags
    return flags

# ─────────────────────────────────────────────────────────────────────────────
# PROCESS SIMULATOR
# ─────────────────────────────────────────────────────────────────────────────
def init_processes():
    """Create initial set of simulated processes."""
    plist = []
    for i in range(5):
        plist.append({
            "pid":       i + 1,
            "name":      PROCESS_NAMES[i],
            "cpu":       random.randint(5, 25),
            "mem_gb":    round(random.uniform(0.2, 1.5), 2),
            "priority":  random.randint(1, 5),
            "state":     "Running",
            "_cpu_trend": random.choice([-1, 0, 0, 1]),
            "_mem_trend": random.choice([-1, 0, 0, 1]),
        })
    st.session_state.processes = plist

def drift_processes():
    """Simulate natural resource fluctuation each tick."""
    for p in st.session_state.processes:
        p["cpu"]    = max(1,   min(50,  p["cpu"]    + p["_cpu_trend"] * random.uniform(0.5, 3) + random.uniform(-1, 1)))
        p["mem_gb"] = max(0.1, min(3.0, p["mem_gb"] + p["_mem_trend"] * random.uniform(0.02, 0.15) + random.uniform(-0.05, 0.05)))
        if random.random() < 0.04:
            p["_cpu_trend"] *= -1
        if random.random() < 0.04:
            p["_mem_trend"] *= -1

def apply_action_rl(action):
    """Apply RL-chosen action to the process pool."""
    plist = st.session_state.processes
    if not plist:
        return
    if action == 1:
        t = min(plist, key=lambda x: x["cpu"])
        t["cpu"] = min(50, t["cpu"] + random.uniform(3, 7))
    elif action == 2:
        t = min(plist, key=lambda x: x["mem_gb"])
        t["mem_gb"] = min(3.0, t["mem_gb"] + random.uniform(0.1, 0.3))
    elif action == 3:
        t = max(plist, key=lambda x: x["cpu"])
        t["cpu"] = max(1, t["cpu"] - random.uniform(3, 7))
    elif action == 4:
        t = max(plist, key=lambda x: x["mem_gb"])
        t["mem_gb"] = max(0.1, t["mem_gb"] - random.uniform(0.1, 0.3))

def apply_priority():
    """Boost the highest-priority process each step."""
    if not st.session_state.processes:
        return
    t = max(st.session_state.processes, key=lambda x: x["priority"])
    t["cpu"] = min(50, t["cpu"] + 3)

def get_totals():
    """Calculate aggregate CPU and memory utilisation percentages."""
    plist = st.session_state.processes
    if not plist:
        return 0.0, 0.0
    cpu = min(100, sum(p["cpu"] for p in plist))
    mem = min(100, sum(p["mem_gb"] for p in plist) / TOTAL_MEMORY_GB * 100)
    return round(cpu, 2), round(mem, 2)

# ─────────────────────────────────────────────────────────────────────────────
# SCENARIO PRESETS
# ─────────────────────────────────────────────────────────────────────────────
def apply_scenario(scenario):
    """Apply a predefined scenario to the process pool."""
    if not st.session_state.processes:
        init_processes()

    plist = st.session_state.processes
    if scenario == "heavy":
        for p in plist:
            p["cpu"] = random.uniform(30, 50)
            p["mem_gb"] = random.uniform(1.5, 3.0)
            p["_cpu_trend"] = 1
            p["_mem_trend"] = 1
    elif scenario == "idle":
        for p in plist:
            p["cpu"] = random.uniform(1, 8)
            p["mem_gb"] = random.uniform(0.1, 0.4)
            p["_cpu_trend"] = -1
            p["_mem_trend"] = -1
    elif scenario == "burst":
        for p in plist:
            p["cpu"] = random.choice([random.uniform(2, 10), random.uniform(35, 50)])
            p["mem_gb"] = random.choice([random.uniform(0.1, 0.5), random.uniform(2.0, 3.0)])
            p["_cpu_trend"] = random.choice([-1, 1])
            p["_mem_trend"] = random.choice([-1, 1])
    elif scenario == "balanced":
        for p in plist:
            p["cpu"] = random.uniform(10, 20)
            p["mem_gb"] = random.uniform(0.4, 1.0)
            p["_cpu_trend"] = 0
            p["_mem_trend"] = 0

# ─────────────────────────────────────────────────────────────────────────────
# SIMULATION STEP
# ─────────────────────────────────────────────────────────────────────────────
def simulate_step():
    """Run one simulation tick: drift processes, apply algorithm, log results."""
    drift_processes()

    cpu_before, mem_before = get_totals()
    mode   = st.session_state.mode
    action = 0
    rew    = 0.0

    if mode == "RL (Q-Learning)":
        action = choose_action(cpu_before, mem_before)
        apply_action_rl(action)
        cpu_after, mem_after = get_totals()
        rew = q_learn(cpu_before, mem_before, action, cpu_after, mem_after)
    elif mode == "Priority-Based":
        apply_priority()
        cpu_after, mem_after = get_totals()
        rew = compute_reward(cpu_after, mem_after)
    else:
        cpu_after, mem_after = cpu_before, mem_before
        rew = compute_reward(cpu_after, mem_after)

    # Real system metrics
    real_cpu = psutil.cpu_percent(interval=None)
    real_mem = psutil.virtual_memory().percent

    # Deadlock detection
    deadlocks = detect_deadlocks()

    # Health score
    health = compute_health(cpu_after, mem_after, rew)
    st.session_state.health_score = health

    st.session_state.last_action = action
    st.session_state.last_reward = rew
    st.session_state.step_count += 1
    st.session_state.bottleneck  = (cpu_after > 88 or mem_after > 88)
    st.session_state.cumulative_reward += rew

    row = {
        "step":     st.session_state.step_count,
        "time":     datetime.now().strftime("%H:%M:%S"),
        "sim_cpu":  cpu_after,
        "sim_mem":  mem_after,
        "real_cpu": real_cpu,
        "real_mem": real_mem,
        "action":   ACTION_LABELS[action],
        "reward":   rew,
        "cum_reward": st.session_state.cumulative_reward,
        "mode":     mode,
        "health":   health,
        "deadlocks": len(deadlocks),
    }
    st.session_state.history.append(row)
    if len(st.session_state.history) > MAX_HISTORY:
        st.session_state.history = st.session_state.history[-MAX_HISTORY:]

    pd.DataFrame(st.session_state.history).to_csv(LOG_FILE, index=False)

# ─────────────────────────────────────────────────────────────────────────────
# PDF REPORT GENERATOR (Rich)
# ─────────────────────────────────────────────────────────────────────────────
def export_pdf():
    """Generate a professional PDF report with executive summary, metrics, and recommendations."""
    doc  = SimpleDocTemplate("report.pdf", pagesize=A4,
                              leftMargin=2*cm, rightMargin=2*cm,
                              topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("title", parent=styles["Title"],
                                  fontSize=20, textColor=colors.HexColor("#0066cc"),
                                  alignment=TA_CENTER, spaceAfter=4)
    sub_style   = ParagraphStyle("sub", parent=styles["Normal"],
                                  fontSize=10, textColor=colors.HexColor("#666666"),
                                  alignment=TA_CENTER, spaceAfter=16)
    h2_style    = ParagraphStyle("h2", parent=styles["Heading2"],
                                  fontSize=13, textColor=colors.HexColor("#0066cc"),
                                  spaceBefore=14, spaceAfter=6)
    body_style  = ParagraphStyle("body", parent=styles["Normal"],
                                  fontSize=10, leading=14,
                                  textColor=colors.HexColor("#333333"))

    story = []

    # Title
    story.append(Paragraph("Adaptive Resource Allocation", title_style))
    story.append(Paragraph("Multiprogramming Systems — Performance Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0066cc")))
    story.append(Spacer(1, 14))

    hist = st.session_state.history

    # Executive Summary
    story.append(Paragraph("1. Executive Summary", h2_style))
    if hist:
        df  = pd.DataFrame(hist)
        avg_cpu = round(df["sim_cpu"].mean(), 2)
        avg_mem = round(df["sim_mem"].mean(), 2)
        avg_rew = round(df["reward"].mean(), 4)
        max_cpu = round(df["sim_cpu"].max(), 2)
        max_mem = round(df["sim_mem"].max(), 2)
        mode    = hist[-1]["mode"]
        steps   = st.session_state.step_count
        health  = st.session_state.health_score

        summary = (
            f"The system ran for <b>{steps} simulation steps</b> using the "
            f"<b>{mode}</b> algorithm. Average CPU utilisation was <b>{avg_cpu}%</b> "
            f"and average memory utilisation was <b>{avg_mem}%</b>. "
            f"The RL agent achieved an average reward of <b>{avg_rew}</b>. "
            f"System health score is <b>{health}/100</b> "
            f"({'Excellent' if health >= 80 else 'Good' if health >= 60 else 'Moderate' if health >= 35 else 'Critical'}). "
            f"Peak CPU reached {max_cpu}% and peak memory reached {max_mem}%."
        )
        story.append(Paragraph(summary, body_style))
    else:
        story.append(Paragraph("No simulation data available.", body_style))

    story.append(Spacer(1, 12))

    # Algorithm
    story.append(Paragraph("2. Algorithm Description", h2_style))
    algo_text = (
        "<b>Q-Learning (Reinforcement Learning):</b> The RL agent maintains a Q-table of "
        "100 states (10 CPU buckets × 10 Memory buckets) and 5 actions. It uses an "
        "epsilon-greedy strategy with both epsilon and learning rate (alpha) decaying over "
        "time. Epsilon decays from 0.20 to 0.05, alpha from 0.10 to 0.01. "
        "The reward function penalises bottlenecks (CPU/MEM &gt; 90%) and idle waste, "
        "while rewarding balanced utilisation in the 40–75% range.<br/><br/>"
        "<b>Priority-Based:</b> Allocates additional CPU to the highest-priority process "
        "each step.<br/><br/>"
        "<b>Static:</b> No reallocation — used as a baseline comparison."
    )
    story.append(Paragraph(algo_text, body_style))
    story.append(Spacer(1, 12))

    # Metrics Table
    if hist:
        story.append(Paragraph("3. Performance Metrics", h2_style))
        df = pd.DataFrame(hist)

        table_data = [
            ["Metric", "Min", "Max", "Average"],
            ["Simulated CPU (%)",
             str(round(df["sim_cpu"].min(), 2)),
             str(round(df["sim_cpu"].max(), 2)),
             str(round(df["sim_cpu"].mean(), 2))],
            ["Simulated Memory (%)",
             str(round(df["sim_mem"].min(), 2)),
             str(round(df["sim_mem"].max(), 2)),
             str(round(df["sim_mem"].mean(), 2))],
            ["Real CPU (%)",
             str(round(df["real_cpu"].min(), 2)),
             str(round(df["real_cpu"].max(), 2)),
             str(round(df["real_cpu"].mean(), 2))],
            ["Real Memory (%)",
             str(round(df["real_mem"].min(), 2)),
             str(round(df["real_mem"].max(), 2)),
             str(round(df["real_mem"].mean(), 2))],
            ["RL Reward",
             str(round(df["reward"].min(), 4)),
             str(round(df["reward"].max(), 4)),
             str(round(df["reward"].mean(), 4))],
            ["Health Score",
             str(round(df["health"].min(), 0)),
             str(round(df["health"].max(), 0)),
             str(round(df["health"].mean(), 1))],
        ]

        tbl = Table(table_data, colWidths=[5.5*cm, 3*cm, 3*cm, 3.5*cm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",  (0, 0), (-1, 0),  colors.HexColor("#0066cc")),
            ("TEXTCOLOR",   (0, 0), (-1, 0),  colors.white),
            ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",    (0, 0), (-1, -1), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.HexColor("#f0f4ff"), colors.white]),
            ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
            ("ALIGN",       (1, 0), (-1, -1), "CENTER"),
            ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",  (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING",(0,0), (-1, -1), 6),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 14))

        # Recommendations
        story.append(Paragraph("4. AI Recommendations", h2_style))
        recs = []
        if avg_cpu > 75:
            recs.append("• <b>High CPU</b>: Consider adding more processes or reducing per-process CPU allocation.")
        elif avg_cpu < 25:
            recs.append("• <b>Low CPU</b>: System under-utilised. Consolidate processes or increase workloads.")
        if avg_mem > 75:
            recs.append("• <b>High Memory</b>: Memory pressure detected. Scale up or optimise allocations.")
        elif avg_mem < 20:
            recs.append("• <b>Low Memory</b>: Memory is under-utilised. Consider allocating more to processes.")
        if avg_rew < -2:
            recs.append("• <b>Poor Reward</b>: RL agent struggling. Allow more training steps or reset epsilon.")
        if not recs:
            recs.append("• <b>System Optimal</b>: Resources are well balanced. No action required.")
        for rec in recs:
            story.append(Paragraph(rec, body_style))

        story.append(Spacer(1, 12))

        # Recent Log
        story.append(Paragraph("5. Recent Allocation Log (Last 10 Steps)", h2_style))
        recent = hist[-10:]
        log_data = [["Step", "Time", "CPU%", "Mem%", "Action", "Reward", "Health"]]
        for r in recent:
            log_data.append([
                str(r["step"]), r["time"],
                str(round(r["sim_cpu"], 1)), str(round(r["sim_mem"], 1)),
                r["action"], str(round(r["reward"], 3)), str(r["health"])
            ])
        ltbl = Table(log_data, colWidths=[1.5*cm, 2*cm, 1.8*cm, 1.8*cm, 4.2*cm, 2*cm, 1.7*cm])
        ltbl.setStyle(TableStyle([
            ("BACKGROUND",  (0, 0), (-1, 0),  colors.HexColor("#0066cc")),
            ("TEXTCOLOR",   (0, 0), (-1, 0),  colors.white),
            ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",    (0, 0), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.HexColor("#f0f4ff"), colors.white]),
            ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
            ("ALIGN",       (0, 0), (-1, -1), "CENTER"),
            ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",  (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING",(0,0), (-1, -1), 4),
        ]))
        story.append(ltbl)

    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Generated by Adaptive Resource Allocation System — Ultimate Edition | Q-Learning RL Engine",
        ParagraphStyle("footer", parent=styles["Normal"],
                       fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    ))

    doc.build(story)

# ─────────────────────────────────────────────────────────────────────────────
# CHART BUILDERS
# ─────────────────────────────────────────────────────────────────────────────
CHART_BG      = "#060614"
CHART_PLOT_BG = "#0a0a1f"
CHART_GRID    = "#141430"
CHART_FONT    = dict(color="#b0b0d0", size=11, family="Inter, sans-serif")

def build_main_chart(hist):
    """Build the primary CPU/Memory/Reward time-series chart."""
    df = pd.DataFrame(hist)
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=("CPU & Memory Utilisation", "RL Reward Over Time"),
        vertical_spacing=0.18,
        row_heights=[0.6, 0.4],
    )

    # Simulated CPU
    fig.add_trace(go.Scatter(
        x=df["step"], y=df["sim_cpu"],
        mode="lines", name="Sim CPU",
        line=dict(color="#00d4ff", width=2.5),
        fill="tozeroy", fillcolor="rgba(0,212,255,0.06)"
    ), row=1, col=1)

    # Simulated Memory
    fig.add_trace(go.Scatter(
        x=df["step"], y=df["sim_mem"],
        mode="lines", name="Sim Memory",
        line=dict(color="#b06aff", width=2.5),
        fill="tozeroy", fillcolor="rgba(176,106,255,0.06)"
    ), row=1, col=1)

    # Real CPU (dotted)
    fig.add_trace(go.Scatter(
        x=df["step"], y=df["real_cpu"],
        mode="lines", name="Real CPU",
        line=dict(color="#00d4ff", width=1.2, dash="dot"),
    ), row=1, col=1)

    # Real MEM (dotted)
    fig.add_trace(go.Scatter(
        x=df["step"], y=df["real_mem"],
        mode="lines", name="Real MEM",
        line=dict(color="#b06aff", width=1.2, dash="dot"),
    ), row=1, col=1)

    # Bottleneck threshold
    fig.add_hline(y=90, line_dash="dash", line_color="#ff4444",
                  opacity=0.5, row=1, col=1,
                  annotation_text="⚠ Bottleneck",
                  annotation_font_color="#ff6666",
                  annotation_font_size=10)

    # Reward
    fig.add_trace(go.Scatter(
        x=df["step"], y=df["reward"],
        mode="lines", name="Reward",
        line=dict(color="#51cf66", width=2),
        fill="tozeroy", fillcolor="rgba(81,207,102,0.06)"
    ), row=2, col=1)

    # Reward moving average
    if len(df) >= 5:
        df["reward_ma"] = df["reward"].rolling(window=5, min_periods=1).mean()
        fig.add_trace(go.Scatter(
            x=df["step"], y=df["reward_ma"],
            mode="lines", name="Reward MA(5)",
            line=dict(color="#ffa94d", width=2, dash="dash"),
        ), row=2, col=1)

    fig.add_hline(y=0, line_dash="dash", line_color="#ffa94d",
                  opacity=0.3, row=2, col=1)

    fig.update_layout(
        height=500,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_PLOT_BG,
        font=CHART_FONT,
        legend=dict(
            bgcolor="rgba(10,10,30,0.7)",
            bordercolor="rgba(100,100,255,0.15)",
            borderwidth=1,
            orientation="h", yanchor="bottom", y=1.03,
            font=dict(size=10)
        ),
        margin=dict(l=45, r=20, t=55, b=30),
    )
    fig.update_xaxes(gridcolor=CHART_GRID, zeroline=False)
    fig.update_yaxes(gridcolor=CHART_GRID, zeroline=False)
    return fig

def build_gauge(value, title, max_val=100, color_ranges=None):
    """Build a speedometer gauge chart."""
    if color_ranges is None:
        color_ranges = [
            {"range": [0, 40],    "color": "rgba(0,212,255,0.15)"},
            {"range": [40, 75],   "color": "rgba(81,207,102,0.15)"},
            {"range": [75, 90],   "color": "rgba(255,170,50,0.15)"},
            {"range": [90, 100],  "color": "rgba(255,80,80,0.15)"},
        ]

    bar_color = "#00d4ff"
    if value > 90:
        bar_color = "#ff5555"
    elif value > 75:
        bar_color = "#ffa94d"
    elif value > 40:
        bar_color = "#51cf66"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"size": 12, "color": "#8aa8d0", "family": "Inter"}},
        number={"suffix": "%", "font": {"size": 24, "color": "#e0e0ff", "family": "JetBrains Mono"}},
        gauge={
            "axis": {"range": [0, max_val], "tickcolor": "#4a4a7a", "tickwidth": 1,
                     "tickfont": {"size": 9, "color": "#6a6a9a"}},
            "bar": {"color": bar_color, "thickness": 0.3},
            "bgcolor": "rgba(10,10,30,0.3)",
            "borderwidth": 1,
            "bordercolor": "rgba(100,100,255,0.15)",
            "steps": color_ranges,
            "threshold": {
                "line": {"color": "#ff4444", "width": 2},
                "thickness": 0.8,
                "value": 90
            }
        }
    ))
    fig.update_layout(
        height=190,
        margin=dict(l=15, r=15, t=35, b=5),
        paper_bgcolor=CHART_BG,
        font=CHART_FONT,
    )
    return fig

def build_radar_chart(processes):
    """Build a radar chart showing each process's resource profile."""
    if not processes:
        return None

    categories = ["CPU %", "Memory", "Priority"]
    fig = go.Figure()

    palette = ["#00d4ff", "#b06aff", "#51cf66", "#ffa94d", "#ff6b6b",
               "#ff6bcb", "#00ff88", "#ffdd57"]

    for i, p in enumerate(processes):
        vals = [
            p["cpu"] / 50 * 100,
            p["mem_gb"] / 3.0 * 100,
            p["priority"] / 5 * 100,
        ]
        vals.append(vals[0])  # close the polygon
        fig.add_trace(go.Scatterpolar(
            r=vals,
            theta=categories + [categories[0]],
            name=f'{p["name"]} (P{p["pid"]})',
            line=dict(color=palette[i % len(palette)], width=2),
            fill="toself",
            fillcolor=palette[i % len(palette)].replace(")", ",0.08)").replace("rgb", "rgba"),
            opacity=0.85,
        ))

    fig.update_layout(
        polar=dict(
            bgcolor=CHART_PLOT_BG,
            radialaxis=dict(
                visible=True, range=[0, 100],
                gridcolor=CHART_GRID, linecolor=CHART_GRID,
                tickfont=dict(size=8, color="#6a6a9a"),
            ),
            angularaxis=dict(
                gridcolor=CHART_GRID, linecolor=CHART_GRID,
                tickfont=dict(size=10, color="#8aa8d0"),
            ),
        ),
        paper_bgcolor=CHART_BG,
        font=CHART_FONT,
        height=300,
        margin=dict(l=40, r=40, t=30, b=30),
        legend=dict(
            bgcolor="rgba(10,10,30,0.7)",
            bordercolor="rgba(100,100,255,0.15)",
            borderwidth=1,
            font=dict(size=9),
        ),
        showlegend=True,
    )
    return fig

def build_action_pie(hist):
    """Build a donut chart of RL action distribution."""
    df = pd.DataFrame(hist)
    counts = df["action"].value_counts().reset_index()
    counts.columns = ["action", "count"]
    fig = go.Figure(go.Pie(
        labels=counts["action"],
        values=counts["count"],
        hole=0.5,
        marker=dict(
            colors=["#00d4ff", "#51cf66", "#ffa94d", "#ff6b6b", "#b06aff"],
            line=dict(color=CHART_BG, width=2),
        ),
        textfont=dict(color="white", size=10),
        textinfo="percent+label",
        hoverinfo="label+value+percent",
    ))
    fig.update_layout(
        paper_bgcolor=CHART_BG,
        font=CHART_FONT,
        margin=dict(l=10, r=10, t=10, b=10),
        height=260,
        showlegend=False,
    )
    return fig

def build_per_process_chart(processes, hist):
    """Build a stacked area chart showing per-process CPU contributions over time."""
    if len(hist) < 2:
        return None

    fig = go.Figure()
    palette = ["#00d4ff", "#b06aff", "#51cf66", "#ffa94d", "#ff6b6b",
               "#ff6bcb", "#00ff88", "#ffdd57"]

    steps = [h["step"] for h in hist]

    for i, p in enumerate(processes):
        # Simulate a per-process contribution curve from the history
        base = p["cpu"]
        noise = np.random.normal(0, 1.5, len(steps))
        vals = np.clip(np.full(len(steps), base) + np.cumsum(noise * 0.3), 1, 50)
        vals = vals * (1 + np.random.uniform(-0.1, 0.1, len(steps)))

        fig.add_trace(go.Scatter(
            x=steps, y=vals.round(1),
            mode="lines",
            name=f'{p["name"]}',
            line=dict(width=0.5, color=palette[i % len(palette)]),
            stackgroup="one",
            fillcolor=palette[i % len(palette)].replace("ff", "40") if len(palette[i % len(palette)]) == 7 else palette[i % len(palette)],
        ))

    fig.update_layout(
        height=280,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_PLOT_BG,
        font=CHART_FONT,
        margin=dict(l=40, r=15, t=15, b=30),
        legend=dict(
            bgcolor="rgba(10,10,30,0.7)",
            bordercolor="rgba(100,100,255,0.15)",
            borderwidth=1,
            orientation="h", yanchor="bottom", y=1.02,
            font=dict(size=9),
        ),
        xaxis=dict(gridcolor=CHART_GRID),
        yaxis=dict(gridcolor=CHART_GRID, title="CPU %"),
    )
    return fig

def build_cumulative_reward_chart(hist):
    """Build cumulative reward chart showing learning progress."""
    df = pd.DataFrame(hist)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["step"], y=df["cum_reward"],
        mode="lines",
        name="Cumulative Reward",
        line=dict(color="#ffa94d", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(255,169,77,0.06)",
    ))

    fig.add_hline(y=0, line_dash="dash", line_color="#6a6a9a", opacity=0.5)

    fig.update_layout(
        height=220,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_PLOT_BG,
        font=CHART_FONT,
        margin=dict(l=45, r=15, t=15, b=30),
        xaxis=dict(gridcolor=CHART_GRID, title="Step"),
        yaxis=dict(gridcolor=CHART_GRID, title="Cumulative Reward"),
        showlegend=False,
    )
    return fig

def build_health_chart(hist):
    """Build health score timeline chart."""
    df = pd.DataFrame(hist)
    fig = go.Figure()

    # Color the line based on health value
    fig.add_trace(go.Scatter(
        x=df["step"], y=df["health"],
        mode="lines+markers",
        name="Health Score",
        line=dict(color="#00ff88", width=2),
        marker=dict(size=4, color=df["health"],
                    colorscale=[[0, "#ff4444"], [0.35, "#ffc040"], [0.6, "#88dd44"], [1, "#00ff88"]],
                    cmin=0, cmax=100),
        fill="tozeroy",
        fillcolor="rgba(0,255,136,0.04)",
    ))

    # Threshold lines
    fig.add_hline(y=80, line_dash="dot", line_color="#00ff88", opacity=0.3,
                  annotation_text="Excellent", annotation_font_color="#00ff88", annotation_font_size=9)
    fig.add_hline(y=60, line_dash="dot", line_color="#88dd44", opacity=0.3)
    fig.add_hline(y=35, line_dash="dot", line_color="#ffc040", opacity=0.3,
                  annotation_text="Moderate", annotation_font_color="#ffc040", annotation_font_size=9)

    fig.update_layout(
        height=220,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_PLOT_BG,
        font=CHART_FONT,
        margin=dict(l=45, r=15, t=15, b=30),
        xaxis=dict(gridcolor=CHART_GRID, title="Step"),
        yaxis=dict(gridcolor=CHART_GRID, title="Health Score", range=[0, 105]),
        showlegend=False,
    )
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: Render custom progress bar
# ─────────────────────────────────────────────────────────────────────────────
def progress_bar_html(value, max_val=100, color_class="progress-cyan"):
    """Return HTML for a custom animated progress bar."""
    pct = min(100, max(0, value / max_val * 100))
    return f"""
    <div class="custom-progress-container">
        <div class="custom-progress-bar {color_class}" style="width: {pct}%;"></div>
    </div>
    """

# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚡ Command Center")
    st.markdown("---")

    # Algorithm selector
    st.session_state.mode = st.selectbox(
        "🧠 Algorithm",
        ["RL (Q-Learning)", "Priority-Based", "Static (Baseline)"],
        index=["RL (Q-Learning)", "Priority-Based", "Static (Baseline)"].index(st.session_state.mode)
    )

    # Start / Stop
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("▶ Start", use_container_width=True):
            st.session_state.started = True
            if not st.session_state.processes:
                init_processes()
    with col_b:
        if st.button("⏹ Stop", use_container_width=True):
            st.session_state.started = False

    st.markdown("---")

    # Scenario Presets
    st.markdown('<div class="scenario-label">📋 Scenario Presets</div>', unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    with sc1:
        if st.button("🔥 Heavy Load"):
            if not st.session_state.processes:
                init_processes()
            apply_scenario("heavy")
            st.session_state.started = True
        if st.button("💤 Idle System"):
            if not st.session_state.processes:
                init_processes()
            apply_scenario("idle")
            st.session_state.started = True
    with sc2:
        if st.button("⚡ Burst Traffic"):
            if not st.session_state.processes:
                init_processes()
            apply_scenario("burst")
            st.session_state.started = True
        if st.button("⚖ Balanced"):
            if not st.session_state.processes:
                init_processes()
            apply_scenario("balanced")
            st.session_state.started = True

    st.markdown("---")

    # Process Management
    st.markdown('<div class="scenario-label">⚙️ Process Management</div>', unsafe_allow_html=True)
    pc1, pc2 = st.columns(2)
    with pc1:
        if st.button("➕ Add Process"):
            if len(st.session_state.processes) < MAX_PROC:
                st.session_state.processes.append({
                    "pid":       len(st.session_state.processes) + 1,
                    "name":      random.choice(PROCESS_NAMES),
                    "cpu":       random.randint(5, 20),
                    "mem_gb":    round(random.uniform(0.2, 1.0), 2),
                    "priority":  random.randint(1, 5),
                    "state":     "Running",
                    "_cpu_trend": random.choice([-1, 0, 1]),
                    "_mem_trend": random.choice([-1, 0, 1]),
                })
    with pc2:
        if st.button("➖ Remove Last"):
            if st.session_state.processes:
                st.session_state.processes.pop()

    st.markdown("---")

    # AI Model
    st.markdown('<div class="scenario-label">🤖 AI Model</div>', unsafe_allow_html=True)
    mc1, mc2 = st.columns(2)
    with mc1:
        if st.button("💾 Save"):
            save_model()
            st.success("Model saved!")
    with mc2:
        if st.button("📂 Load"):
            if load_model():
                st.success("Model loaded!")
            else:
                st.warning("No saved model.")

    st.markdown("---")

    # Reports
    st.markdown('<div class="scenario-label">📊 Reports</div>', unsafe_allow_html=True)
    if st.button("📄 Export PDF Report"):
        export_pdf()
        with open("report.pdf", "rb") as f:
            st.download_button("⬇ Download PDF", f, "report.pdf", "application/pdf")

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "rb") as f:
            st.download_button("⬇ Download CSV", f, "allocation_logs.csv", "text/csv")

    st.markdown("---")

    # Agent Status
    st.markdown('<div class="scenario-label">🧬 Agent Status</div>', unsafe_allow_html=True)

    eps_val = st.session_state.epsilon
    alpha_val = st.session_state.alpha
    st.markdown(f"**ε Exploration:** `{eps_val:.4f}`")
    st.markdown(progress_bar_html(eps_val, 0.20, "progress-cyan"), unsafe_allow_html=True)

    st.markdown(f"**α Learning Rate:** `{alpha_val:.4f}`")
    st.markdown(progress_bar_html(alpha_val, 0.10, "progress-purple"), unsafe_allow_html=True)

    st.markdown(f"**Steps:** `{st.session_state.step_count}`")
    st.markdown(f"**Cumulative Reward:** `{st.session_state.cumulative_reward:.2f}`")

    # Health badge in sidebar
    h = st.session_state.health_score
    st.markdown(f"""
    <div style="text-align:center; margin-top:10px;">
        <div class="health-badge {health_class(h)}">{h}</div>
        <div style="color:#6a6a9a; font-size:0.7rem; margin-top:4px; font-family:'JetBrains Mono';">
            HEALTH — {health_label(h)}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# MAIN DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════

# ── HERO HEADER (static — outside fragment so it never flickers) ────────────
st.markdown("""
<div style="margin-bottom: 4px;">
    <div class="hero-title">⚙️ Adaptive Resource Allocation Dashboard</div>
    <div class="hero-subtitle">Multiprogramming System • Q-Learning RL Engine • Real-Time Monitoring</div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# ─────────────────────────────────────────────────────────────────────────────
# FRAGMENT — Only this section re-renders on each tick (no full page flicker)
# ─────────────────────────────────────────────────────────────────────────────
_refresh_interval = timedelta(seconds=1.5) if st.session_state.started else None

@st.fragment(run_every=_refresh_interval)
def live_dashboard():
    """The main live dashboard fragment. Re-runs every 1.5s when simulation is active."""

    # Run one simulation tick if active
    if st.session_state.started:
        simulate_step()

    # ── GAUGE + HEALTH ROW ────────────────────────────────────────────────────
    sim_cpu, sim_mem = get_totals()
    real_cpu = psutil.cpu_percent(interval=None)
    real_mem = psutil.virtual_memory().percent
    hist     = st.session_state.history
    h_score  = st.session_state.health_score

    g1, g2, g3, g4 = st.columns([1, 1, 1, 1])

    with g1:
        st.plotly_chart(build_gauge(sim_cpu, "SIM CPU"), use_container_width=True, config={'displayModeBar': False})
    with g2:
        st.plotly_chart(build_gauge(sim_mem, "SIM MEMORY"), use_container_width=True, config={'displayModeBar': False})
    with g3:
        st.plotly_chart(build_gauge(real_cpu, "REAL CPU"), use_container_width=True, config={'displayModeBar': False})
    with g4:
        st.plotly_chart(build_gauge(real_mem, "REAL RAM"), use_container_width=True, config={'displayModeBar': False})

    # ── METRIC CARDS ─────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    delta_cpu = sim_cpu - (hist[-2]['sim_cpu'] if len(hist)>1 else sim_cpu)
    delta_mem = sim_mem - (hist[-2]['sim_mem'] if len(hist)>1 else sim_mem)
    m1.metric("Sim CPU",      f"{sim_cpu:.1f}%", delta=f"{delta_cpu:+.1f}%")
    m2.metric("Sim Memory",   f"{sim_mem:.1f}%", delta=f"{delta_mem:+.1f}%")
    m3.metric("RL Reward",    f"{st.session_state.last_reward:.3f}")
    m4.metric("Processes",    f"{len(st.session_state.processes)} active")

    m5, m6, m7, m8 = st.columns(4)
    m5.metric("Real CPU",     f"{real_cpu:.1f}%")
    m6.metric("Real RAM",     f"{real_mem:.1f}%")
    m7.metric("Health Score", f"{h_score}/100")
    m8.metric("Total Steps",  st.session_state.step_count)

    # ── ALERTS ───────────────────────────────────────────────────────────
    if st.session_state.bottleneck:
        st.markdown('<div class="bottleneck-alert">⚠️ BOTTLENECK DETECTED — RL Agent is actively reallocating resources to stabilise the system...</div>',
                    unsafe_allow_html=True)
    elif st.session_state.deadlock_flags:
        st.markdown(f'<div class="info-alert">🔒 POTENTIAL DEADLOCK — Starving processes: {", ".join(st.session_state.deadlock_flags)}</div>',
                    unsafe_allow_html=True)
    elif st.session_state.started:
        st.markdown(f'<div class="stable-alert">✅ System Stable — {ACTION_LABELS[st.session_state.last_action]} • {st.session_state.mode} • Health: {h_score}/100</div>',
                    unsafe_allow_html=True)

    st.markdown("")

    # ── MAIN CONTENT — TABS ──────────────────────────────────────────────────
    tab_live, tab_processes, tab_analytics, tab_brain = st.tabs([
        "📊 Live Performance", "🗂 Processes", "📈 Analytics", "🧠 RL Brain"
    ])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 1: LIVE PERFORMANCE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_live:
        if hist:
            st.plotly_chart(build_main_chart(hist), use_container_width=True, config={'displayModeBar': False})

            lc1, lc2 = st.columns(2)
            with lc1:
                st.markdown('<div class="section-title">🏥 System Health Score</div>', unsafe_allow_html=True)
                st.plotly_chart(build_health_chart(hist), use_container_width=True, config={'displayModeBar': False})
            with lc2:
                st.markdown('<div class="section-title">📈 Cumulative Reward (Learning Progress)</div>', unsafe_allow_html=True)
                st.plotly_chart(build_cumulative_reward_chart(hist), use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown('<div class="info-alert">ℹ️ Click ▶ Start in the sidebar to begin the simulation and see live charts.</div>',
                        unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 2: PROCESSES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_processes:
        pc1, pc2 = st.columns([3, 2])

        with pc1:
            st.markdown('<div class="section-title">📋 Running Processes</div>', unsafe_allow_html=True)
            if st.session_state.processes:
                display_cols = ["pid", "name", "cpu", "mem_gb", "priority", "state"]
                df_show = pd.DataFrame(st.session_state.processes)[display_cols].copy()
                df_show.columns = ["PID", "Name", "CPU %", "Mem GB", "Priority", "State"]
                df_show["CPU %"]  = df_show["CPU %"].round(1)
                df_show["Mem GB"] = df_show["Mem GB"].round(2)
                st.dataframe(df_show, use_container_width=True, height=300)

                # Per-process CPU overview bars
                st.markdown('<div class="section-title">⚡ Per-Process CPU Load</div>', unsafe_allow_html=True)
                for p in st.session_state.processes:
                    cpu_pct = min(100, p["cpu"] / 50 * 100)
                    color = "progress-green" if cpu_pct < 50 else "progress-orange" if cpu_pct < 80 else "progress-red"
                    st.markdown(f'**{p["name"]}** (PID {p["pid"]}) — `{p["cpu"]:.1f}%`')
                    st.markdown(progress_bar_html(cpu_pct, 100, color), unsafe_allow_html=True)
            else:
                st.markdown('<div class="info-alert">ℹ️ No processes running. Click ▶ Start to initialise.</div>',
                            unsafe_allow_html=True)

        with pc2:
            st.markdown('<div class="section-title">🕸 Resource Radar</div>', unsafe_allow_html=True)
            if st.session_state.processes:
                radar = build_radar_chart(st.session_state.processes)
                if radar:
                    st.plotly_chart(radar, use_container_width=True, config={'displayModeBar': False})

            st.markdown('<div class="section-title">🎯 Action Distribution</div>', unsafe_allow_html=True)
            if hist:
                st.plotly_chart(build_action_pie(hist), use_container_width=True, config={'displayModeBar': False})

        # Stacked area
        if hist and st.session_state.processes:
            st.markdown('<div class="section-title">📊 Per-Process CPU Contribution (Stacked)</div>', unsafe_allow_html=True)
            stacked = build_per_process_chart(st.session_state.processes, hist)
            if stacked:
                st.plotly_chart(stacked, use_container_width=True, config={'displayModeBar': False})

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 3: ANALYTICS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_analytics:
        if hist:
            df_hist = pd.DataFrame(hist)

            # Summary metrics
            st.markdown('<div class="section-title">📊 Performance Summary</div>', unsafe_allow_html=True)
            a1, a2, a3, a4, a5, a6 = st.columns(6)
            a1.metric("Avg CPU %",      f"{df_hist['sim_cpu'].mean():.2f}")
            a2.metric("Avg Mem %",      f"{df_hist['sim_mem'].mean():.2f}")
            a3.metric("Avg Reward",     f"{df_hist['reward'].mean():.3f}")
            a4.metric("Peak CPU %",     f"{df_hist['sim_cpu'].max():.1f}")
            a5.metric("Best Reward",    f"{df_hist['reward'].max():.3f}")
            a6.metric("Avg Health",     f"{df_hist['health'].mean():.0f}")

            st.markdown("")

            # Resource utilisation overview
            st.markdown('<div class="section-title">⚡ Resource Utilisation Overview</div>', unsafe_allow_html=True)

            avg_cpu = df_hist['sim_cpu'].mean()
            avg_mem = df_hist['sim_mem'].mean()
            max_cpu = df_hist['sim_cpu'].max()
            max_mem = df_hist['sim_mem'].max()

            ov1, ov2 = st.columns(2)
            with ov1:
                st.markdown(f"**Average CPU:** `{avg_cpu:.1f}%`")
                cpu_color = "progress-green" if avg_cpu < 60 else "progress-orange" if avg_cpu < 85 else "progress-red"
                st.markdown(progress_bar_html(avg_cpu, 100, cpu_color), unsafe_allow_html=True)

                st.markdown(f"**Peak CPU:** `{max_cpu:.1f}%`")
                cpu_pk_color = "progress-green" if max_cpu < 60 else "progress-orange" if max_cpu < 85 else "progress-red"
                st.markdown(progress_bar_html(max_cpu, 100, cpu_pk_color), unsafe_allow_html=True)

            with ov2:
                st.markdown(f"**Average Memory:** `{avg_mem:.1f}%`")
                mem_color = "progress-purple" if avg_mem < 60 else "progress-orange" if avg_mem < 85 else "progress-red"
                st.markdown(progress_bar_html(avg_mem, 100, mem_color), unsafe_allow_html=True)

                st.markdown(f"**Peak Memory:** `{max_mem:.1f}%`")
                mem_pk_color = "progress-purple" if max_mem < 60 else "progress-orange" if max_mem < 85 else "progress-red"
                st.markdown(progress_bar_html(max_mem, 100, mem_pk_color), unsafe_allow_html=True)

            st.markdown("")

            # Recent log
            st.markdown('<div class="section-title">📝 Recent Allocation Log</div>', unsafe_allow_html=True)
            recent_df = df_hist[["step", "time", "sim_cpu", "sim_mem", "real_cpu", "real_mem", "action", "reward", "health"]].tail(15)
            recent_df.columns = ["Step", "Time", "Sim CPU%", "Sim Mem%", "Real CPU%", "Real Mem%", "Action", "Reward", "Health"]
            st.dataframe(recent_df, use_container_width=True, height=350)
        else:
            st.markdown('<div class="info-alert">ℹ️ Run the simulation to see analytics data.</div>',
                        unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 4: RL BRAIN
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_brain:
        bc1, bc2 = st.columns([2, 1])

        with bc1:
            st.markdown('<div class="section-title">🧠 Q-Table Heatmap (Agent Knowledge)</div>', unsafe_allow_html=True)
            q = st.session_state.qtable
            fig_q = go.Figure(go.Heatmap(
                z=q,
                colorscale=[
                    [0.0, "#0a0a2e"],
                    [0.25, "#1a1a6e"],
                    [0.5, "#4a2a8e"],
                    [0.75, "#8a4abe"],
                    [1.0, "#ff6bcb"],
                ],
                colorbar=dict(
                    title=dict(text="Q-Value", font=dict(color="#8aa8d0")),
                    tickfont=dict(color="#6a6a9a"),
                ),
            ))
            fig_q.update_layout(
                xaxis_title="Action (0=None 1=↑CPU 2=↑Mem 3=↓CPU 4=↓Mem)",
                yaxis_title="State (CPU×10 + Mem bucket)",
                paper_bgcolor=CHART_BG,
                plot_bgcolor=CHART_PLOT_BG,
                font=CHART_FONT,
                height=420,
                margin=dict(l=60, r=20, t=20, b=50),
            )
            st.plotly_chart(fig_q, use_container_width=True, config={'displayModeBar': False})

        with bc2:
            st.markdown('<div class="section-title">📊 Agent Statistics</div>', unsafe_allow_html=True)

            # Q-table stats
            q_nonzero = np.count_nonzero(q)
            q_max     = q.max()
            q_min     = q.min()
            q_mean    = q[q != 0].mean() if q_nonzero > 0 else 0

            st.metric("States Explored", f"{q_nonzero} / {q.size}")
            st.markdown(progress_bar_html(q_nonzero, q.size, "progress-cyan"), unsafe_allow_html=True)

            st.metric("Max Q-Value", f"{q_max:.4f}")
            st.metric("Min Q-Value", f"{q_min:.4f}")
            st.metric("Mean Q-Value (non-zero)", f"{q_mean:.4f}")

            st.markdown("")
            st.markdown('<div class="section-title">🎛 Hyperparameters</div>', unsafe_allow_html=True)
            st.markdown(f"**ε (Exploration):** `{st.session_state.epsilon:.4f}`")
            st.markdown(f"**α (Learning Rate):** `{st.session_state.alpha:.4f}`")
            st.markdown(f"**γ (Discount):** `0.9000`")
            st.markdown(f"**States:** `100` (10×10)")
            st.markdown(f"**Actions:** `5`")

            # Best action per state analysis
            if q_nonzero > 0:
                st.markdown("")
                st.markdown('<div class="section-title">🏆 Preferred Actions</div>', unsafe_allow_html=True)
                best_actions = np.argmax(q, axis=1)
                action_counts = pd.Series(best_actions).value_counts().sort_index()
                for act_id, count in action_counts.items():
                    st.markdown(f"`{ACTION_LABELS[act_id]}` — {count} states")

# ─────────────────────────────────────────────────────────────────────────────
# INVOKE THE LIVE DASHBOARD FRAGMENT
# ─────────────────────────────────────────────────────────────────────────────
live_dashboard()
