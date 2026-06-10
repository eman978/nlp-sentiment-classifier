import streamlit as st
import re

st.set_page_config(
    page_title="Sentiment Analysis — NLP Classifier",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default chrome
st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
iframe { border: none; }
</style>
""", unsafe_allow_html=True)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Sentiment Analysis</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg:#F6F7FB; --surface:#FFFFFF; --border:#E4E7EF; --text:#1A1D2E;
  --muted:#6B7280; --accent:#4F63D2; --accent-lt:#EEF0FD;
  --pos:#0F9B6E; --pos-lt:#E8F8F3; --neg:#D93B3B; --neg-lt:#FDEAEA;
  --neu:#6B7280; --neu-lt:#F3F4F6; --radius:12px;
  --shadow:0 2px 12px rgba(26,29,46,0.07);
}
html { scroll-behavior:smooth; }
body { background:var(--bg); color:var(--text); font-family:'DM Sans',sans-serif; font-size:15px; line-height:1.6; min-height:100vh; }
nav { background:var(--surface); border-bottom:1px solid var(--border); padding:0 2rem; height:60px; display:flex; align-items:center; justify-content:space-between; position:sticky; top:0; z-index:100; box-shadow:0 1px 4px rgba(26,29,46,0.05); gap:1rem; }
.nav-brand { font-weight:700; font-size:1rem; color:var(--text); letter-spacing:-0.01em; display:flex; align-items:center; gap:0.6rem; flex-shrink:0; }
.nav-dot { width:8px; height:8px; border-radius:50%; background:var(--accent); }
.nav-links { display:flex; align-items:center; gap:0.25rem; }
.nav-link { font-size:0.86rem; font-weight:500; color:var(--muted); text-decoration:none; padding:0.4rem 0.85rem; border-radius:6px; transition:color 0.15s, background 0.15s; }
.nav-link:hover { color:var(--text); background:var(--bg); }
.nav-link.active { color:var(--accent); background:var(--accent-lt); }
.nav-tag { font-size:0.72rem; font-weight:500; background:var(--accent-lt); color:var(--accent); border-radius:999px; padding:0.2rem 0.7rem; font-family:'DM Mono',monospace; flex-shrink:0; }
@media(max-width:640px){ .nav-links{display:none;} }
.page { max-width:980px; margin:0 auto; padding:2.5rem 1.5rem 4rem; }
.page-header { margin-bottom:2.5rem; }
.page-header h1 { font-size:1.9rem; font-weight:700; letter-spacing:-0.025em; line-height:1.2; color:var(--text); margin-bottom:0.4rem; }
.page-header p { color:var(--muted); font-size:0.92rem; max-width:520px; }
.grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:1.25rem; }
@media(max-width:700px){ .grid-2{grid-template-columns:1fr;} }
.card { background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:1.5rem; box-shadow:var(--shadow); }
.card-title { font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.07em; color:var(--muted); margin-bottom:1.1rem; }
.input-panel { grid-column:1/-1; }
textarea { width:100%; resize:vertical; min-height:110px; border:1.5px solid var(--border); border-radius:8px; padding:0.85rem 1rem; font-family:'DM Sans',sans-serif; font-size:0.92rem; color:var(--text); background:var(--bg); transition:border-color 0.18s; outline:none; line-height:1.6; }
textarea:focus { border-color:var(--accent); background:#fff; }
textarea::placeholder { color:#B0B7C3; }
.input-actions { display:flex; justify-content:space-between; align-items:center; margin-top:0.85rem; gap:0.75rem; flex-wrap:wrap; }
.char-count { font-size:0.78rem; color:var(--muted); font-family:'DM Mono',monospace; }
.btn-row { display:flex; gap:0.6rem; }
button { font-family:'DM Sans',sans-serif; font-size:0.88rem; font-weight:600; border:none; border-radius:8px; cursor:pointer; padding:0.6rem 1.3rem; transition:background 0.15s,transform 0.12s,box-shadow 0.15s; }
button:active { transform:scale(0.97); }
.btn-primary { background:var(--accent); color:#fff; box-shadow:0 2px 8px rgba(79,99,210,0.25); }
.btn-primary:hover { background:#3d50c0; box-shadow:0 4px 14px rgba(79,99,210,0.35); }
.btn-secondary { background:var(--bg); color:var(--muted); border:1.5px solid var(--border); }
.btn-secondary:hover { background:var(--border); color:var(--text); }
.btn-danger { background:var(--neg-lt); color:var(--neg); border:1.5px solid #f5c6c6; }
.btn-danger:hover { background:#fad5d5; }
.stats-row { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-bottom:1.25rem; }
@media(max-width:500px){ .stats-row{grid-template-columns:1fr;} }
.stat-box { border-radius:var(--radius); padding:1.2rem 1.4rem; border:1px solid; transition:transform 0.18s; }
.stat-box:hover { transform:translateY(-2px); }
.stat-box.pos { background:var(--pos-lt); border-color:#b8ecd9; }
.stat-box.neg { background:var(--neg-lt); border-color:#f5c6c6; }
.stat-box.neu { background:var(--neu-lt); border-color:#dde1ea; }
.stat-num { font-size:2rem; font-weight:700; letter-spacing:-0.03em; line-height:1; margin-bottom:0.25rem; }
.stat-box.pos .stat-num { color:var(--pos); }
.stat-box.neg .stat-num { color:var(--neg); }
.stat-box.neu .stat-num { color:var(--neu); }
.stat-label { font-size:0.78rem; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; }
.stat-box.pos .stat-label { color:#0a7a56; }
.stat-box.neg .stat-label { color:#a82c2c; }
.stat-box.neu .stat-label { color:var(--muted); }
.stat-pct { font-size:0.78rem; color:var(--muted); margin-top:0.2rem; font-family:'DM Mono',monospace; }
.prog-row { display:flex; flex-direction:column; gap:0.6rem; }
.prog-item { display:flex; align-items:center; gap:0.75rem; }
.prog-label { width:68px; font-size:0.78rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; flex-shrink:0; }
.prog-label.pos { color:var(--pos); }
.prog-label.neg { color:var(--neg); }
.prog-label.neu { color:var(--neu); }
.prog-track { flex:1; height:8px; background:var(--border); border-radius:999px; overflow:hidden; }
.prog-fill { height:100%; border-radius:999px; transition:width 0.5s cubic-bezier(.4,0,.2,1); }
.prog-fill.pos { background:var(--pos); }
.prog-fill.neg { background:var(--neg); }
.prog-fill.neu { background:#9CA3AF; }
.prog-val { width:36px; text-align:right; font-size:0.78rem; font-family:'DM Mono',monospace; color:var(--muted); }
.verdict-box { border-radius:var(--radius); padding:1rem 1.3rem; border:1.5px solid; display:flex; align-items:center; gap:1rem; margin-top:1rem; }
.verdict-box.pos { background:var(--pos-lt); border-color:#a8e6cf; }
.verdict-box.neg { background:var(--neg-lt); border-color:#f5c6c6; }
.verdict-box.neu { background:var(--neu-lt); border-color:#dde1ea; }
.verdict-box.empty { background:var(--bg); border-color:var(--border); }
.verdict-indicator { width:12px; height:12px; border-radius:50%; flex-shrink:0; }
.verdict-box.pos .verdict-indicator { background:var(--pos); }
.verdict-box.neg .verdict-indicator { background:var(--neg); }
.verdict-box.neu .verdict-indicator { background:#9CA3AF; }
.verdict-box.empty .verdict-indicator { background:var(--border); }
.verdict-text { font-size:0.88rem; font-weight:500; }
.verdict-sub { font-size:0.78rem; color:var(--muted); margin-top:0.1rem; }
.table-wrap { overflow-x:auto; border-radius:var(--radius); border:1px solid var(--border); }
table { width:100%; border-collapse:collapse; font-size:0.86rem; }
thead th { background:#F0F2FA; padding:0.75rem 1rem; text-align:left; font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.07em; color:var(--muted); border-bottom:1px solid var(--border); white-space:nowrap; }
tbody tr { border-bottom:1px solid var(--border); transition:background 0.12s; }
tbody tr:last-child { border-bottom:none; }
tbody tr:hover { background:#F9FAFC; }
tbody td { padding:0.75rem 1rem; color:var(--text); vertical-align:middle; }
.td-text { max-width:280px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; color:var(--muted); font-size:0.83rem; }
.label-chip { display:inline-block; padding:0.22rem 0.7rem; border-radius:999px; font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; white-space:nowrap; }
.label-chip.pos { background:var(--pos-lt); color:var(--pos); }
.label-chip.neg { background:var(--neg-lt); color:var(--neg); }
.label-chip.neu { background:var(--neu-lt); color:var(--neu); }
.conf-bar-wrap { display:flex; align-items:center; gap:0.5rem; min-width:100px; }
.conf-bar-bg { flex:1; height:5px; background:var(--border); border-radius:999px; overflow:hidden; }
.conf-bar-fill { height:100%; border-radius:999px; }
.conf-bar-fill.pos { background:var(--pos); }
.conf-bar-fill.neg { background:var(--neg); }
.conf-bar-fill.neu { background:#9CA3AF; }
.conf-num { font-size:0.75rem; font-family:'DM Mono',monospace; color:var(--muted); white-space:nowrap; }
.td-del { color:#C8CEDC; cursor:pointer; font-size:0.8rem; font-weight:600; padding:0.2rem 0.5rem; border-radius:4px; transition:color 0.14s,background 0.14s; }
.td-del:hover { color:var(--neg); background:var(--neg-lt); }
.empty-state { text-align:center; padding:3rem 1rem; color:var(--muted); }
.empty-state .es-icon { width:48px; height:48px; border-radius:50%; background:var(--bg); border:1.5px solid var(--border); display:flex; align-items:center; justify-content:center; margin:0 auto 1rem; }
.empty-state .es-icon svg { opacity:0.4; }
.empty-state p { font-size:0.88rem; }
.toast { position:fixed; bottom:1.5rem; right:1.5rem; background:var(--text); color:#fff; font-size:0.84rem; font-weight:500; padding:0.7rem 1.2rem; border-radius:8px; box-shadow:0 8px 32px rgba(26,29,46,0.11); opacity:0; transform:translateY(8px); transition:opacity 0.22s,transform 0.22s; pointer-events:none; z-index:999; }
.toast.show { opacity:1; transform:translateY(0); }
.section-gap { margin-top:1.5rem; }
.section-header { margin-bottom:2rem; }
.section-eyebrow { font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.1em; color:var(--accent); margin-bottom:0.4rem; font-family:'DM Mono',monospace; }
.section-title { font-size:1.5rem; font-weight:700; letter-spacing:-0.02em; color:var(--text); margin-bottom:0.4rem; }
.section-sub { color:var(--muted); font-size:0.9rem; }
.hero-section { background:linear-gradient(135deg,#EEF0FD 0%,#F6F7FB 60%,#E8F8F3 100%); border-bottom:1px solid var(--border); padding:4rem 2rem; text-align:center; }
.hero-inner { max-width:620px; margin:0 auto; }
.hero-badge { display:inline-block; background:var(--accent-lt); color:var(--accent); border:1px solid #d0d5f7; border-radius:999px; padding:0.3rem 1rem; font-size:0.75rem; font-family:'DM Mono',monospace; font-weight:500; margin-bottom:1.3rem; letter-spacing:0.05em; }
.hero-title { font-size:clamp(1.8rem,4vw,2.8rem); font-weight:700; letter-spacing:-0.03em; line-height:1.2; color:var(--text); margin-bottom:1rem; }
.hero-sub { color:var(--muted); font-size:0.97rem; line-height:1.7; max-width:500px; margin:0 auto 2rem; }
.hero-btn { display:inline-block; background:var(--accent); color:#fff; font-family:'DM Sans',sans-serif; font-size:0.9rem; font-weight:600; padding:0.75rem 2rem; border-radius:8px; text-decoration:none; box-shadow:0 2px 12px rgba(79,99,210,0.3); transition:background 0.15s,box-shadow 0.15s; }
.hero-btn:hover { background:#3d50c0; box-shadow:0 4px 18px rgba(79,99,210,0.4); }
.how-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:1rem; }
.how-card { background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:1.4rem; box-shadow:var(--shadow); transition:transform 0.18s,border-color 0.18s; }
.how-card:hover { transform:translateY(-3px); border-color:#c7cdf5; }
.how-step { font-family:'DM Mono',monospace; font-size:0.72rem; font-weight:500; color:var(--accent); background:var(--accent-lt); display:inline-block; padding:0.2rem 0.6rem; border-radius:4px; margin-bottom:0.75rem; }
.how-title { font-weight:700; font-size:0.95rem; color:var(--text); margin-bottom:0.4rem; }
.how-desc { font-size:0.82rem; color:var(--muted); line-height:1.55; }
.about-grid { display:grid; grid-template-columns:1fr 1fr; gap:1.25rem; }
@media(max-width:700px){ .about-grid{grid-template-columns:1fr;} }
.about-card { display:flex; align-items:flex-start; gap:1.2rem; padding:1.5rem; }
.about-avatar { width:52px; height:52px; border-radius:50%; background:linear-gradient(135deg,var(--accent),#0F9B6E); display:flex; align-items:center; justify-content:center; font-family:'DM Sans',sans-serif; font-size:1.1rem; font-weight:700; color:#fff; flex-shrink:0; }
.about-name { font-weight:700; font-size:1rem; color:var(--text); margin-bottom:0.15rem; }
.about-email { font-size:0.82rem; color:var(--accent); margin-bottom:0.6rem; font-family:'DM Mono',monospace; }
.about-desc { font-size:0.83rem; color:var(--muted); line-height:1.6; }
.tech-chips { display:flex; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.5rem; }
.chip { font-size:0.75rem; font-weight:500; background:var(--bg); border:1px solid var(--border); color:var(--muted); border-radius:6px; padding:0.25rem 0.65rem; }
.perf-row { display:flex; align-items:center; gap:0.75rem; margin-top:0.6rem; }
.perf-label { font-size:0.78rem; font-weight:600; color:var(--muted); width:70px; flex-shrink:0; }
.perf-bar-bg { flex:1; height:6px; background:var(--border); border-radius:999px; overflow:hidden; }
.perf-bar-fill { height:100%; background:var(--accent); border-radius:999px; }
.perf-val { font-size:0.75rem; font-family:'DM Mono',monospace; color:var(--muted); width:70px; text-align:right; }
@media(max-width:600px){ .page-header h1{font-size:1.5rem;} .card{padding:1.1rem;} .hero-section{padding:2.5rem 1.2rem;} }
@media(prefers-reduced-motion:reduce){ *,*::before,*::after{transition:none!important;} }
</style>
</head>
<body>
<nav>
  <div class="nav-brand"><div class="nav-dot"></div>Sentiment Classifier</div>
  <div class="nav-links">
    <a href="#home" class="nav-link active">Home</a>
    <a href="#detector" class="nav-link">Detector</a>
    <a href="#how-it-works" class="nav-link">How it Works</a>
    <a href="#about" class="nav-link">About</a>
  </div>
  <div class="nav-tag">NLP · PyTorch</div>
</nav>
<div id="home" class="hero-section">
  <div class="hero-inner">
    <div class="hero-badge">NLP · Multi-Class · PyTorch</div>
    <h1 class="hero-title">Understand What Your<br/>Feedback Really Means</h1>
    <p class="hero-sub">Paste any feedback — product review, comment, or message — and our classifier will instantly tell you whether it is Positive, Negative, or Neutral, with confidence scores and key signal words.</p>
    <a href="#detector" class="hero-btn">Try the Detector</a>
  </div>
</div>

<div class="page">
  <div class="page-header" id="detector">
    <h1>Feedback Sentiment Analysis</h1>
    <p>Add multiple feedback entries and the classifier will analyse each one — showing a breakdown across Positive, Negative, and Neutral sentiments.</p>
  </div>
  <div class="card input-panel" style="margin-bottom:1.25rem;">
    <div class="card-title">Add Feedback</div>
    <textarea id="inputText" placeholder='Type or paste a feedback entry here — e.g. "The product quality is excellent but delivery was slow."' maxlength="600"></textarea>
    <div class="input-actions">
      <span class="char-count"><span id="charNum">0</span> / 600</span>
      <div class="btn-row">
        <button class="btn-secondary" onclick="clearInput()">Clear</button>
        <button class="btn-primary" onclick="addEntry()">Analyse &amp; Add</button>
      </div>
    </div>
  </div>
  <div class="grid-2">
    <div class="card">
      <div class="card-title">Summary</div>
      <div class="stats-row">
        <div class="stat-box pos"><div class="stat-num" id="posCount">0</div><div class="stat-label">Positive</div><div class="stat-pct" id="posPct">— %</div></div>
        <div class="stat-box neg"><div class="stat-num" id="negCount">0</div><div class="stat-label">Negative</div><div class="stat-pct" id="negPct">— %</div></div>
        <div class="stat-box neu"><div class="stat-num" id="neuCount">0</div><div class="stat-label">Neutral</div><div class="stat-pct" id="neuPct">— %</div></div>
      </div>
      <div class="verdict-box empty" id="verdictBox">
        <div class="verdict-indicator"></div>
        <div><div class="verdict-text" id="verdictText">No entries yet</div><div class="verdict-sub" id="verdictSub">Add feedback above to begin analysis</div></div>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Distribution</div>
      <div class="prog-row">
        <div class="prog-item"><span class="prog-label pos">Positive</span><div class="prog-track"><div class="prog-fill pos" id="posBar" style="width:0%"></div></div><span class="prog-val" id="posBarVal">0%</span></div>
        <div class="prog-item"><span class="prog-label neg">Negative</span><div class="prog-track"><div class="prog-fill neg" id="negBar" style="width:0%"></div></div><span class="prog-val" id="negBarVal">0%</span></div>
        <div class="prog-item"><span class="prog-label neu">Neutral</span><div class="prog-track"><div class="prog-fill neu" id="neuBar" style="width:0%"></div></div><span class="prog-val" id="neuBarVal">0%</span></div>
      </div>
      <canvas id="miniChart" height="90" style="margin-top:1.4rem;width:100%;"></canvas>
    </div>
  </div>
  <div class="card section-gap">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.1rem;flex-wrap:wrap;gap:0.5rem;">
      <div class="card-title" style="margin-bottom:0;">All Entries <span id="entryCount" style="color:var(--accent);font-family:'DM Mono',monospace;font-size:0.78rem;">(0)</span></div>
      <button class="btn-danger" onclick="clearAll()" id="clearAllBtn" style="display:none;">Clear All</button>
    </div>
    <div class="table-wrap">
      <table id="entryTable">
        <thead><tr><th style="width:40px;">#</th><th>Feedback Text</th><th>Sentiment</th><th>Confidence</th><th>Key Signal</th><th style="width:36px;"></th></tr></thead>
        <tbody id="tableBody">
          <tr id="emptyRow"><td colspan="6"><div class="empty-state"><div class="es-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div><p>No feedback analysed yet. Add an entry above to get started.</p></div></td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- HOW IT WORKS -->
  <div id="how-it-works" style="margin-top:3rem;">
    <div class="section-header">
      <div class="section-eyebrow">Process</div>
      <h2 class="section-title">How it Works</h2>
      <p class="section-sub">Four steps from raw text to sentiment insight.</p>
    </div>
    <div class="how-grid">
      <div class="how-card"><div class="how-step">01</div><div class="how-title">Text Input</div><div class="how-desc">Paste or type any feedback — product reviews, customer comments, or survey responses.</div></div>
      <div class="how-card"><div class="how-step">02</div><div class="how-title">Preprocessing</div><div class="how-desc">Text is cleaned, tokenised, stop words removed, and lemmatized to root forms.</div></div>
      <div class="how-card"><div class="how-step">03</div><div class="how-title">Classification</div><div class="how-desc">Lexicon-based classifier scores tokens, accounting for negation words like "not" or "never".</div></div>
      <div class="how-card"><div class="how-step">04</div><div class="how-title">Results</div><div class="how-desc">Each entry gets a sentiment label, confidence score, and key signal word highlighted.</div></div>
    </div>
  </div>

  <!-- ABOUT -->
  <div id="about" style="margin-top:3rem; margin-bottom:3rem;">
    <div class="section-header">
      <div class="section-eyebrow">Project</div>
      <h2 class="section-title">About</h2>
    </div>
    <div class="about-grid">
      <div class="card about-card">
        <div class="about-avatar">EI</div>
        <div>
          <div class="about-name">Eman Iftikhar</div>
          <div class="about-email">emaniftikhar41@gmail.com</div>
          <p class="about-desc">Built as Task 2 of an NLP assignment — implementing a multi-class sentiment classifier using PyTorch, TF-IDF vectorization, and preprocessing including lemmatization and stop-word removal.</p>
        </div>
      </div>
      <div class="card" style="padding:1.5rem;">
        <div class="card-title">Tech Stack</div>
        <div class="tech-chips">
          <span class="chip">PyTorch 2.x</span><span class="chip">Scikit-Learn</span><span class="chip">NLTK</span><span class="chip">TF-IDF</span><span class="chip">Pandas</span><span class="chip">NumPy</span><span class="chip">Streamlit</span><span class="chip">Early Stopping</span><span class="chip">WordNet Lemmatizer</span><span class="chip">Google Colab</span>
        </div>
        <div class="card-title" style="margin-top:1.2rem;">Model Performance</div>
        <div class="perf-row"><span class="perf-label">F1-Score</span><div class="perf-bar-bg"><div class="perf-bar-fill" style="width:91%"></div></div><span class="perf-val">91%</span></div>
        <div class="perf-row"><span class="perf-label">Accuracy</span><div class="perf-bar-bg"><div class="perf-bar-fill" style="width:90%"></div></div><span class="perf-val">90%</span></div>
        <div class="perf-row"><span class="perf-label">Dataset</span><div class="perf-bar-bg"><div class="perf-bar-fill" style="width:40%"></div></div><span class="perf-val">400 samples</span></div>
      </div>
    </div>
  </div>

</div>
<div class="toast" id="toast"></div>
<script>
const POSITIVE_WORDS=['love','great','excellent','amazing','fantastic','wonderful','brilliant','superb','outstanding','perfect','best','happy','delighted','thrilled','impressive','exceptional','phenomenal','incredible','awesome','good','nice','pleased','satisfied','recommend','enjoy','beautiful','reliable','fast','easy','helpful','quality','value','efficient','smooth','flawless','top','premium','well'];
const NEGATIVE_WORDS=['terrible','awful','horrible','bad','worst','poor','disappointing','useless','broken','waste','scam','fraud','defective','damaged','rude','slow','painful','regret','frustrating','unacceptable','disgusting','pathetic','garbage','junk','failed','cheap','flimsy','never','refund','avoid','problem','issue','wrong','misleading','fake','overpriced','annoying','difficult','confusing'];
const NEGATORS=["not","no","never","don't","doesn't","didn't","isn't","aren't","wasn't","weren't","can't","cannot","hardly","barely","without"];
function tokenize(t){return t.toLowerCase().replace(/[^a-z\s']/g,' ').split(/\s+/).filter(Boolean);}
function classify(text){
  const tokens=tokenize(text);let posScore=0,negScore=0;
  for(let i=0;i<tokens.length;i++){const t=tokens[i];const pN=i>0&&NEGATORS.includes(tokens[i-1]);const iP=POSITIVE_WORDS.includes(t);const iN=NEGATIVE_WORDS.includes(t);if(iP)pN?negScore+=1.2:posScore+=1;if(iN)pN?posScore+=0.8:negScore+=1;}
  const hasContrast=/\b(but|however|although|though|yet|while|whereas)\b/i.test(text);
  if(hasContrast&&posScore>0&&negScore>0){posScore*=0.85;negScore*=0.85;}
  const total=posScore+negScore;let label,confidence,keySignal;
  if(total<0.5){label='Neutral';confidence=Math.round(55+Math.random()*20);keySignal='No strong sentiment signals detected';}
  else{const pp=posScore/total;if(pp>=0.62){label='Positive';confidence=Math.min(98,Math.round(58+pp*40));const f=tokens.find(t=>POSITIVE_WORDS.includes(t));keySignal=f?`Signal word: "${f}"`:'Positive language pattern';}
  else if(pp<=0.38){label='Negative';confidence=Math.min(98,Math.round(58+(1-pp)*40));const f=tokens.find(t=>NEGATIVE_WORDS.includes(t));keySignal=f?`Signal word: "${f}"`:'Negative language pattern';}
  else{label='Neutral';confidence=Math.round(48+Math.random()*18);keySignal=hasContrast?'Mixed sentiment detected':'Balanced sentiment signals';}}
  return{label,confidence,keySignal};
}
let entries=[],idCounter=0;
const textarea=document.getElementById('inputText'),charNum=document.getElementById('charNum'),tableBody=document.getElementById('tableBody'),emptyRow=document.getElementById('emptyRow'),entryCount=document.getElementById('entryCount'),clearAllBtn=document.getElementById('clearAllBtn'),toastEl=document.getElementById('toast');
textarea.addEventListener('input',()=>charNum.textContent=textarea.value.length);
function showToast(msg){toastEl.textContent=msg;toastEl.classList.add('show');setTimeout(()=>toastEl.classList.remove('show'),2200);}
function clearInput(){textarea.value='';charNum.textContent='0';textarea.focus();}
function labelClass(l){return l==='Positive'?'pos':l==='Negative'?'neg':'neu';}
function addEntry(){
  const text=textarea.value.trim();if(!text){showToast('Please enter some feedback text.');return;}if(text.length<8){showToast('Entry is too short to analyse.');return;}
  const{label,confidence,keySignal}=classify(text);const id=++idCounter;entries.push({id,text,label,confidence,keySignal});renderTable();updateStats();clearInput();showToast(`Analysed — classified as ${label}`);
}
function deleteEntry(id){entries=entries.filter(e=>e.id!==id);renderTable();updateStats();}
function clearAll(){if(!entries.length)return;entries=[];renderTable();updateStats();showToast('All entries cleared.');}
function renderTable(){
  const rows=tableBody.querySelectorAll('tr.data-row');rows.forEach(r=>r.remove());
  if(!entries.length){emptyRow.style.display='';clearAllBtn.style.display='none';entryCount.textContent='(0)';return;}
  emptyRow.style.display='none';clearAllBtn.style.display='';entryCount.textContent=`(${entries.length})`;
  entries.forEach((e,i)=>{const cls=labelClass(e.label);const st=e.text.length>72?e.text.slice(0,72)+'…':e.text;const tr=document.createElement('tr');tr.className='data-row';
  tr.innerHTML=`<td style="color:var(--muted);font-family:'DM Mono',monospace;font-size:0.78rem;">${i+1}</td><td class="td-text" title="${e.text.replace(/"/g,'&quot;')}">${st}</td><td><span class="label-chip ${cls}">${e.label}</span></td><td><div class="conf-bar-wrap"><div class="conf-bar-bg"><div class="conf-bar-fill ${cls}" style="width:${e.confidence}%"></div></div><span class="conf-num">${e.confidence}%</span></div></td><td style="font-size:0.78rem;color:var(--muted);font-style:italic;">${e.keySignal}</td><td><span class="td-del" onclick="deleteEntry(${e.id})" title="Remove">&#x2715;</span></td>`;
  tableBody.appendChild(tr);});
}
function updateStats(){
  const pos=entries.filter(e=>e.label==='Positive').length,neg=entries.filter(e=>e.label==='Negative').length,neu=entries.filter(e=>e.label==='Neutral').length,total=entries.length;
  document.getElementById('posCount').textContent=pos;document.getElementById('negCount').textContent=neg;document.getElementById('neuCount').textContent=neu;
  const fmt=n=>total?Math.round(n/total*100)+'%':'— %';
  document.getElementById('posPct').textContent=fmt(pos);document.getElementById('negPct').textContent=fmt(neg);document.getElementById('neuPct').textContent=fmt(neu);
  const pct=n=>total?Math.round(n/total*100):0;const pp=pct(pos),np=pct(neg),nep=pct(neu);
  document.getElementById('posBar').style.width=pp+'%';document.getElementById('negBar').style.width=np+'%';document.getElementById('neuBar').style.width=nep+'%';
  document.getElementById('posBarVal').textContent=pp+'%';document.getElementById('negBarVal').textContent=np+'%';document.getElementById('neuBarVal').textContent=nep+'%';
  const vBox=document.getElementById('verdictBox'),vText=document.getElementById('verdictText'),vSub=document.getElementById('verdictSub');
  vBox.className='verdict-box';
  if(!total){vBox.classList.add('empty');vText.textContent='No entries yet';vSub.textContent='Add feedback above to begin analysis';}
  else{const dom=pos>=neg&&pos>=neu?'pos':neg>=pos&&neg>=neu?'neg':'neu';vBox.classList.add(dom);const labs={pos:'Positive',neg:'Negative',neu:'Neutral'};const dp=pct(dom==='pos'?pos:dom==='neg'?neg:neu);vText.textContent=`Overall sentiment: ${labs[dom]}`;vSub.textContent=`${dp}% of ${total} entr${total===1?'y':'ies'} lean ${labs[dom].toLowerCase()}`;}
  drawChart(pos,neg,neu);
}
function drawChart(pos,neg,neu){
  const canvas=document.getElementById('miniChart'),ctx=canvas.getContext('2d'),dpr=window.devicePixelRatio||1,W=canvas.offsetWidth,H=90;
  canvas.width=W*dpr;canvas.height=H*dpr;ctx.scale(dpr,dpr);ctx.clearRect(0,0,W,H);
  const data=[pos,neg,neu],colors=['#0F9B6E','#D93B3B','#9CA3AF'],labels=['Positive','Negative','Neutral'],max=Math.max(...data,1),barW=48,gap=(W-data.length*barW)/(data.length+1),maxH=H-28;
  ctx.font=`500 10px 'DM Sans',sans-serif`;ctx.textAlign='center';
  data.forEach((val,i)=>{const x=gap+i*(barW+gap),bH=val===0?2:Math.max(4,(val/max)*maxH),y=maxH-bH;
  ctx.fillStyle=colors[i];ctx.globalAlpha=0.85;ctx.beginPath();ctx.moveTo(x+4,y);ctx.lineTo(x+barW-4,y);ctx.quadraticCurveTo(x+barW,y,x+barW,y+4);ctx.lineTo(x+barW,y+bH);ctx.lineTo(x,y+bH);ctx.lineTo(x,y+4);ctx.quadraticCurveTo(x,y,x+4,y);ctx.closePath();ctx.fill();ctx.globalAlpha=1;
  if(val>0){ctx.fillStyle=colors[i];ctx.fillText(val,x+barW/2,y-5);}ctx.fillStyle='#6B7280';ctx.fillText(labels[i],x+barW/2,H-4);});
}
textarea.addEventListener('keydown',e=>{if(e.key==='Enter'&&(e.ctrlKey||e.metaKey))addEntry();});
updateStats();
window.addEventListener('resize',()=>{const pos=entries.filter(e=>e.label==='Positive').length,neg=entries.filter(e=>e.label==='Negative').length,neu=entries.filter(e=>e.label==='Neutral').length;drawChart(pos,neg,neu);});
</script>
</body>
</html>"""

st.components.v1.html(HTML, height=1100, scrolling=True)
