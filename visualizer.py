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
    <div class="header-meta">__TIME_NOW__</div>
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
            <p>Click nodes to expand/collapse &middot; Scroll to zoom &middot; Drag to pan</p>
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

<script>
(function() {
    var categories = __CAT_JSON__;
    var wcRaw      = __WC_JSON__;
    var dlRaw      = __DL_JSON__;

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
    function buildTree(cats) {
        var entries = Object.entries(cats);
        var children = entries.map(function(entry, i) {
            var cat = entry[0], items = entry[1];
            var c = COLORS[i % COLORS.length];
            var list = Array.isArray(items) ? items : [String(items)];
            return {
                name: cat,
                itemStyle: { color: c, borderColor: c },
                lineStyle: { color: c, opacity: 0.5 },
                children: list.filter(Boolean).map(function(t) {
                    return {
                        name: String(t),
                        itemStyle: { color: c, borderColor: c, opacity: 0.75 },
                        lineStyle: { color: c, opacity: 0.35 }
                    };
                })
            };
        });
        return {
            name: 'Email Hub',
            itemStyle: { color: '#6366f1', borderColor: '#818cf8', borderWidth: 3 },
            children: children
        };
    }

    var treeData = buildTree(categories);
    var mmChart = echarts.init(document.getElementById('mindmap-chart'));

    function mmOption(layout) {
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
                    return p.name;
                }
            },
            series: [{
                type: 'tree',
                data: [treeData],
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
            mmChart.setOption(mmOption(this.dataset.layout), true);
        });
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
            renderDDL(this.dataset.filter);
        });
        filtersEl.appendChild(btn);
    });

    function renderDDL(filter) {
        var gridEl = document.getElementById('ddl-grid');
        gridEl.innerHTML = '';
        var items = filter === 'all' ? dlRaw : dlRaw.filter(function(d) { return d.urgency === filter; });

        if (items.length === 0) {
            gridEl.innerHTML = '<div class="ddl-empty"><div class="ddl-empty-icon">&#x2705;</div><p>No items in this category</p></div>';
            return;
        }

        items.forEach(function(d) {
            var card = document.createElement('div');
            card.className = 'ddl-card u-' + (d.urgency || 'low');
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
                     output_file="dashboard.html"):
    """Render the interactive dashboard HTML and open it in the browser."""
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M')
    cat_json = json.dumps(categories_data, ensure_ascii=False)
    wc_json = json.dumps(wordcloud_data, ensure_ascii=False)
    dl_json = json.dumps(deadline_data, ensure_ascii=False)

    html = HTML_TEMPLATE
    html = html.replace("__TIME_NOW__", time_now)
    html = html.replace("__CAT_JSON__", cat_json)
    html = html.replace("__WC_JSON__", wc_json)
    html = html.replace("__DL_JSON__", dl_json)

    file_path = os.path.abspath(output_file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Dashboard written to: {file_path}")
    webbrowser.open("file:///" + file_path.replace("\\", "/"))
