<template>
  <teleport to="body">
    <div
      class="llm-popup"
      :style="{ left: pos.x + 'px', top: pos.y + 'px', width: minimized ? 'auto' : '520px' }"
      ref="popupEl"
    >
      <!-- Drag handle / header -->
      <div class="llm-popup-header" @mousedown="startDrag">
        <div class="llm-popup-title">
          <span class="llm-dot" :class="{ pulsing: live }"></span>
          AGENTIC CONVERSATION LOG
          <span class="llm-count">{{ calls.length }}</span>
        </div>
        <div class="llm-popup-actions">
          <button class="llm-hdr-btn" @click.stop="minimized = !minimized" :title="minimized ? 'Expand' : 'Minimise'">
            {{ minimized ? '▲' : '▼' }}
          </button>
          <button class="llm-hdr-btn close" @click.stop="$emit('close')" title="Close">×</button>
        </div>
      </div>

      <!-- Body -->
      <div v-if="!minimized" class="llm-popup-body">
        <div v-if="calls.length === 0" class="llm-empty">
          No LLM calls yet — start a simulation to see live conversation…
        </div>
        <div v-else ref="scrollEl" class="llm-scroll">
          <div
            v-for="(call, i) in calls"
            :key="i"
            class="llm-card"
            :class="{ expanded: expanded === i }"
            @click="expanded = expanded === i ? null : i"
          >
            <div class="llm-card-hdr">
              <span class="tag-pill" :style="tagColor(call.tag)">{{ call.tag }}</span>
              <span class="model-pill">{{ shortModel(call.model) }}</span>
              <span class="elapsed-pill">{{ call.elapsed_ms }}ms</span>
              <span
                class="relevance-pill"
                :style="relevanceColor(call.relevance_score)"
                :title="'Relevance: ' + call.relevance_score + '/100' + (call.relevance_flags?.length ? ' — ' + call.relevance_flags.join(', ') : '')"
              >R{{ call.relevance_score ?? '?' }}</span>
              <span class="ts-pill">{{ fmtTime(call.timestamp) }}</span>
              <span class="chevron">{{ expanded === i ? '▲' : '▼' }}</span>
            </div>
            <!-- Preview line -->
            <div v-if="expanded !== i" class="llm-preview">
              {{ preview(call) }}
            </div>
            <!-- Expanded full conversation -->
            <div v-if="expanded === i" class="llm-convo">
              <div
                v-for="(msg, mi) in call.messages"
                :key="mi"
                class="llm-msg"
                :class="'role-' + msg.role"
              >
                <span class="role-label">{{ msg.role }}</span>
                <pre class="msg-text">{{ msg.content }}</pre>
              </div>
              <div class="llm-msg role-assistant">
                <span class="role-label">assistant</span>
                <pre class="msg-text response">{{ call.response }}</pre>
              </div>
            </div>
          </div>
        </div>
        <div class="llm-footer">
          <span>Polling every 2s</span>
          <button class="clear-btn" @click="calls = []">Clear</button>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { getGlobalLlmCalls } from '../api/settings'

const props = defineProps({
  simulationId: String
})
defineEmits(['close'])

const pos = ref({ x: window.innerWidth - 540, y: 60 })
const minimized = ref(false)
const expanded = ref(null)
const calls = ref([])
const live = ref(false)
const scrollEl = ref(null)
const popupEl = ref(null)

let pollTimer = null
let dragging = false
let dragStart = { mx: 0, my: 0, px: 0, py: 0 }

const tagColors = {
  ontology: ['#E3F2FD', '#0D47A1'],
  simulation: ['#F3E5F5', '#6A1B9A'],
  report: ['#E8F5E9', '#1B5E20'],
  general: ['#FFF3E0', '#E65100'],
}
const tagColor = (tag) => {
  const [bg, fg] = tagColors[tag] || ['#F5F5F5', '#333']
  return { background: bg, color: fg }
}
const shortModel = (m = '') => m.length > 22 ? m.slice(0, 20) + '…' : m
const fmtTime = (ts) => {
  try { return new Date(ts).toLocaleTimeString() } catch { return '' }
}
const preview = (call) => {
  const last = call.messages?.[call.messages.length - 1]
  return (last?.content || '').slice(0, 120).replace(/\n/g, ' ')
}

const relevanceColor = (score) => {
  if (score == null) return { background: '#EEE', color: '#999' }
  if (score >= 75) return { background: '#E8F5E9', color: '#1B5E20' }
  if (score >= 45) return { background: '#FFF8E1', color: '#F57F17' }
  return { background: '#FFEBEE', color: '#B71C1C' }
}

const poll = async () => {
  try {
    const res = await getGlobalLlmCalls(100)
    const newCalls = res.data?.calls || []
    if (newCalls.length !== calls.value.length) {
      live.value = true
      calls.value = newCalls
      setTimeout(() => { live.value = false }, 1200)
      await nextTick()
      if (scrollEl.value) scrollEl.value.scrollTop = scrollEl.value.scrollHeight
    }
  } catch (_) {}
}

onMounted(() => {
  poll()
  pollTimer = setInterval(poll, 2000)
})
onUnmounted(() => clearInterval(pollTimer))

