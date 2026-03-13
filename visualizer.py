import os
import json
import webbrowser
from datetime import datetime

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Email Intelligence Hub</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/echarts-wordcloud@2.1.0/dist/echarts-wordcloud.min.js"></script>
<style>
:root {
    --bg-deep: #06080f;
    --bg-primary: #0a0e1a;
    --bg-card: #12162a;
    --bg-card-hover: #1a1f3a;
    --accent-blue: #3b82f6;
    --accent-purple: #8b5cf6;
    --accent-pink: #ec4899;
    --accent-cyan: #06b6d4;
    --accent-green: #10b981;
    --accent-amber: #f59e0b;
    --accent-red: #ef4444;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: rgba(255,255,255,0.07);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100%; }
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg-deep);
    color: var(--text-primary);
    overflow-x: hidden;
}

.bg-glow {
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    overflow: hidden;
}
.bg-glow .orb {
    position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.12;
    animation: float 20s ease-in-out infinite alternate;
}
.bg-glow .orb:nth-child(1) { width: 600px; height: 600px; background: #6366f1; top: -10%; left: -5%; }
.bg-glow .orb:nth-child(2) { width: 500px; height: 500px; background: #ec4899; bottom: -10%; right: -5%; animation-delay: -7s; }
.bg-glow .orb:nth-child(3) { width: 400px; height: 400px; background: #06b6d4; top: 40%; left: 50%; animation-delay: -14s; }
@keyframes float {
    0% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(30px, -40px) scale(1.05); }
    66% { transform: translate(-20px, 20px) scale(0.95); }
    100% { transform: translate(10px, -10px) scale(1.02); }
}

header {
    position: relative; z-index: 10;
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 32px;
    border-bottom: 1px solid var(--border);
    background: rgba(6,8,15,0.85);
    backdrop-filter: blur(24px);
}
.logo {
    display: flex; align-items: center; gap: 14px;
    font-size: 1.2rem; font-weight: 700;
}
.logo-mark {
    width: 38px; height: 38px; border-radius: 11px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; font-weight: 800; color: white;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4);
}
.logo-text {
    background: linear-gradient(135deg, #a5b4fc, #c4b5fd, #f0abfc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.header-right {
    display: flex; align-items: center; gap: 24px;
}
.filter-bar {
    display: flex; align-items: center; gap: 20px; flex-wrap: wrap;
}
.date-filter-bar, .exclude-filter-bar {
    display: flex; align-items: center; gap: 10px;
}
.exclude-filter-bar { flex-wrap: wrap; }
.exclude-check {
    display: flex; align-items: center; gap: 5px;
    font-size: 0.8rem; color: var(--text-muted); cursor: pointer;
    user-select: none;
}
.exclude-check:hover { color: var(--text-secondary); }
.exclude-check input { cursor: pointer; }
.date-filter-label { color: var(--text-muted); font-size: 0.82rem; }
.date-filter-btns { display: flex; gap: 4px; }
.date-filter-btn {
    padding: 6px 14px; border-radius: 8px;
    font-size: 0.8rem; font-weight: 500;
    color: var(--text-muted); cursor: pointer;
    border: 1px solid var(--border);
    background: transparent; transition: all 0.2s;
    font-family: inherit;
}
.date-filter-btn:hover {
    color: var(--text-secondary); border-color: rgba(255,255,255,0.15);
}
.date-filter-btn.active {
    color: #c7d2fe; background: rgba(99,102,241,0.15);
    border-color: rgba(99,102,241,0.35);
}
.header-meta { color: var(--text-muted); font-size: 0.82rem; }

nav {
    position: sticky; top: 0; z-index: 20;
    display: flex; justify-content: center; gap: 6px;
    padding: 12px 32px;
    background: rgba(6,8,15,0.92);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
}
.tab {
    padding: 9px 24px; border-radius: 9px;
    font-size: 0.88rem; font-weight: 500;
    color: var(--text-muted); cursor: pointer;
    transition: all 0.25s ease;
    border: 1px solid transparent;
    display: flex; align-items: center; gap: 8px;
    user-select: none;
}
.tab:hover { color: var(--text-secondary); background: rgba(255,255,255,0.03); }
.tab.active {
    color: #e0e7ff;
    background: rgba(99,102,241,0.12);
    border-color: rgba(99,102,241,0.25);
}
.tab .badge {
    background: #ef4444; color: white;
    font-size: 0.65rem; font-weight: 700;
    padding: 2px 6px; border-radius: 10px;
    line-height: 1; min-width: 18px; text-align: center;
}

main {
    position: relative; z-index: 5;
    padding: 28px 32px 80px;
    max-width: 1440px; margin: 0 auto;
}
.panel { display: none; animation: panelIn 0.35s ease; }
.panel.active { display: block; }
@keyframes panelIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.section-head { margin-bottom: 20px; }
.section-head h2 { font-size: 1.35rem; font-weight: 700; margin-bottom: 4px; }
.section-head p { color: var(--text-muted); font-size: 0.85rem; }

.chart-wrap {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    position: relative;
}
.chart-toolbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 20px;
    border-bottom: 1px solid var(--border);
    background: rgba(255,255,255,0.02);
}
.chart-toolbar .toolbar-group { display: flex; gap: 4px; }
.seg-btn {
    padding: 5px 14px; border-radius: 7px;
    font-size: 0.78rem; font-weight: 500;
    color: var(--text-muted); cursor: pointer;
    border: 1px solid transparent;
    background: transparent; transition: all 0.2s;
    font-family: inherit;
}
.seg-btn:hover { color: var(--text-secondary); }
.seg-btn.active {
    color: #c7d2fe; background: rgba(99,102,241,0.15);
    border-color: rgba(99,102,241,0.3);
}
.toolbar-hint { color: var(--text-muted); font-size: 0.75rem; }
#mindmap-chart { width: 100%; height: 680px; }
#wordcloud-chart { width: 100%; height: 560px; }

.wc-layout { display: grid; grid-template-columns: 1fr 320px; gap: 20px; }
@media (max-width: 960px) { .wc-layout { grid-template-columns: 1fr; } }
.wc-sidebar { display: flex; flex-direction: column; gap: 14px; }
.stat-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 18px;
}
.stat-card h4 {
    font-size: 0.72rem; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 10px;
}
.stat-big {
    font-size: 2.2rem; font-weight: 800;
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.rank-list { list-style: none; }
.rank-item {
    display: flex; align-items: center; gap: 10px;
    padding: 7px 0; border-bottom: 1px solid var(--border);
    font-size: 0.85rem;
}
.rank-item:last-child { border-bottom: none; }
.rank-pos {
    width: 22px; height: 22px; border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.7rem; font-weight: 700; flex-shrink: 0;
}
.rank-pos.top3 { background: rgba(99,102,241,0.2); color: #a5b4fc; }
.rank-pos.rest { background: rgba(255,255,255,0.04); color: var(--text-muted); }
.rank-word { flex: 1; color: var(--text-primary); }
.rank-bar { flex: 0 0 80px; height: 4px; border-radius: 2px; background: rgba(255,255,255,0.06); overflow: hidden; }
.rank-bar-fill { height: 100%; border-radius: 2px; background: linear-gradient(90deg, #6366f1, #8b5cf6); }
.rank-val { color: var(--accent-purple); font-weight: 600; font-size: 0.8rem; width: 28px; text-align: right; }

.ddl-bar { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.ddl-chip {
    display: flex; align-items: center; gap: 10px;
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 10px; padding: 12px 20px; min-width: 140px;
}
.ddl-dot { width: 10px; height: 10px; border-radius: 50%; }
.ddl-dot.high { background: #ef4444; box-shadow: 0 0 10px rgba(239,68,68,0.5); }
.ddl-dot.medium { background: #f59e0b; box-shadow: 0 0 10px rgba(245,158,11,0.5); }
.ddl-dot.low { background: #10b981; box-shadow: 0 0 10px rgba(16,185,129,0.5); }
.ddl-chip-num { font-size: 1.3rem; font-weight: 700; }
.ddl-chip-label { font-size: 0.78rem; color: var(--text-muted); }

.ddl-filters { display: flex; gap: 6px; margin-bottom: 18px; }
.ddl-filter-btn {
    padding: 6px 16px; border-radius: 8px;
    font-size: 0.8rem; font-weight: 500;
    color: var(--text-muted); cursor: pointer;
    border: 1px solid var(--border);
    background: transparent; transition: all 0.2s;
    font-family: inherit;
}
.ddl-filter-btn:hover { color: var(--text-secondary); border-color: rgba(255,255,255,0.12); }
.ddl-filter-btn.active {
    color: #c7d2fe; background: rgba(99,102,241,0.1); border-color: rgba(99,102,241,0.3);
}

.ddl-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 14px;
}
.ddl-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 14px; padding: 22px;
    transition: all 0.25s ease; position: relative; overflow: hidden;
}
.ddl-card.clickable {
    cursor: pointer;
}
.ddl-card.clickable::after {
    content: 'Click to view original email';
    position: absolute; bottom: 12px; right: 18px;
    font-size: 0.7rem; color: var(--accent-cyan); opacity: 0.8;
}
.ddl-card:hover {
    background: var(--bg-card-hover);
    border-color: rgba(99,102,241,0.25);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}
.ddl-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
}
.ddl-card.u-high::before { background: linear-gradient(90deg, #ef4444, #ec4899); }
.ddl-card.u-medium::before { background: linear-gradient(90deg, #f59e0b, #fb923c); }
.ddl-card.u-low::before { background: linear-gradient(90deg, #10b981, #34d399); }
.ddl-tag {
    display: inline-block; padding: 3px 10px; border-radius: 6px;
    font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.05em; margin-bottom: 10px;
}
.u-high .ddl-tag { background: rgba(239,68,68,0.12); color: #f87171; }
.u-medium .ddl-tag { background: rgba(245,158,11,0.12); color: #fbbf24; }
.u-low .ddl-tag { background: rgba(16,185,129,0.12); color: #34d399; }
.ddl-title { font-size: 1rem; font-weight: 600; margin-bottom: 6px; line-height: 1.4; }
.ddl-desc { color: var(--text-secondary); font-size: 0.82rem; margin-bottom: 12px; line-height: 1.5; }
.ddl-meta { display: flex; justify-content: space-between; align-items: center; color: var(--text-muted); font-size: 0.78rem; }
.ddl-date { display: flex; align-items: center; gap: 5px; font-weight: 500; }
.ddl-cd { font-weight: 600; padding: 3px 9px; border-radius: 6px; font-size: 0.72rem; }
.u-high .ddl-cd { background: rgba(239,68,68,0.1); color: #f87171; }
.u-medium .ddl-cd { background: rgba(245,158,11,0.1); color: #fbbf24; }
.u-low .ddl-cd { background: rgba(16,185,129,0.1); color: #34d399; }
.ddl-empty { grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--text-muted); }
.ddl-empty-icon { font-size: 2.5rem; margin-bottom: 12px; opacity: 0.6; }

footer {
    position: relative; z-index: 10;
    text-align: center; padding: 20px;
    color: var(--text-muted); font-size: 0.75rem;
    border-top: 1px solid var(--border);
}

.email-modal-overlay {
    display: none; position: fixed; inset: 0; z-index: 1000;
    background: rgba(0,0,0,0.65); backdrop-filter: blur(8px);
    align-items: center; justify-content: center;
    animation: modalBgIn 0.2s ease;
}
.email-modal-overlay.visible { display: flex; }
@keyframes modalBgIn { from { opacity: 0; } to { opacity: 1; } }
.email-modal {
    background: var(--bg-card); border: 1px solid rgba(99,102,241,0.25);
    border-radius: 18px; width: 90%; max-width: 640px; max-height: 80vh;
    display: flex; flex-direction: column;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 40px rgba(99,102,241,0.1);
    animation: modalIn 0.25s ease;
}
@keyframes modalIn {
    from { opacity: 0; transform: translateY(20px) scale(0.97); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
.email-modal-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 18px 24px; border-bottom: 1px solid var(--border);
}
.email-modal-header h3 {
    font-size: 1rem; font-weight: 600;
    background: linear-gradient(135deg, #a5b4fc, #c4b5fd);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.email-modal-close {
    width: 32px; height: 32px; border-radius: 8px;
    border: 1px solid var(--border); background: transparent;
    color: var(--text-muted); font-size: 1.2rem; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: all 0.2s;
}
.email-modal-close:hover { background: rgba(239,68,68,0.1); color: #f87171; border-color: rgba(239,68,68,0.3); }
.email-modal-body { padding: 20px 24px; overflow-y: auto; flex: 1; }
.email-detail-card {
    background: rgba(255,255,255,0.02); border: 1px solid var(--border);
    border-radius: 12px; padding: 18px; margin-bottom: 12px;
    transition: border-color 0.2s;
}
.email-detail-card:last-child { margin-bottom: 0; }
.email-detail-card:hover { border-color: rgba(99,102,241,0.3); }
.email-detail-subject {
    font-size: 0.95rem; font-weight: 600; color: var(--text-primary);
    margin-bottom: 8px; line-height: 1.4;
}
.email-detail-date {
    font-size: 0.78rem; color: var(--accent-cyan); font-weight: 500;
    margin-bottom: 10px; display: flex; align-items: center; gap: 6px;
}
.email-detail-snippet {
    font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;
    border-left: 3px solid rgba(99,102,241,0.3); padding-left: 14px;
}
.email-detail-label {
    font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;
    letter-spacing: 0.06em; margin-bottom: 4px;
}
.email-modal-empty { text-align: center; padding: 40px 20px; color: var(--text-muted); }
.email-gmail-link {
    display: block; margin-top: 12px; padding: 10px 14px;
    background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.2);
    border-radius: 8px; color: #93c5fd; font-size: 0.82rem;
    text-decoration: none; transition: all 0.2s; font-weight: 500;
}
.email-gmail-link:hover {
    background: rgba(59,130,246,0.15); border-color: rgba(59,130,246,0.4);
    color: #bfdbfe;
}
</style>
</head>
<body>
<div class="bg-glow">
    <div class="orb"></div><div class="orb"></div><div class="orb"></div>
</div>

<header>
    <div class="logo">
        <div class="logo-mark">E</div>
        <span class="logo-text">Email Intelligence Hub</span>
    </div>
    <div class="header-right">
        <div class="filter-bar">
            <div class="date-filter-bar">
                <span class="date-filter-label">Date:</span>
                <div class="date-filter-btns">
                    <button class="date-filter-btn active" data-range="all">All</button>
                    <button class="date-filter-btn" data-range="7d">7 days</button>
                    <button class="date-filter-btn" data-range="30d">30 days</button>
                </div>
            </div>
            <div class="exclude-filter-bar">
                <span class="date-filter-label">Exclude:</span>
                <label class="exclude-check"><input type="checkbox" id="exclude-promotions"> Promotions</label>
                <label class="exclude-check"><input type="checkbox" id="exclude-social"> Social</label>
                <label class="exclude-check"><input type="checkbox" id="exclude-updates"> Updates</label>
                <label class="exclude-check" title="Exclude emails with unsubscribe, newsletter, etc. in subject/snippet"><input type="checkbox" id="exclude-keywords"> Keywords</label>
            </div>
        </div>
        <div class="header-meta">__TIME_NOW__</div>
    </div>
</header>

<nav>
    <div class="tab active" data-panel="mindmap">&#x1f9e0; Mind Map</div>
    <div class="tab" data-panel="wordcloud">&#x2601;&#xfe0f; Word Cloud</div>
    <div class="tab" data-panel="deadline" id="tab-ddl">&#x23f0; DDL Tracker</div>
</nav>

<main>
    <div class="panel active" id="panel-mindmap">
        <div class="section-head">
            <h2>Email Mind Map</h2>
            <p>Click leaf nodes to view original email &middot; Scroll to zoom &middot; Drag to pan</p>
        </div>
        <div class="chart-wrap">
            <div class="chart-toolbar">
                <div class="toolbar-group">
                    <button class="seg-btn active" data-layout="radial">Radial</button>
                    <button class="seg-btn" data-layout="lr">Horizontal</button>
                    <button class="seg-btn" data-layout="tb">Vertical</button>
                </div>
                <span class="toolbar-hint">Scroll to zoom &middot; Drag to pan</span>
            </div>
            <div id="mindmap-chart"></div>
        </div>
    </div>

    <div class="panel" id="panel-wordcloud">
        <div class="section-head">
            <h2>Word Cloud Analysis</h2>
            <p>Keywords extracted from your emails, sized by importance &middot; Hover for details</p>
        </div>
        <div class="wc-layout">
            <div class="chart-wrap">
                <div id="wordcloud-chart"></div>
            </div>
            <div class="wc-sidebar">
                <div class="stat-card">
                    <h4>Total Keywords</h4>
                    <div class="stat-big" id="wc-total">--</div>
                </div>
                <div class="stat-card">
                    <h4>Top Keywords</h4>
                    <ul class="rank-list" id="wc-ranks"></ul>
                </div>
            </div>
        </div>
    </div>

    <div class="panel" id="panel-deadline">
        <div class="section-head">
            <h2>DDL Tracker</h2>
            <p>Deadlines and action items extracted from your emails</p>
        </div>
        <div class="ddl-bar" id="ddl-bar"></div>
        <div class="ddl-filters" id="ddl-filters"></div>
        <div class="ddl-grid" id="ddl-grid"></div>
    </div>
</main>

<footer>Email Intelligence Hub &middot; Powered by Claude AI &middot; __TIME_NOW__</footer>

<div class="email-modal-overlay" id="emailModal">
    <div class="email-modal">
        <div class="email-modal-header">
            <h3>&#x1f4e7; Original Email Content</h3>
            <button class="email-modal-close" id="emailModalClose">&times;</button>
        </div>
        <div class="email-modal-body" id="emailModalBody"></div>
    </div>
</div>

<script>
(function() {
    var categories = __CAT_JSON__;
    var wcRaw      = __WC_JSON__;
    var dlRaw      = __DL_JSON__;
    var emailsRaw  = __EMAILS_JSON__;

    /* ===== Filter state ===== */
    var EXCLUDE_KEYWORDS = ['unsubscribe', 'newsletter', 'marketing'];
    var currentDateRange = 'all';

    function getVisibleIndices(range) {
        var excludePromo = document.getElementById('exclude-promotions') && document.getElementById('exclude-promotions').checked;
        var excludeSocial = document.getElementById('exclude-social') && document.getElementById('exclude-social').checked;
        var excludeUpdates = document.getElementById('exclude-updates') && document.getElementById('exclude-updates').checked;
        var excludeKw = document.getElementById('exclude-keywords') && document.getElementById('exclude-keywords').checked;

        var visible = new Set();
        var today = new Date(); today.setHours(0,0,0,0);
        var cutoff = range === '7d' ? (function(){ var d=new Date(today); d.setDate(d.getDate()-7); return d; })() :
                     range === '30d' ? (function(){ var d=new Date(today); d.setDate(d.getDate()-30); return d; })() : null;

        emailsRaw.forEach(function(em, idx) {
            var labels = em.labelIds || [];
            if (excludePromo && labels.indexOf('CATEGORY_PROMOTIONS') >= 0) return;
            if (excludeSocial && labels.indexOf('CATEGORY_SOCIAL') >= 0) return;
            if (excludeUpdates && labels.indexOf('CATEGORY_UPDATES') >= 0) return;
            if (excludeKw) {
                var text = ((em.subject || '') + ' ' + (em.snippet || '')).toLowerCase();
                if (EXCLUDE_KEYWORDS.some(function(k) { return k && text.indexOf(k.toLowerCase()) >= 0; })) return;
            }
            if (cutoff) {
                var iso = em.date_iso;
                if (!iso) { visible.add(idx); return; }
                if (new Date(iso + 'T12:00:00') >= cutoff) visible.add(idx);
            } else {
                visible.add(idx);
            }
        });
        return visible;
    }

    function buildFilteredTree(cats, visibleIndices) {
        var filterFn = function(indices) {
            if (!visibleIndices) return indices.length > 0;
            return indices.some(function(i) { return visibleIndices.has(i); });
        };
        var children = Object.entries(cats).map(function(entry) {
            var cat = entry[0], items = entry[1];
            var c = COLORS[Object.keys(cats).indexOf(cat) % COLORS.length];
            var list = Array.isArray(items) ? items : [items];
            var filtered = list.filter(Boolean).map(function(t) {
                var isObj = typeof t === 'object' && t !== null;
                var aiText = isObj ? String(t.text || '') : String(t);
                var rawIndices = isObj && Array.isArray(t.idx) ? t.idx : [];
                var indices = rawIndices.filter(function(idx) {
                    return typeof idx === 'number' && idx >= 0 && idx < emailsRaw.length;
                });
                if (!filterFn(indices)) return null;
                var label = aiText;
                if (indices.length === 1) {
                    var origSubj = getOriginalSubject(indices[0]);
                    if (origSubj && origSubj !== aiText) label = aiText + ' [' + origSubj + ']';
                }
                var hasValidLink = indices.length > 0;
                return {
                    name: label,
                    aiText: aiText,
                    emailIndices: indices,
                    itemStyle: { color: c, borderColor: hasValidLink ? '#818cf8' : c, opacity: hasValidLink ? 0.85 : 0.5, borderWidth: hasValidLink ? 2 : 0 },
                    lineStyle: { color: c, opacity: 0.35 }
                };
            }).filter(Boolean);
            if (filtered.length === 0) return null;
            return {
                name: cat,
                itemStyle: { color: c, borderColor: c },
                lineStyle: { color: c, opacity: 0.5 },
                children: filtered
            };
        }).filter(Boolean);
        return {
            name: 'Email Hub',
            itemStyle: { color: '#6366f1', borderColor: '#818cf8', borderWidth: 3 },
            children: children.length ? children : [{ name: '(No emails in this range)', itemStyle: { opacity: 0.5 }, lineStyle: { opacity: 0.2 } }]
        };
    }

    function applyDateFilter(range) {
        currentDateRange = range;
        var visible = getVisibleIndices(range);
        var tree = buildFilteredTree(categories, visible);
        var layout = document.querySelector('.seg-btn[data-layout].active');
        mmChart.setOption(mmOption(layout ? layout.dataset.layout : 'radial', tree), true);
        currentDdlData = range === 'all' ? dlRaw : dlRaw.filter(function(d) {
            if (!d.date) return true;
            var dDate = new Date(d.date + 'T12:00:00');
            var today = new Date(); today.setHours(0,0,0,0);
            var cutoff = new Date(today);
            if (range === '7d') cutoff.setDate(cutoff.getDate() - 7);
            else if (range === '30d') cutoff.setDate(cutoff.getDate() - 30);
            return dDate >= cutoff;
        });
        renderDDL(currentUrgencyFilter);
    }

    document.querySelectorAll('.date-filter-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.date-filter-btn').forEach(function(b) { b.classList.remove('active'); });
            this.classList.add('active');
            currentDateRange = this.dataset.range;
            applyDateFilter(currentDateRange);
        });
    });

    ['exclude-promotions','exclude-social','exclude-updates','exclude-keywords'].forEach(function(id) {
        var el = document.getElementById(id);
        if (el) el.addEventListener('change', function() { applyDateFilter(currentDateRange); });
    });

    /* ===== Tab switching ===== */
    var tabs = document.querySelectorAll('.tab');
    var panels = document.querySelectorAll('.panel');
    var wcInited = false;

    tabs.forEach(function(tab) {
        tab.addEventListener('click', function() {
            tabs.forEach(function(t) { t.classList.remove('active'); });
            panels.forEach(function(p) { p.classList.remove('active'); });
            tab.classList.add('active');
            var id = tab.dataset.panel;
            document.getElementById('panel-' + id).classList.add('active');
            if (id === 'mindmap') setTimeout(function() { mmChart.resize(); }, 50);
            if (id === 'wordcloud') {
                if (!wcInited) { initWordCloud(); wcInited = true; }
                setTimeout(function() { if (wcChart) wcChart.resize(); }, 50);
            }
        });
    });

    /* ===== Colors ===== */
    var COLORS = [
        '#6366f1','#ec4899','#10b981','#f59e0b','#06b6d4',
        '#8b5cf6','#f43f5e','#14b8a6','#3b82f6','#a855f7',
        '#84cc16','#f97316'
    ];

    /* ===== MIND MAP ===== */
    function getOriginalSubject(idx) {
        if (typeof idx === 'number' && idx >= 0 && idx < emailsRaw.length) {
            var subj = emailsRaw[idx].subject || '';
            return subj.length > 20 ? subj.substring(0, 18) + '..' : subj;
        }
        return '';
    }

    var treeData = buildFilteredTree(categories, null);
    var mmChart = echarts.init(document.getElementById('mindmap-chart'));

    function mmOption(layout, treeDataToUse) {
        var tree = treeDataToUse || treeData;
        var isRadial = layout === 'radial';
        var orient = layout === 'tb' ? 'TB' : 'LR';
        return {
            tooltip: {
                trigger: 'item', triggerOn: 'mousemove',
                backgroundColor: 'rgba(10,14,26,0.92)',
                borderColor: 'rgba(99,102,241,0.3)',
                textStyle: { color: '#e2e8f0', fontSize: 13, fontFamily: 'Inter' },
                formatter: function(p) {
                    if (p.data.children && p.data.children.length)
                        return '<b>' + p.name + '</b><br/><span style="color:#94a3b8">' + p.data.children.length + ' items</span>';
                    if (p.data.emailIndices && p.data.emailIndices.length) {
                        var tip = '<b>' + (p.data.aiText || p.name) + '</b>';
                        p.data.emailIndices.forEach(function(idx) {
                            if (idx >= 0 && idx < emailsRaw.length) {
                                tip += '<br/><span style="color:#94a3b8;font-size:11px">Subject: ' + emailsRaw[idx].subject + '</span>';
                            }
                        });
                        tip += '<br/><span style="color:#818cf8;font-size:11px">&#x1f517; Click to view original email</span>';
                        return tip;
                    }
                    if (p.data.aiText) return p.data.aiText + '<br/><span style="color:#f87171;font-size:11px">&#x26a0; No linked email</span>';
                    return p.name;
                }
            },
            series: [{
                type: 'tree',
                data: [tree],
                layout: isRadial ? 'radial' : 'orthogonal',
                orient: isRadial ? undefined : orient,
                roam: true,
                initialTreeDepth: 3,
                symbol: 'circle',
                symbolSize: function(val, params) {
                    var d = params.data;
                    if (d.name === 'Email Hub') return 28;
                    if (d.children && d.children.length) return 14;
                    return 7;
                },
                label: {
                    fontSize: 13,
                    color: '#e2e8f0',
                    fontFamily: 'Inter, sans-serif',
                    formatter: function(p) {
                        var n = p.name;
                        return n.length > 24 ? n.substring(0, 22) + '...' : n;
                    }
                },
                leaves: {
                    label: { fontSize: 11, color: '#94a3b8' }
                },
                lineStyle: { width: 1.5, curveness: 0.5 },
                emphasis: {
                    focus: 'descendant',
                    itemStyle: { shadowBlur: 10, shadowColor: 'rgba(99,102,241,0.4)' }
                },
                expandAndCollapse: true,
                animationDuration: 500,
                animationDurationUpdate: 600,
                left: isRadial ? undefined : '8%',
                right: isRadial ? undefined : '24%',
                top: isRadial ? undefined : '6%',
                bottom: isRadial ? undefined : '6%'
            }]
        };
    }

    mmChart.setOption(mmOption('radial'));

    document.querySelectorAll('.seg-btn[data-layout]').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.seg-btn[data-layout]').forEach(function(b) { b.classList.remove('active'); });
            this.classList.add('active');
            var tree = buildFilteredTree(categories, getVisibleIndices(currentDateRange));
            mmChart.setOption(mmOption(this.dataset.layout, tree), true);
        });
    });

    /* ===== EMAIL DETAIL MODAL ===== */
    var modalEl = document.getElementById('emailModal');
    var modalBody = document.getElementById('emailModalBody');
    var modalClose = document.getElementById('emailModalClose');

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function gmailSearchUrl(subject) {
        return 'https://mail.google.com/mail/u/0/#search/' + encodeURIComponent('subject:' + subject);
    }

    function showEmailModal(indices) {
        modalBody.innerHTML = '';
        if (!indices || !indices.length || !emailsRaw.length) {
            modalBody.innerHTML = '<div class="email-modal-empty">&#x26a0; No linked email found for this node.<br/><span style="font-size:0.82rem">This may indicate AI hallucination.</span></div>';
            modalEl.classList.add('visible');
            return;
        }
        indices.forEach(function(idx) {
            if (idx < 0 || idx >= emailsRaw.length) return;
            var email = emailsRaw[idx];
            if (!email) return;
            var card = document.createElement('div');
            card.className = 'email-detail-card';
            var subject = email.subject || 'No Subject';
            card.innerHTML =
                '<div class="email-detail-label">Subject</div>' +
                '<div class="email-detail-subject">' + escapeHtml(subject) + '</div>' +
                (email.from ? '<div class="email-detail-date">&#x1f464; ' + escapeHtml(email.from) + '</div>' : '') +
                '<div class="email-detail-date">&#x1f4c5; ' + escapeHtml(email.date || 'Unknown') + '</div>' +
                '<div class="email-detail-label">Email Snippet</div>' +
                '<div class="email-detail-snippet">' + escapeHtml(email.snippet || 'No content available') + '</div>' +
                '<a class="email-gmail-link" href="' + gmailSearchUrl(subject) + '" target="_blank" rel="noopener">&#x1f50d; Search in Gmail: ' + escapeHtml(subject.length > 40 ? subject.substring(0,38) + '..' : subject) + '</a>';
            modalBody.appendChild(card);
        });
        modalEl.classList.add('visible');
    }

    function hideEmailModal() { modalEl.classList.remove('visible'); }
    modalClose.addEventListener('click', hideEmailModal);
    modalEl.addEventListener('click', function(e) { if (e.target === modalEl) hideEmailModal(); });
    document.addEventListener('keydown', function(e) { if (e.key === 'Escape') hideEmailModal(); });

    mmChart.on('click', function(params) {
        var data = params.data;
        if (data && data.emailIndices && data.emailIndices.length > 0) {
            showEmailModal(data.emailIndices);
        }
    });

    /* ===== WORD CLOUD ===== */
    var wcChart = null;
    var wcSorted = wcRaw.slice().sort(function(a, b) { return b.weight - a.weight; });

    document.getElementById('wc-total').textContent = wcRaw.length;

    var ranksEl = document.getElementById('wc-ranks');
    var topN = wcSorted.slice(0, 10);
    var maxW = topN.length ? topN[0].weight : 1;
    topN.forEach(function(item, i) {
        var li = document.createElement('li');
        li.className = 'rank-item';
        var pct = Math.round(item.weight / maxW * 100);
        li.innerHTML =
            '<span class="rank-pos ' + (i < 3 ? 'top3' : 'rest') + '">' + (i + 1) + '</span>' +
            '<span class="rank-word">' + item.word + '</span>' +
            '<div class="rank-bar"><div class="rank-bar-fill" style="width:' + pct + '%"></div></div>' +
            '<span class="rank-val">' + item.weight + '</span>';
        ranksEl.appendChild(li);
    });

    function initWordCloud() {
        var el = document.getElementById('wordcloud-chart');
        wcChart = echarts.init(el);
        wcChart.setOption({
            tooltip: {
                show: true,
                backgroundColor: 'rgba(10,14,26,0.92)',
                borderColor: 'rgba(99,102,241,0.3)',
                textStyle: { color: '#e2e8f0', fontSize: 14, fontFamily: 'Inter' },
                formatter: function(p) {
                    return '<b style="font-size:16px">' + p.name + '</b><br/>Weight: <b style="color:#a5b4fc">' + p.value + '</b>';
                }
            },
            series: [{
                type: 'wordCloud',
                shape: 'circle',
                gridSize: 10,
                sizeRange: [16, 72],
                rotationRange: [-30, 30],
                rotationStep: 15,
                width: '90%',
                height: '90%',
                textStyle: {
                    fontFamily: 'Inter, sans-serif',
                    fontWeight: '600',
                    color: function() {
                        return COLORS[Math.floor(Math.random() * COLORS.length)];
                    }
                },
                emphasis: {
                    textStyle: {
                        shadowBlur: 12,
                        shadowColor: 'rgba(99,102,241,0.6)',
                        fontWeight: '800'
                    }
                },
                data: wcRaw.map(function(d) { return { name: d.word, value: d.weight }; })
            }]
        });
    }

    /* ===== DDL TRACKER ===== */
    var urgOrder = { high: 0, medium: 1, low: 2 };
    dlRaw.sort(function(a, b) { return (urgOrder[a.urgency] || 3) - (urgOrder[b.urgency] || 3); });

    var currentDdlData = dlRaw;
    var currentUrgencyFilter = 'all';

    var counts = { high: 0, medium: 0, low: 0, all: dlRaw.length };
    dlRaw.forEach(function(d) { counts[d.urgency] = (counts[d.urgency] || 0) + 1; });

    if (counts.high > 0) {
        var badge = document.createElement('span');
        badge.className = 'badge';
        badge.textContent = counts.high;
        document.getElementById('tab-ddl').appendChild(badge);
    }

    var barEl = document.getElementById('ddl-bar');
    [
        { key: 'high', label: 'Urgent', dot: 'high' },
        { key: 'medium', label: 'This Week', dot: 'medium' },
        { key: 'low', label: 'Later', dot: 'low' }
    ].forEach(function(m) {
        if (!counts[m.key]) return;
        var d = document.createElement('div');
        d.className = 'ddl-chip';
        d.innerHTML = '<div class="ddl-dot ' + m.dot + '"></div>' +
            '<div><div class="ddl-chip-num">' + counts[m.key] + '</div><div class="ddl-chip-label">' + m.label + '</div></div>';
        barEl.appendChild(d);
    });

    var filtersEl = document.getElementById('ddl-filters');
    [
        { key: 'all', label: 'All (' + counts.all + ')' },
        { key: 'high', label: 'Urgent (' + (counts.high || 0) + ')' },
        { key: 'medium', label: 'This Week (' + (counts.medium || 0) + ')' },
        { key: 'low', label: 'Later (' + (counts.low || 0) + ')' }
    ].forEach(function(f) {
        var btn = document.createElement('button');
        btn.className = 'ddl-filter-btn' + (f.key === 'all' ? ' active' : '');
        btn.textContent = f.label;
        btn.dataset.filter = f.key;
        btn.addEventListener('click', function() {
            document.querySelectorAll('.ddl-filter-btn').forEach(function(b) { b.classList.remove('active'); });
            this.classList.add('active');
            currentUrgencyFilter = this.dataset.filter;
            renderDDL(this.dataset.filter);
        });
        filtersEl.appendChild(btn);
    });

    function renderDDL(filter) {
        var gridEl = document.getElementById('ddl-grid');
        gridEl.innerHTML = '';
        var items = filter === 'all' ? currentDdlData : currentDdlData.filter(function(d) { return d.urgency === filter; });

        if (items.length === 0) {
            gridEl.innerHTML = '<div class="ddl-empty"><div class="ddl-empty-icon">&#x2705;</div><p>No items in this category</p></div>';
            return;
        }

        function findIndicesBySource(source) {
            if (!source || !emailsRaw.length) return [];
            var src = String(source).trim().toLowerCase();
            if (!src) return [];
            var found = [];
            emailsRaw.forEach(function(em, i) {
                var subj = (em.subject || '').toLowerCase();
                if (subj.indexOf(src) >= 0 || src.indexOf(subj) >= 0) found.push(i);
            });
            return found;
        }

        items.forEach(function(d) {
            var card = document.createElement('div');
            var indices = Array.isArray(d.idx) ? d.idx.filter(function(i) { return typeof i === 'number' && i >= 0 && i < emailsRaw.length; }) : [];
            if (indices.length === 0 && d.source) indices = findIndicesBySource(d.source);
            card.className = 'ddl-card u-' + (d.urgency || 'low') + (indices.length > 0 ? ' clickable' : '');
            var urgLabel = { high: 'URGENT', medium: 'THIS WEEK', low: 'UPCOMING' };
            var cd = '';
            if (d.date) {
                var target = new Date(d.date + 'T23:59:59');
                var diff = Math.ceil((target - new Date()) / 86400000);
                if (diff < 0) cd = Math.abs(diff) + 'd overdue';
                else if (diff === 0) cd = 'Today';
                else if (diff === 1) cd = 'Tomorrow';
                else cd = diff + ' days';
            }
            card.innerHTML =
                '<div class="ddl-tag">' + (urgLabel[d.urgency] || 'UPCOMING') + '</div>' +
                '<div class="ddl-title">' + (d.title || 'Untitled') + '</div>' +
                '<div class="ddl-desc">' + (d.description || d.source || '') + '</div>' +
                '<div class="ddl-meta">' +
                    '<div class="ddl-date">&#x1f4c5; ' + (d.date || 'TBD') + '</div>' +
                    (cd ? '<div class="ddl-cd">' + cd + '</div>' : '') +
                '</div>';
            if (indices.length > 0) {
                card.addEventListener('click', function() { showEmailModal(indices); });
            }
            gridEl.appendChild(card);
        });
    }
    renderDDL('all');

    /* ===== Resize ===== */
    window.addEventListener('resize', function() {
        mmChart.resize();
        if (wcChart) wcChart.resize();
    });
})();
</script>
</body>
</html>"""


def render_dashboard(categories_data, wordcloud_data, deadline_data,
                     emails_data=None, output_file="dashboard.html"):
    """Render the interactive dashboard HTML and open it in the browser."""
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M')
    cat_json = json.dumps(categories_data, ensure_ascii=False)
    wc_json = json.dumps(wordcloud_data, ensure_ascii=False)
    dl_json = json.dumps(deadline_data, ensure_ascii=False)
    emails_json = json.dumps(emails_data or [], ensure_ascii=False)

    html = HTML_TEMPLATE
    html = html.replace("__TIME_NOW__", time_now)
    html = html.replace("__CAT_JSON__", cat_json)
    html = html.replace("__WC_JSON__", wc_json)
    html = html.replace("__DL_JSON__", dl_json)
    html = html.replace("__EMAILS_JSON__", emails_json)

    file_path = os.path.abspath(output_file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Dashboard written to: {file_path}")
    webbrowser.open("file:///" + file_path.replace("\\", "/"))
