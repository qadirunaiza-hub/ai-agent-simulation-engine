<template>
  <router-view />
</template>

<script setup>
import { initTheme } from './store/theme'
initTheme()
</script>

<style>
/* ── CSS Theme Variables ── */
:root, [data-theme="light"] {
  --bg:          #F8F9FC;
  --bg2:         #FFFFFF;
  --bg3:         #EEF0F6;
  --surface:     #FFFFFF;
  --border:      #DDE1EC;
  --border2:     #C8CEDD;
  --text:        #0A0E1A;
  --text2:       #374151;
  --text3:       #6B7280;
  --accent:      #FF4500;
  --accent2:     #7C3AED;
  --neon:        #FF4500;
  --neon-dim:    #CC3300;
  --neon-glow:   0 0 8px rgba(255,69,0,0.5), 0 0 20px rgba(255,69,0,0.25);
  --navbar-bg:   #0A0E1A;
  --navbar-text: #FFFFFF;
  --tag-bg:      #0A0E1A;
  --tag-text:    #FF4500;
  --btn-primary: #0A0E1A;
  --btn-text:    #FFFFFF;
  --scrollbar-track: #EEF0F6;
  --scrollbar-thumb: #FF4500;
}

[data-theme="dark"] {
  --bg:          #03030a;
  --bg2:         #0b0b15;
  --bg3:         #111122;
  --surface:     #0b0b15;
  --border:      rgba(255,255,255,.07);
  --border2:     rgba(255,255,255,.12);
  --text:        #E2E8F0;
  --text2:       #A0AEC0;
  --text3:       #718096;
  --accent:      #f97316;
  --accent2:     #A78BFA;
  --neon:        #f97316;
  --neon-dim:    #ea580c;
  --neon-glow:   0 0 8px rgba(249,115,22,0.6), 0 0 20px rgba(249,115,22,0.3), 0 0 40px rgba(234,88,12,0.15);
  --navbar-bg:   #040710;
  --navbar-text: #E2E8F0;
  --tag-bg:      rgba(249,115,22,.1);
  --tag-text:    #f97316;
  --btn-primary: rgba(249,115,22,.15);
  --btn-text:    #f97316;
  --scrollbar-track: transparent;
  --scrollbar-thumb: rgba(255,255,255,0.15);
}

/* ── Reset ── */
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

html { transition: background-color 0.3s, color 0.3s; }
body { background: var(--bg); color: var(--text); }

#app {
  font-family: 'JetBrains Mono', 'Space Grotesk', system-ui, monospace;
  -webkit-font-smoothing: antialiased;
  min-height: 100vh;
  background: var(--bg);
  color: var(--text);
  transition: background 0.3s, color 0.3s;
}

button { font-family: inherit; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: transparent; border-radius: 3px; }
html:hover ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.28) !important; }

/* ── Global home page styles (theme-aware) ── */
.home-container {
  min-height: 100vh;
  background: var(--bg);
  color: var(--text);
  font-family: 'Space Grotesk', system-ui, sans-serif;
  transition: background 0.3s, color 0.3s;
}

.navbar {
  height: 60px;
  background: var(--navbar-bg);
  color: var(--navbar-text);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  border-bottom: 1px solid rgba(0,255,200,0.1);
}

.nav-brand {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  letter-spacing: 1px;
  font-size: 1rem;
  color: var(--navbar-text);
}

.nav-brand .brand-accent { color: var(--neon); }

.nav-links {
  display: flex;
  align-items: center;
  gap: 18px;
}

.github-link {
  color: var(--navbar-text);
  text-decoration: none;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  opacity: 0.7;
  transition: opacity 0.2s;
}
.github-link:hover { opacity: 1; }

.theme-toggle {
  background: transparent;
  border: 1px solid var(--border2);
  color: var(--navbar-text);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  transition: all 0.2s;
}
.theme-toggle:hover { border-color: var(--neon); color: var(--neon); }

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* Hero */
.hero-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 80px;
  gap: 60px;
}

.hero-left { flex: 1; }

