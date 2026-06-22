<template>
  <div class="home-container">
    <canvas ref="starCanvas" class="star-bg"></canvas>
    <div class="orb orb1"></div>
    <div class="orb orb2"></div>
    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-brand">
        MIROFISH <span class="brand-accent">×</span> MU SIGMA
      </div>
      <div class="nav-links">
        <button class="theme-toggle" @click="toggleTheme" :title="isDark ? 'Switch to light' : 'Switch to dark'">
          {{ isDark ? '☀' : '🌙' }}
        </button>
        <span v-if="currentUser" class="user-badge">
          <span v-if="currentUser.role === 'admin'" class="star">★</span>
          {{ currentUser.username }}
        </span>
        <a href="https://github.com/nikmcfly/MiroFish-Offline" target="_blank" class="github-link">
          Github <span>↗</span>
        </a>
        <button @click="handleLogout" class="logout-btn">Sign Out</button>
      </div>
    </nav>

    <div class="home-inner">
    <div class="main-content">
      <!-- Hero -->
      <section class="hero-section">
        <div class="hero-left">
          <div class="tag-row">
            <span class="neon-tag">Decision Intelligence Platform</span>
            <span class="version-text">/ Mu Sigma Custom Build</span>
          </div>

          <h1 class="main-title">
            Upload Any Dataset<br>
            <span class="gradient-text">Simulate What Happens Next</span>
          </h1>

          <div class="hero-desc">
            <p>
              Forked from <span class="hl-brand">MiroFish</span> and customised for <span class="hl-neon">Mu Sigma's</span> Decision Science practice. Extract entity networks from any document, spawn an ecosystem of <span class="hl-neon">autonomous AI agents</span> — each with a distinct persona, memory, and behaviour model — and observe emergent social dynamics before your decisions reach production.
            </p>
            <p>
              Model policy impacts, forecast stakeholder reactions, and find <span class="hl-code">"local optima"</span> in complex organisational dynamics. Built for analysts who think in systems.
            </p>
            <p class="slogan-text">
              All compute runs on Mu Sigma infrastructure. Zero data leaves your environment<span class="blinking-cursor">_</span>
            </p>
          </div>

          <div class="decoration-square"></div>
        </div>

        <div class="hero-right">
          <canvas ref="simCanvas" class="sim-canvas"></canvas>
        </div>
      </section>

      <!-- Dashboard -->
      <section class="dashboard-section">
        <div class="left-panel">
          <div class="panel-header">
            <span class="status-dot">■</span> System Status
          </div>
          <h2 class="section-title">Ready</h2>
          <p class="section-desc">
            Local prediction engine on standby. Upload your data to initialise a simulation run.
          </p>

          <div class="metrics-row">
            <div class="metric-card">
              <div class="metric-value">Local</div>
              <div class="metric-label">Runs on your infra</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">Private</div>
              <div class="metric-label">Zero cloud dependency</div>
            </div>
          </div>

          <div class="steps-container">
            <div class="steps-header">
              <span class="diamond-icon">◇</span> Workflow Sequence
            </div>
            <div class="workflow-list">
              <div v-for="step in steps" :key="step.num" class="workflow-item">
                <span class="step-num">{{ step.num }}</span>
                <div class="step-info">
                  <div class="step-title">{{ step.title }}</div>
                  <div class="step-desc">{{ step.desc }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Upload Console -->
        <div class="right-panel">
          <div class="console-box">
            <div class="console-section">
              <div class="console-header">
                <span>01 / Reality Seeds</span>
                <span>Supported: PDF, MD, TXT, JSON</span>
              </div>
              <div
                class="upload-zone"
                @dragover.prevent="isDragOver = true"
                @dragleave.prevent="isDragOver = false"
                @drop.prevent="handleDrop"
                @click="triggerFileInput"
                :style="isDragOver ? 'border-color: var(--neon); background: var(--bg2)' : ''"
              >
                <input ref="fileInput" type="file" multiple accept=".pdf,.md,.txt,.json" @change="handleFileSelect" style="display:none" :disabled="loading" />
                <div v-if="files.length === 0" class="upload-placeholder">
                  <div class="upload-icon">↑</div>
                  <div class="upload-title">Drag & drop files here</div>
                  <div class="upload-hint">or click to browse</div>
                </div>
                <div v-else class="file-list">
                  <div v-for="(file, i) in files" :key="i" class="file-item">
                    <span>📄</span>
                    <span class="file-name">{{ file.name }}</span>
                    <button @click.stop="files.splice(i, 1)" class="remove-btn">×</button>
                  </div>
                </div>
              </div>
            </div>

            <div class="console-divider"><span>Parameters</span></div>

            <div class="console-section">
              <div class="console-header">
                <span>>_ 02 / Simulation Prompt</span>
              </div>
              <div class="input-wrapper">
                <textarea
                  v-model="simReq"
                  class="code-input"
                  placeholder="// Describe your simulation or prediction goal in natural language"
                  rows="6"
                  :disabled="loading"
                ></textarea>
                <div class="model-badge">Engine: Ollama + Neo4j (local)</div>
              </div>
            </div>

            <div class="console-section" style="padding-top:0">
              <button class="start-engine-btn" @click="startSim" :disabled="!canSubmit || loading">
                <span>{{ loading ? 'Initialising…' : 'Start Engine' }}</span>
                <span>→</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <HistoryDatabase />
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import HistoryDatabase from '../components/HistoryDatabase.vue'
import { setPendingUpload } from '../store/pendingUpload'
import { currentUser, clearAuth } from '../store/auth'
import { isDark, toggleTheme } from '../store/theme'
import { logout as apiLogout } from '../api/auth'

const router = useRouter()
const files = ref([])
const simReq = ref('')
const loading = ref(false)
const isDragOver = ref(false)
const fileInput = ref(null)
const starCanvas = ref(null)
const simCanvas = ref(null)

onMounted(() => {
  // --- Network simulation canvas ---
  const sim = simCanvas.value
  if (sim) {
    const sc = sim.getContext('2d')
    const rsim = () => { const r = sim.getBoundingClientRect(); sim.width = r.width || sim.offsetWidth; sim.height = r.height || sim.offsetHeight }
    rsim()
    window.addEventListener('resize', rsim)
    const nodes = Array.from({ length: 22 }, () => ({
      x: Math.random(), y: Math.random(),
      vx: (Math.random() - 0.5) * 0.0003, vy: (Math.random() - 0.5) * 0.0003,
      r: Math.random() * 3 + 2, phase: Math.random() * Math.PI * 2,
      spd: Math.random() * 0.015 + 0.008
    }))
    const parts = []
    const drawSim = () => {
      const W = sim.width, H = sim.height
      sc.clearRect(0, 0, W, H)
      nodes.forEach(n => {
        n.x += n.vx; n.y += n.vy; n.phase += n.spd
        if (n.x < 0.05 || n.x > 0.95) n.vx *= -1
        if (n.y < 0.05 || n.y > 0.95) n.vy *= -1
      })
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = (nodes[i].x - nodes[j].x) * W, dy = (nodes[i].y - nodes[j].y) * H
          const d = Math.sqrt(dx*dx + dy*dy)
          if (d < 140) {
            sc.beginPath(); sc.moveTo(nodes[i].x*W, nodes[i].y*H); sc.lineTo(nodes[j].x*W, nodes[j].y*H)
            sc.strokeStyle = `rgba(249,115,22,${(1-d/140)*0.22})`; sc.lineWidth = 1; sc.stroke()
            if (Math.random() < 0.0008) parts.push({ a:i, b:j, t:0, spd: Math.random()*0.004+0.002 })
          }
        }
      }
      for (let i = parts.length - 1; i >= 0; i--) {
        const p = parts[i]; p.t += p.spd
        if (p.t >= 1) { parts.splice(i,1); continue }
        const na = nodes[p.a], nb = nodes[p.b]
        sc.beginPath(); sc.arc((na.x+(nb.x-na.x)*p.t)*W, (na.y+(nb.y-na.y)*p.t)*H, 2, 0, Math.PI*2)
        sc.fillStyle = `rgba(249,115,22,${0.9-p.t*0.5})`; sc.fill()
      }
      nodes.forEach(n => {
        const pulse = 0.6 + 0.4 * Math.sin(n.phase)
        const g = sc.createRadialGradient(n.x*W, n.y*H, 0, n.x*W, n.y*H, n.r*4)
        g.addColorStop(0, `rgba(249,115,22,${0.85*pulse})`); g.addColorStop(1, 'rgba(249,115,22,0)')
        sc.beginPath(); sc.arc(n.x*W, n.y*H, n.r*4, 0, Math.PI*2); sc.fillStyle = g; sc.fill()
        sc.beginPath(); sc.arc(n.x*W, n.y*H, n.r, 0, Math.PI*2)
        sc.fillStyle = `rgba(255,200,100,${pulse})`; sc.fill()
      })

      // Center text
      const t = performance.now() / 1000
      const textPulse = 0.7 + 0.3 * Math.sin(t * 1.2)
      const cx = W / 2, cy = H / 2
      sc.save()
      sc.textAlign = 'center'
      sc.textBaseline = 'middle'
      // Glow
      sc.shadowColor = `rgba(255,255,255,${0.6 * textPulse})`
      sc.shadowBlur = 30
      sc.font = `900 ${Math.max(22, W * 0.095)}px "JetBrains Mono", monospace`
      sc.fillStyle = `rgba(255,255,255,${textPulse})`
      sc.fillText('MIROFISH', cx, cy - W * 0.032)
      sc.shadowBlur = 0
      sc.font = `500 ${Math.max(9, W * 0.032)}px "JetBrains Mono", monospace`
      sc.fillStyle = `rgba(255,255,255,${0.45 * textPulse})`
      sc.fillText('v26.06.04', cx, cy + W * 0.036)
      sc.font = `400 ${Math.max(8, W * 0.026)}px "Space Grotesk", sans-serif`
      sc.fillStyle = `rgba(255,255,255,${0.28 * textPulse})`
      sc.fillText('Customized for Mu Sigma Operations..', cx, cy + W * 0.088)
      sc.restore()

      requestAnimationFrame(drawSim)
    }
    drawSim()
  }

  // --- Star canvas ---
  const canvas = starCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  const stars = []
  const resize = () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight }
  resize()
  window.addEventListener('resize', resize)
  for (let s = 0; s < 180; s++) {
    stars.push({ x: Math.random(), y: Math.random(), r: Math.random() * 1.2 + 0.2, o: Math.random() * 0.5 + 0.1, d: Math.random() * 0.003 + 0.001 })
  }
  const draw = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    stars.forEach(s => {
      s.o += s.d; if (s.o > 0.6 || s.o < 0.1) s.d *= -1
      ctx.beginPath(); ctx.arc(s.x * canvas.width, s.y * canvas.height, s.r, 0, Math.PI * 2)
      ctx.fillStyle = `rgba(255,255,255,${s.o})`; ctx.fill()
    })
    requestAnimationFrame(draw)
  }
  draw()
})

