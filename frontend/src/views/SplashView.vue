<template>
  <div class="splash">
    <div class="splash-card">
      <!-- Fish + Brand -->
      <div class="splash-header">
        <svg class="splash-fish" viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" fill="none">
          <defs>
            <filter id="sf"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
          </defs>
          <g filter="url(#sf)">
            <path d="M 45 60 L 10 35 L 10 85 Z" stroke="currentColor" stroke-width="2.2" fill="none"/>
            <ellipse cx="110" cy="60" rx="65" ry="36" stroke="currentColor" stroke-width="2.5" fill="none"/>
            <ellipse cx="110" cy="60" rx="65" ry="36" stroke="currentColor" stroke-width="10" fill="none" opacity="0.06"/>
            <path d="M 96 26 Q 112 4 130 26" stroke="currentColor" stroke-width="2" fill="none"/>
            <path d="M 114 78 Q 103 96 90 88" stroke="currentColor" stroke-width="1.6" fill="none" opacity="0.8"/>
            <path d="M 148 32 Q 151 60 148 88" stroke="currentColor" stroke-width="1.4" fill="none" opacity="0.55"/>
            <path d="M 128 28 Q 125 60 128 92" stroke="currentColor" stroke-width="0.8" opacity="0.28"/>
            <path d="M 110 28 Q 108 60 110 92" stroke="currentColor" stroke-width="0.8" opacity="0.28"/>
            <circle cx="165" cy="50" r="9" stroke="currentColor" stroke-width="2.2" fill="none"/>
            <circle cx="167" cy="48" r="4.5" fill="currentColor"/>
            <circle cx="168.5" cy="46.5" r="2" fill="#070B14" opacity="0.8"/>
            <circle cx="170" cy="45" r="1" fill="white" opacity="0.7"/>
            <path d="M 177 62 Q 182 67 177 72" stroke="currentColor" stroke-width="1.8" fill="none"/>
          </g>
        </svg>
        <div class="splash-titles">
          <div class="splash-brand">MIROFISH</div>
          <div class="splash-mu">× MU SIGMA</div>
        </div>
      </div>

      <div class="splash-tagline">Decision Intelligence Simulation Platform</div>

      <!-- How-to -->
      <div class="instructions">
        <div class="inst-title">Getting Started</div>
        <ol class="inst-list">
          <li>
            <span class="step-badge">01</span>
            <div>
              <strong>Upload Documents</strong>
              <p>Drop in PDF, TXT, MD, or JSON files — reports, surveys, org charts, datasets, policy documents.</p>
            </div>
          </li>
          <li>
            <span class="step-badge">02</span>
            <div>
              <strong>Write a Simulation Prompt</strong>
              <p>Describe in plain language what you want to predict (e.g. "How will employees react if remote work policy changes?").</p>
            </div>
          </li>
          <li>
            <span class="step-badge">03</span>
            <div>
              <strong>Configure Your LLM</strong>
              <p>Click the model badge (top-right) to connect your local Ollama server. <strong>qwen2.5:32b</strong> is recommended.</p>
            </div>
          </li>
          <li>
            <span class="step-badge">04</span>
            <div>
              <strong>Run the Simulation</strong>
              <p>MiroFish builds a knowledge graph, generates agent personas, and runs a fully local multi-agent social simulation.</p>
            </div>
          </li>
          <li>
            <span class="step-badge">05</span>
            <div>
              <strong>Analyse &amp; Interact</strong>
              <p>Review the AI-generated insight report, then interview individual agents to probe their reasoning directly.</p>
            </div>
          </li>
        </ol>

        <div class="req-block">
          <div class="req-title">Platform Requirements</div>
          <ul class="req-list">
            <li>Ollama running locally or on a reachable host</li>
            <li>Neo4j 5.18+ (bundled via Docker Compose)</li>
            <li>Recommended model: <code>qwen2.5:32b</code></li>
            <li>All data stays within Mu Sigma infrastructure</li>
          </ul>
        </div>
      </div>

      <!-- Footer -->
      <div class="splash-footer">
        <div class="countdown-bar-wrap">
          <div class="countdown-bar" :style="{ width: progressPct + '%' }"></div>
        </div>
        <div class="footer-row">
          <span class="countdown-text">Continuing in {{ remaining }}s…</span>
          <button class="skip-btn" @click="goHome">Enter MiroFish →</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const DURATION = 5