.tag-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 28px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
}

.neon-tag {
  background: var(--tag-bg);
  color: var(--tag-text);
  padding: 4px 10px;
  font-weight: 700;
  letter-spacing: 1.5px;
  font-size: 0.7rem;
  border: 1px solid var(--neon);
  box-shadow: var(--neon-glow);
  text-transform: uppercase;
}

.version-text { color: var(--text3); font-weight: 500; letter-spacing: 0.5px; }

.main-title {
  font-size: 4rem;
  line-height: 1.15;
  font-weight: 600;
  margin: 0 0 36px 0;
  letter-spacing: -1.5px;
  color: var(--text);
}

.gradient-text {
  background: linear-gradient(90deg, var(--neon) 0%, var(--accent2) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.hero-desc {
  font-size: 1rem;
  line-height: 1.85;
  color: var(--text2);
  max-width: 600px;
  margin-bottom: 40px;
  text-align: justify;
}

.hero-desc p { margin-bottom: 1.2rem; }

.hl-brand { color: var(--text); font-weight: 700; }
.hl-neon  { color: var(--neon); font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.hl-code  {
  background: var(--bg3);
  padding: 2px 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.88em;
  color: var(--neon);
  font-weight: 600;
  border: 1px solid var(--border);
}

.slogan-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text);
  letter-spacing: 0.5px;
  border-left: 3px solid var(--neon);
  padding-left: 14px;
  margin-top: 20px;
  line-height: 1.4;
}

.blinking-cursor { color: var(--neon); animation: blink 1s step-end infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

.decoration-square { width: 12px; height: 12px; background: var(--neon); margin-top: 20px; box-shadow: var(--neon-glow); }

/* Hero right — fish */
.hero-right {
  flex: 0.75;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-start;
  gap: 20px;
  padding-top: 10px;
}

.fish-container {
  width: 100%;
  max-width: 460px;
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.scroll-down-btn {
  width: 36px;
  height: 36px;
  border: 1px solid var(--border2);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--neon);
  font-size: 1.1rem;
  transition: all 0.2s;
}
.scroll-down-btn:hover { border-color: var(--neon); box-shadow: var(--neon-glow); }

/* Dashboard */
.dashboard-section {
  display: flex;
  gap: 60px;
  border-top: 1px solid var(--border);
  padding-top: 60px;
  align-items: flex-start;
}

.left-panel { flex: 0.85; display: flex; flex-direction: column; }
.right-panel { flex: 1.2; display: flex; flex-direction: column; }

.panel-header {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--text3);
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 18px;
}

.status-dot { color: var(--neon); font-size: 0.75rem; }

.section-title { font-size: 1.8rem; font-weight: 600; margin: 0 0 12px 0; color: var(--text); }
.section-desc { color: var(--text2); margin-bottom: 24px; line-height: 1.6; font-size: 0.92rem; }

.metrics-row { display: flex; gap: 16px; margin-bottom: 16px; }

.metric-card {
  border: 1px solid var(--border);
  padding: 18px 26px;
  min-width: 140px;
  background: var(--bg2);
  transition: border-color 0.2s;
}
.metric-card:hover { border-color: var(--neon); }

.metric-value { font-family: 'JetBrains Mono', monospace; font-size: 1.6rem; font-weight: 700; margin-bottom: 4px; color: var(--neon); }
.metric-label { font-size: 0.78rem; color: var(--text3); }

.steps-container { border: 1px solid var(--border); padding: 28px; background: var(--bg2); }
.steps-header {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--text3);
  margin-bottom: 22px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.diamond-icon { font-size: 1.1rem; color: var(--neon); }
.workflow-list { display: flex; flex-direction: column; gap: 18px; }
.workflow-item { display: flex; align-items: flex-start; gap: 18px; }
.step-num { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--neon); opacity: 0.5; }
.step-info { flex: 1; }
.step-title { font-weight: 600; font-size: 0.95rem; margin-bottom: 3px; color: var(--text); }
.step-desc { font-size: 0.82rem; color: var(--text3); line-height: 1.4; }