// Drag logic
const startDrag = (e) => {
  if (e.target.tagName === 'BUTTON') return
  dragging = true
  dragStart = { mx: e.clientX, my: e.clientY, px: pos.value.x, py: pos.value.y }
  window.addEventListener('mousemove', onDrag)
  window.addEventListener('mouseup', stopDrag)
}
const onDrag = (e) => {
  if (!dragging) return
  pos.value = {
    x: Math.max(0, Math.min(window.innerWidth - 520, dragStart.px + e.clientX - dragStart.mx)),
    y: Math.max(0, Math.min(window.innerHeight - 80, dragStart.py + e.clientY - dragStart.my)),
  }
}
const stopDrag = () => {
  dragging = false
  window.removeEventListener('mousemove', onDrag)
  window.removeEventListener('mouseup', stopDrag)
}
</script>

<script>
// Helper exposed to template — imported separately from settings.js
</script>

<style scoped>
.llm-popup {
  position: fixed;
  z-index: 9000;
  border-radius: 8px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.25);
  border: 1px solid #222;
  overflow: hidden;
  font-family: 'JetBrains Mono', monospace;
  user-select: none;
  min-width: 240px;
}

.llm-popup-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 9px 14px;
  background: #111;
  cursor: grab;
}
.llm-popup-header:active { cursor: grabbing; }

.llm-popup-title {
  display: flex; align-items: center; gap: 8px;
  font-size: 10px; font-weight: 700; color: #EEE;
  letter-spacing: 0.08em; text-transform: uppercase;
}

.llm-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: #555; flex-shrink: 0; transition: background 0.3s;
}
.llm-dot.pulsing { background: #4CAF50; animation: llm-pulse 0.6s ease; }
@keyframes llm-pulse { 0%,100% { opacity:1 } 50% { opacity:0.3 } }

.llm-count {
  background: #333; color: #AAA; font-size: 9px;
  padding: 1px 5px; border-radius: 10px;
}

.llm-popup-actions { display: flex; gap: 4px; }
.llm-hdr-btn {
  background: none; border: 1px solid #444; color: #AAA;
  border-radius: 3px; font-size: 12px; padding: 1px 6px;
  cursor: pointer; line-height: 1.4;
}
.llm-hdr-btn:hover { background: #333; color: #FFF; }
.llm-hdr-btn.close { border-color: #922; color: #F88; }
.llm-hdr-btn.close:hover { background: #922; color: #FFF; }

.llm-popup-body {
  background: #FAFAFA;
  display: flex; flex-direction: column;
  max-height: 480px;
}

.llm-empty {
  padding: 28px 16px; text-align: center;
  font-size: 11px; color: #999;
}

.llm-scroll {
  flex: 1; overflow-y: auto; padding: 8px;
  display: flex; flex-direction: column; gap: 6px;
}

.llm-card {
  border: 1px solid #E0E0E0; border-radius: 5px;
  background: #FFF; cursor: pointer; overflow: hidden;
  transition: border-color 0.15s;
}
.llm-card:hover { border-color: #AAA; }
.llm-card.expanded { border-color: #333; }

.llm-card-hdr {
  display: flex; align-items: center; gap: 6px;
  padding: 6px 10px; background: #F7F7F7;
  flex-wrap: wrap;
}

.tag-pill {
  font-size: 8px; font-weight: 700; padding: 2px 6px;
  border-radius: 3px; text-transform: uppercase; letter-spacing: 0.05em;
}
.model-pill { font-size: 9px; color: #555; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.elapsed-pill { font-size: 9px; color: #888; white-space: nowrap; }
.relevance-pill {
  font-size: 8px; font-weight: 700; padding: 2px 5px;
  border-radius: 3px; white-space: nowrap; cursor: help;
}
.ts-pill { font-size: 9px; color: #BBB; white-space: nowrap; }
.chevron { font-size: 8px; color: #CCC; margin-left: auto; }

.llm-preview {
  padding: 4px 10px 6px;
  font-size: 10px; color: #666; white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis;
}

.llm-convo { padding: 8px; display: flex; flex-direction: column; gap: 6px; }

.llm-msg { display: flex; flex-direction: column; gap: 3px; }
.role-label {
  font-size: 8px; font-weight: 700; text-transform: uppercase;
  padding: 1px 5px; border-radius: 2px; align-self: flex-start;
  background: #E8F0FE; color: #1A56DB;
}
.role-system .role-label { background: #F0F0F0; color: #555; }
.role-user .role-label { background: #FFF3E0; color: #E65100; }
.role-assistant .role-label { background: #E8F5E9; color: #1B5E20; }

.msg-text {
  font-size: 10px; line-height: 1.5; color: #333;
  white-space: pre-wrap; word-break: break-word;
  background: #F8F8F8; border: 1px solid #EEE;
  padding: 6px 8px; border-radius: 3px; margin: 0;
  max-height: 180px; overflow-y: auto;
}
.msg-text.response { background: #F0FFF4; border-color: #C8E6C9; }

.llm-footer {
  display: flex; justify-content: space-between; align-items: center;
  padding: 5px 10px; background: #F0F0F0;
  border-top: 1px solid #E0E0E0;
  font-size: 9px; color: #AAA;
}
.clear-btn {
  background: none; border: 1px solid #CCC; color: #888;
  font-size: 9px; padding: 1px 7px; border-radius: 3px; cursor: pointer;
}
.clear-btn:hover { background: #E0E0E0; }
</style>