const router = useRouter()
const elapsed = ref(0)
const remaining = computed(() => Math.max(0, DURATION - elapsed.value))
const progressPct = computed(() => Math.min(100, (elapsed.value / DURATION) * 100))
let timer = null

const goHome = () => {
  sessionStorage.setItem('mirofish_splash_seen', '1')
  router.replace({ name: 'Home' })
}

onMounted(() => {
  timer = setInterval(() => { elapsed.value++; if (elapsed.value >= DURATION) goHome() }, 1000)
})
onUnmounted(() => clearInterval(timer))
</script>

<style scoped>
.splash {
  min-height: 100vh;
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
  font-family: 'Space Grotesk', system-ui, sans-serif;
  background-image:
    linear-gradient(rgba(0,255,200,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,255,200,0.04) 1px, transparent 1px);
  background-size: 40px 40px;
}

.splash-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  max-width: 680px;
  width: 100%;
  padding: 44px 44px 28px;
  box-shadow: 0 0 60px rgba(0,255,200,0.05);
}

/* Header */
.splash-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 8px;
}

.splash-fish {
  width: 100px;
  height: 56px;
  color: var(--neon);
  filter: drop-shadow(0 0 5px var(--neon)) drop-shadow(0 0 14px var(--neon-dim));
  animation: splashFloat 3s ease-in-out infinite;
}
@keyframes splashFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }

.splash-titles { line-height: 1.2; }
.splash-brand {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: 2px;
  color: var(--text);
}
.splash-mu {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: var(--neon);
  text-shadow: 0 0 8px var(--neon);
}

.splash-tagline {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--text3);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 32px;
}

/* Instructions */
.instructions {
  border: 1px solid var(--border);
  padding: 24px 24px 18px;
  margin-bottom: 24px;
  background: var(--bg3);
}

.inst-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text3);
  margin-bottom: 18px;
}

.inst-list {
  list-style: none;
  padding: 0;
  margin: 0 0 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.inst-list li {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.step-badge {
  background: var(--neon);
  color: var(--bg);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.62rem;
  font-weight: 800;
  padding: 3px 6px;
  flex-shrink: 0;
  margin-top: 2px;
  box-shadow: 0 0 8px var(--neon);
}

.inst-list li strong { display: block; font-size: 0.92rem; font-weight: 600; margin-bottom: 3px; color: var(--text); }
.inst-list li p { font-size: 0.82rem; color: var(--text3); margin: 0; line-height: 1.5; }

.req-block { border-top: 1px solid var(--border); padding-top: 14px; }
.req-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text3);
  margin-bottom: 8px;
}
.req-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 4px; }
.req-list li { font-size: 0.8rem; color: var(--text2); padding-left: 14px; position: relative; }
.req-list li::before { content: '→'; position: absolute; left: 0; color: var(--neon); font-size: 0.68rem; }
.req-list code { font-family: 'JetBrains Mono', monospace; background: var(--bg); padding: 1px 5px; font-size: 0.78rem; color: var(--neon); border: 1px solid var(--border); }

/* Footer */
.splash-footer { border-top: 1px solid var(--border); padding-top: 18px; }
.countdown-bar-wrap { background: var(--bg3); height: 2px; margin-bottom: 14px; overflow: hidden; }
.countdown-bar { height: 100%; background: var(--neon); box-shadow: 0 0 6px var(--neon); transition: width 1s linear; }
.footer-row { display: flex; justify-content: space-between; align-items: center; }
.countdown-text { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--text3); }
.skip-btn {
  background: var(--btn-primary);
  color: var(--btn-text);
  border: 1px solid var(--neon);
  padding: 9px 22px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  letter-spacing: 0.5px;
  transition: all 0.15s;
  box-shadow: var(--neon-glow);
}
.skip-btn:hover { filter: brightness(1.15); transform: translateY(-1px); }
</style>