/* Console / Upload */
.console-box { border: 1px solid var(--border); padding: 6px; background: var(--bg2); }
.console-section { padding: 18px; }
.console-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 14px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: var(--text3);
}
.upload-zone {
  border: 1px dashed var(--border2);
  height: 180px;
  overflow-y: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: var(--bg3);
  transition: all 0.25s;
}
.upload-zone:hover { background: var(--bg2); border-color: var(--neon); box-shadow: inset 0 0 20px rgba(0,255,200,0.03); }
.upload-placeholder { text-align: center; }
.upload-icon { width: 38px; height: 38px; border: 1px solid var(--border2); display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; color: var(--neon); }
.upload-title { font-weight: 500; font-size: 0.88rem; margin-bottom: 4px; color: var(--text2); }
.upload-hint { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--text3); }
.file-list { width: 100%; padding: 12px; display: flex; flex-direction: column; gap: 8px; }
.file-item { display: flex; align-items: center; background: var(--bg); padding: 7px 10px; border: 1px solid var(--border); font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: var(--text2); }
.file-name { flex: 1; margin: 0 10px; }
.remove-btn { background: none; border: none; cursor: pointer; font-size: 1.1rem; color: var(--text3); }
.remove-btn:hover { color: #ef4444; }

.console-divider { display: flex; align-items: center; margin: 8px 0; border-top: 1px solid var(--border); }
.console-divider span { padding: 0 14px; font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: var(--text3); letter-spacing: 1px; }

.input-wrapper { position: relative; border: 1px solid var(--border); background: var(--bg3); }
.code-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 18px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.88rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  min-height: 140px;
  color: var(--text);
}
.code-input::placeholder { color: var(--text3); }
.model-badge { position: absolute; bottom: 8px; right: 12px; font-family: 'JetBrains Mono', monospace; font-size: 0.67rem; color: var(--text3); }

.start-engine-btn {
  width: 100%;
  background: var(--btn-primary);
  color: var(--btn-text);
  border: 1px solid var(--neon);
  padding: 18px 24px;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  font-size: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  letter-spacing: 1px;
  transition: all 0.25s;
  box-shadow: var(--neon-glow);
}
.start-engine-btn:hover:not(:disabled) { filter: brightness(1.15); transform: translateY(-2px); }
.start-engine-btn:disabled { background: var(--bg3); color: var(--text3); border-color: var(--border); cursor: not-allowed; box-shadow: none; transform: none; }

@media (max-width: 1024px) {
  .hero-section, .dashboard-section { flex-direction: column; }
  .hero-right { align-items: flex-start; }
  .fish-container { max-width: 100%; min-height: 200px; }
}

/* ═══════════════════════════════════════════════
   GLOBAL DARK-MODE OVERRIDES
   Covers inner views / step components that still
   have scoped styles not yet using CSS variables.
   Using [data-theme="dark"] + class for specificity.
   ═══════════════════════════════════════════════ */

[data-theme="dark"] .main-view,
[data-theme="dark"] .simulation-view,
[data-theme="dark"] .simulation-run-view,
[data-theme="dark"] .report-view,
[data-theme="dark"] .interaction-view {
  background: var(--bg) !important;
  color: var(--text) !important;
}

/* ── Inner app header ── */
[data-theme="dark"] .app-header {
  background: var(--bg2) !important;
  border-bottom-color: var(--border) !important;
  color: var(--text) !important;
}

[data-theme="dark"] .brand        { color: var(--text) !important; }
[data-theme="dark"] .step-name    { color: var(--text) !important; }
[data-theme="dark"] .step-num     { color: var(--text3) !important; }
[data-theme="dark"] .status-indicator { color: var(--text2) !important; }

/* View switcher */
[data-theme="dark"] .view-switcher  { background: var(--bg3) !important; }
[data-theme="dark"] .switch-btn     { color: var(--text3) !important; background: transparent !important; }
[data-theme="dark"] .switch-btn.active { background: var(--bg2) !important; color: var(--text) !important; box-shadow: 0 2px 8px rgba(0,0,0,0.4) !important; }