const canSubmit = computed(() => simReq.value.trim() !== '' && files.value.length > 0)

const triggerFileInput = () => { if (!loading.value) fileInput.value?.click() }
const handleFileSelect = (e) => addFiles(Array.from(e.target.files))
const handleDrop = (e) => { isDragOver.value = false; addFiles(Array.from(e.dataTransfer.files)) }

const addFiles = (newFiles) => {
  const allowed = ['.pdf', '.md', '.txt', '.json']
  const valid = newFiles.filter(f => allowed.some(ext => f.name.toLowerCase().endsWith(ext)))
  files.value = [...files.value, ...valid]
}

const scrollToBottom = () => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })

const startSim = () => {
  if (!canSubmit.value || loading.value) return
  setPendingUpload(files.value, simReq.value)
  router.push({ name: 'Process', params: { projectId: 'new' } })
}

const handleLogout = async () => {
  try { await apiLogout() } catch (_) {}
  clearAuth()
  router.push({ name: 'Login' })
}

const steps = [
  { num: '01', title: 'Knowledge Graph', desc: 'Extract entity networks from your documents using Neo4j + GraphRAG' },
  { num: '02', title: 'Agent Configuration', desc: 'Generate AI personas from graph entities via local Ollama LLM' },
  { num: '03', title: 'Simulation', desc: 'Run multi-agent social dynamics locally with emergent behaviour tracking' },
  { num: '04', title: 'Analysis Report', desc: 'AI-generated strategic insights from simulation output' },
  { num: '05', title: 'Deep Interaction', desc: 'Interview any simulated agent to probe reasoning and perspectives' },
]
</script>