/* Step dividers */
[data-theme="dark"] .step-divider { background: var(--border) !important; }

/* Panels and content areas */
[data-theme="dark"] .panel-wrapper  { background: var(--bg2) !important; border-color: var(--border) !important; }
[data-theme="dark"] .content-area   { background: var(--bg) !important; }
[data-theme="dark"] .right-panel-content,
[data-theme="dark"] .left-panel-content { background: var(--bg2) !important; }

/* All inner panels, cards, boxes */
[data-theme="dark"] .card,
[data-theme="dark"] .panel,
[data-theme="dark"] .section-card,
[data-theme="dark"] .config-panel,
[data-theme="dark"] .info-panel,
[data-theme="dark"] .detail-panel,
[data-theme="dark"] .stats-card,
[data-theme="dark"] .agent-card,
[data-theme="dark"] .round-card,
[data-theme="dark"] .action-item,
[data-theme="dark"] .post-card,
[data-theme="dark"] .comment-card,
[data-theme="dark"] .profile-card,
[data-theme="dark"] .report-section,
[data-theme="dark"] .chat-message {
  background: var(--bg2) !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
}

/* Form elements */
[data-theme="dark"] input:not([type="checkbox"]):not([type="radio"]):not([type="range"]),
[data-theme="dark"] textarea,
[data-theme="dark"] select {
  background: var(--bg3) !important;
  color: var(--text) !important;
  border-color: var(--border) !important;
}
[data-theme="dark"] input::placeholder,
[data-theme="dark"] textarea::placeholder { color: var(--text3) !important; }
[data-theme="dark"] input:focus,
[data-theme="dark"] textarea:focus { border-color: var(--neon) !important; }

/* Scrollable areas */
[data-theme="dark"] .scroll-area,
[data-theme="dark"] .content-scroll,
[data-theme="dark"] .log-area,
[data-theme="dark"] .actions-list,
[data-theme="dark"] .posts-list,
[data-theme="dark"] .timeline-list { background: var(--bg) !important; }

/* Sidebar navigation */
[data-theme="dark"] .sidebar,
[data-theme="dark"] .step-sidebar,
[data-theme="dark"] .nav-sidebar { background: var(--bg2) !important; border-color: var(--border) !important; }

[data-theme="dark"] .sidebar-item,
[data-theme="dark"] .step-item    { color: var(--text2) !important; }
[data-theme="dark"] .sidebar-item.active,
[data-theme="dark"] .step-item.active { color: var(--neon) !important; background: rgba(0,255,200,0.06) !important; }

/* Buttons that use hardcoded black */
[data-theme="dark"] button.primary-btn,
[data-theme="dark"] button.action-btn,
[data-theme="dark"] button.submit-btn:not(.neon-btn) {
  background: var(--bg3) !important;
  color: var(--text) !important;
  border-color: var(--border) !important;
}

/* Labels, headings, generic text */
[data-theme="dark"] label { color: var(--text2) !important; }
[data-theme="dark"] h1, [data-theme="dark"] h2,
[data-theme="dark"] h3, [data-theme="dark"] h4 { color: var(--text) !important; }
[data-theme="dark"] p:not(.neon):not([class*="status"]) { color: var(--text2) !important; }

/* Borders */
[data-theme="dark"] hr { border-color: var(--border) !important; }
[data-theme="dark"] .divider,
[data-theme="dark"] .separator { background: var(--border) !important; border-color: var(--border) !important; }

/* QuestionBanner and ScrapeBanner already dark, keep intact */

/* ModelChooser dropdown */
[data-theme="dark"] .model-dropdown {
  background: var(--bg2) !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
}
[data-theme="dark"] .model-dropdown .dropdown-header { background: var(--bg3) !important; color: var(--text2) !important; border-color: var(--border) !important; }
[data-theme="dark"] .model-option { color: var(--text) !important; }
[data-theme="dark"] .model-option:hover { background: var(--bg3) !important; }
[data-theme="dark"] .model-option.selected { background: rgba(0,255,200,0.08) !important; color: var(--neon) !important; }
[data-theme="dark"] .model-btn { background: var(--bg3) !important; border-color: var(--border) !important; color: var(--text) !important; }
[data-theme="dark"] .server-input { background: var(--bg) !important; color: var(--text) !important; border-color: var(--border) !important; }
[data-theme="dark"] .server-status,
[data-theme="dark"] .server-label { color: var(--text3) !important; }
[data-theme="dark"] .custom-input { background: var(--bg) !important; color: var(--text) !important; border-color: var(--border) !important; }
[data-theme="dark"] .qwen-rec { background: rgba(0,255,200,0.05) !important; border-color: rgba(0,255,200,0.1) !important; color: var(--text2) !important; }
[data-theme="dark"] .no-models,
[data-theme="dark"] .dropdown-loading { color: var(--text3) !important; }
[data-theme="dark"] .dropdown-error { color: #f87171 !important; }
[data-theme="dark"] .model-list-header { color: var(--text3) !important; }

/* HistoryDatabase in dark */
[data-theme="dark"] .project-card { background: var(--bg2) !important; border-color: var(--border) !important; }
[data-theme="dark"] .card-title  { color: var(--text) !important; }
[data-theme="dark"] .card-desc   { color: var(--text3) !important; }
[data-theme="dark"] .card-id     { color: var(--text3) !important; }
[data-theme="dark"] .card-footer { border-top-color: var(--border) !important; color: var(--text3) !important; }
[data-theme="dark"] .card-files-wrapper { background: var(--bg3) !important; border-color: var(--border) !important; }
[data-theme="dark"] .file-item   { background: var(--bg2) !important; }
[data-theme="dark"] .file-name   { color: var(--text2) !important; }
[data-theme="dark"] .modal-content { background: var(--bg2) !important; border-color: var(--border) !important; }
[data-theme="dark"] .modal-header { background: var(--bg2) !important; border-color: var(--border) !important; }
[data-theme="dark"] .modal-id,
[data-theme="dark"] .modal-file-name { color: var(--text) !important; }
[data-theme="dark"] .modal-requirement { background: var(--bg3) !important; border-color: var(--border) !important; color: var(--text2) !important; }
[data-theme="dark"] .modal-btn   { background: var(--bg2) !important; border-color: var(--border) !important; }
[data-theme="dark"] .modal-btn .btn-text { color: var(--text2) !important; }
[data-theme="dark"] .modal-empty { background: var(--bg3) !important; border-color: var(--border) !important; color: var(--text3) !important; }
[data-theme="dark"] .hint-text   { color: var(--text3) !important; }
[data-theme="dark"] .section-title.history-title,
[data-theme="dark"] .section-header .section-title { color: var(--text3) !important; }

/* Step components generic containers */
[data-theme="dark"] .step-content,
[data-theme="dark"] .step-body,
[data-theme="dark"] .step-container,
[data-theme="dark"] .step-panel { background: var(--bg2) !important; color: var(--text) !important; }

/* Graph panel */
[data-theme="dark"] .graph-panel,
[data-theme="dark"] .graph-container { background: var(--bg) !important; }

/* ── Entity / relation tags — make them neon chips ── */
[data-theme="dark"] .entity-tag,
[data-theme="dark"] .relation-tag,
[data-theme="dark"] .example-tag,
[data-theme="dark"] .tag-chip {
  background: rgba(0,255,200,0.07) !important;
  border-color: rgba(0,255,200,0.35) !important;
  color: var(--neon) !important;
}
[data-theme="dark"] .entity-tag.clickable:hover,
[data-theme="dark"] .relation-tag:hover {
  background: rgba(0,255,200,0.15) !important;
  border-color: var(--neon) !important;
  box-shadow: 0 0 8px rgba(0,255,200,0.2) !important;
}

/* Tag section label */
[data-theme="dark"] .tag-label,
[data-theme="dark"] .tags-label,
[data-theme="dark"] .section-subtitle,
[data-theme="dark"] .api-note,
[data-theme="dark"] .hint,
[data-theme="dark"] .hint-row,
[data-theme="dark"] .sub-label { color: var(--neon) !important; opacity: 0.7; }

/* Overlays — white popups in dark mode */
[data-theme="dark"] .ontology-detail-overlay,
[data-theme="dark"] .detail-overlay,
[data-theme="dark"] .popup-overlay,
[data-theme="dark"] .modal-overlay-inner {
  background: var(--bg2) !important;
  border-color: var(--border) !important;
}
[data-theme="dark"] .detail-type-badge {
  background: var(--neon) !important;
  color: var(--bg) !important;
}
[data-theme="dark"] .detail-name { color: var(--text) !important; }
[data-theme="dark"] .detail-desc,
[data-theme="dark"] .attr-item  { color: var(--text2) !important; border-color: var(--border) !important; }
[data-theme="dark"] .detail-section h4,
[data-theme="dark"] .detail-section .section-label { color: var(--neon) !important; opacity: 0.7; }
[data-theme="dark"] .conn-item { background: var(--bg3) !important; color: var(--text2) !important; border-color: var(--border) !important; }

/* Progress bars */
[data-theme="dark"] .progress-bar-bg,
[data-theme="dark"] .progress-track { background: var(--bg3) !important; }
[data-theme="dark"] .progress-bar-fill,
[data-theme="dark"] .progress-fill  { background: var(--neon) !important; }

/* Badge states */
[data-theme="dark"] .badge.pending  { background: var(--bg3) !important; color: var(--text3) !important; border: 1px solid var(--border) !important; }
[data-theme="dark"] .badge.success  { background: rgba(16,185,129,0.15) !important; color: #10B981 !important; border: 1px solid rgba(16,185,129,0.3) !important; }
[data-theme="dark"] .badge.processing { background: rgba(255,69,0,0.15) !important; color: #FF6B35 !important; border: 1px solid rgba(255,69,0,0.3) !important; }

/* Step card boxes */
[data-theme="dark"] .step-card,
[data-theme="dark"] .phase-card,
[data-theme="dark"] .task-card,
[data-theme="dark"] .config-card {
  background: var(--bg2) !important;
  border-color: var(--border) !important;
}
[data-theme="dark"] .step-card:hover,
[data-theme="dark"] .phase-card:hover { border-color: var(--neon) !important; }

[data-theme="dark"] .step-card .step-title,
[data-theme="dark"] .phase-title,
[data-theme="dark"] .task-title      { color: var(--text) !important; }
[data-theme="dark"] .step-card .step-desc,
[data-theme="dark"] .phase-desc,
[data-theme="dark"] .task-desc       { color: var(--text2) !important; }

/* All description/paragraph text in inner panels */
[data-theme="dark"] .desc,
[data-theme="dark"] .description,
[data-theme="dark"] .body-text       { color: var(--text2) !important; }

/* Any leftover white/near-white small text */
[data-theme="dark"] small,
[data-theme="dark"] .text-muted,
[data-theme="dark"] .caption,
[data-theme="dark"] .meta-text,
[data-theme="dark"] .log-line,
[data-theme="dark"] .console-line    { color: var(--text3) !important; }

/* Log / console output */
[data-theme="dark"] .log-container,
[data-theme="dark"] .console-output,
[data-theme="dark"] .log-panel       { background: var(--bg) !important; border-color: var(--border) !important; }
[data-theme="dark"] .log-text        { color: var(--text2) !important; }
[data-theme="dark"] .log-timestamp   { color: var(--text3) !important; }
[data-theme="dark"] .log-info        { color: var(--neon) !important; }
[data-theme="dark"] .log-warn        { color: #F59E0B !important; }
[data-theme="dark"] .log-error       { color: #EF4444 !important; }

/* Tables */
[data-theme="dark"] table { background: var(--bg2) !important; color: var(--text) !important; }
[data-theme="dark"] th    { background: var(--bg3) !important; color: var(--neon) !important; border-color: var(--border) !important; }
[data-theme="dark"] td    { border-color: var(--border) !important; color: var(--text2) !important; }
[data-theme="dark"] tr:hover td { background: rgba(0,255,200,0.04) !important; }

/* View switcher in graph panel */
[data-theme="dark"] .graph-view-switcher,
[data-theme="dark"] .panel-tabs { background: var(--bg3) !important; border-color: var(--border) !important; }
[data-theme="dark"] .panel-tab  { color: var(--text3) !important; }
[data-theme="dark"] .panel-tab.active { color: var(--neon) !important; border-bottom-color: var(--neon) !important; }

/* Stat / metric labels */
[data-theme="dark"] .stat-label,
[data-theme="dark"] .metric-label-inner { color: var(--text3) !important; }
[data-theme="dark"] .stat-value,
[data-theme="dark"] .metric-value-inner { color: var(--neon) !important; }

/* Close buttons */
[data-theme="dark"] .close-btn { color: var(--text3) !important; background: transparent !important; border: none !important; }
[data-theme="dark"] .close-btn:hover { color: var(--text) !important; }

/* Tooltips */
[data-theme="dark"] .tooltip,
[data-theme="dark"] [data-tooltip] { background: var(--bg2) !important; color: var(--text) !important; border-color: var(--border) !important; }

/* Graph legend */
[data-theme="dark"] .graph-legend,
[data-theme="dark"] .legend-item,
[data-theme="dark"] .entity-legend  { background: var(--bg2) !important; border-color: var(--border) !important; }
[data-theme="dark"] .legend-label   { color: var(--text2) !important; }
[data-theme="dark"] .legend-title   { color: var(--neon) !important; }

/* Simulation run panels */
[data-theme="dark"] .round-info,
[data-theme="dark"] .action-row,
[data-theme="dark"] .agent-info     { background: var(--bg2) !important; border-color: var(--border) !important; color: var(--text2) !important; }
[data-theme="dark"] .round-num,
[data-theme="dark"] .agent-name     { color: var(--neon) !important; }

/* Report view */
[data-theme="dark"] .report-content,
[data-theme="dark"] .report-block,
[data-theme="dark"] .insight-card   { background: var(--bg2) !important; border-color: var(--border) !important; }
[data-theme="dark"] .report-content h1,
[data-theme="dark"] .report-content h2,
[data-theme="dark"] .report-content h3 { color: var(--neon) !important; }
[data-theme="dark"] .report-content p,
[data-theme="dark"] .report-content li { color: var(--text2) !important; }
[data-theme="dark"] .report-content code,
[data-theme="dark"] .report-content pre { background: var(--bg3) !important; color: var(--neon) !important; border-color: var(--border) !important; }
[data-theme="dark"] .report-content blockquote { border-left-color: var(--neon) !important; background: rgba(0,255,200,0.05) !important; }
[data-theme="dark"] .report-content a { color: var(--neon) !important; }

/* Interaction/chat */
[data-theme="dark"] .chat-input-area { background: var(--bg2) !important; border-color: var(--border) !important; }
[data-theme="dark"] .agent-bubble    { background: var(--bg3) !important; color: var(--text) !important; }
[data-theme="dark"] .user-bubble     { background: rgba(0,255,200,0.1) !important; color: var(--text) !important; border-color: rgba(0,255,200,0.3) !important; }
[data-theme="dark"] .agent-label     { color: var(--neon) !important; }

/* HistoryDatabase — force dark on cards */
[data-theme="dark"] .history-database { background: transparent !important; }
[data-theme="dark"] .project-card     { background: var(--bg2) !important; border-color: var(--border) !important; color: var(--text) !important; }
[data-theme="dark"] .project-card:hover { border-color: var(--neon) !important; box-shadow: 0 0 20px rgba(0,255,200,0.08) !important; }
[data-theme="dark"] .section-line { background: linear-gradient(90deg, transparent, var(--border), transparent) !important; }
[data-theme="dark"] .empty-file-icon,
[data-theme="dark"] .empty-file-text { color: var(--text3) !important; }
</style>
