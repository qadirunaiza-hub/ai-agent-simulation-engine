<template>
  <div class="model-chooser">
    <!-- Trigger button -->
    <button class="model-btn" @click="toggle" :title="currentBase + ' / ' + currentModel">
      <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="2" y="3" width="20" height="14" rx="2"></rect>
        <line x1="8" y1="21" x2="16" y2="21"></line>
        <line x1="12" y1="17" x2="12" y2="21"></line>
      </svg>
      <span class="model-name">{{ shortModel }}</span>
      <span class="server-dot" :class="{ live: serverLive, dead: !serverLive && serverChecked }" />
      <svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </button>

    <!-- User (non-admin) panel — read-only + request button -->
    <div v-if="open && !isAdmin" class="model-dropdown">
      <div class="dropdown-header">
        <span>Active Model</span>
        <button class="close-btn" @click="open = false">×</button>
      </div>
      <div class="server-row">
        <div class="server-label">CURRENT MODEL</div>
        <div style="font-size:13px;padding:4px 0;font-family:'JetBrains Mono',monospace;color:#333">{{ currentModel }}</div>
        <div style="font-size:11px;color:#999;margin-top:6px">Model changes require admin approval.</div>
      </div>
      <div class="custom-model-row">
        <input v-model="requestedModel" class="custom-input" placeholder="Request a different model…" @keyup.enter="sendModelRequest" />
        <button class="apply-btn" @click="sendModelRequest" :disabled="!requestedModel.trim() || requestSending">
          {{ requestSending ? '…' : 'Request' }}
        </button>
      </div>
      <div v-if="requestMsg" class="dropdown-error" :style="{ color: requestMsg.startsWith('✓') ? '#1A936F' : '#c00' }">{{ requestMsg }}</div>
    </div>

    <!-- Admin dropdown (full control) -->
    <div v-if="open && isAdmin" class="model-dropdown">
      <div class="dropdown-header">
        <span>LLM Server &amp; Model</span>
        <button class="close-btn" @click="open = false">×</button>
      </div>

      <!-- Server URL row -->
      <div class="server-row">
        <label class="server-label">OLLAMA SERVER</label>
        <div class="server-input-wrap">
          <input
            v-model="serverInput"
            class="server-input"
            placeholder="http://172.25.1.70:11434"
            @keyup.enter="applyServer"
          />
          <button class="server-btn" @click="applyServer" :disabled="!serverInput.trim() || serverSaving">
            {{ serverSaving ? '…' : 'Connect' }}
          </button>
        </div>
        <div class="server-status" :class="{ live: serverLive, dead: !serverLive && serverChecked }">
          {{ serverStatusText }}
        </div>
      </div>

      <!-- Model list -->
      <div v-if="loadingModels" class="dropdown-loading">Loading models from server…</div>

      <div v-else-if="models.length > 0" class="model-list">
        <div class="model-list-header">{{ models.length }} models on {{ shortBase }}</div>
        <div class="qwen-rec">
          Recommended: <strong>qwen2.5:32b</strong> — best balance of speed &amp; quality for MiroFish simulations.
        </div>
        <button
          v-for="m in models"
          :key="m"
          class="model-option"
          :class="{ selected: m === currentModel, recommended: m.startsWith('qwen') }"
          @click="selectModel(m)"
        >
          <span class="model-label">{{ m }}</span>
          <span v-if="m.startsWith('qwen')" class="rec-badge">★ REC</span>
          <svg v-if="m === currentModel" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </button>
      </div>

      <div v-else-if="serverChecked" class="no-models">
        No models found — check server URL or run <code>ollama list</code>
      </div>

      <!-- Custom model input -->
      <div class="custom-model-row">
        <input
          v-model="customModel"
          class="custom-input"
          placeholder="or type a model name…"
          @keyup.enter="selectCustom"
        />
        <button class="apply-btn" @click="selectCustom" :disabled="!customModel.trim()">Use</button>
      </div>

      <div v-if="errorMsg" class="dropdown-error">{{ errorMsg }}</div>
    </div><!-- end admin dropdown -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getSettings, listModels, setModel, setServer } from '../api/settings'
import { submitModelRequest } from '../api/auth'
import { isAdmin } from '../store/auth'

const open = ref(false)
const loadingModels = ref(false)
const serverSaving = ref(false)
const models = ref([])
const currentModel = ref('…')
const currentBase = ref('')
const serverInput = ref('')
const customModel = ref('')
const errorMsg = ref('')
const serverLive = ref(false)
const serverChecked = ref(false)
const requestedModel = ref('')
const requestSending = ref(false)
const requestMsg = ref('')

const shortModel = computed(() => {
  const m = currentModel.value
  return m.length > 20 ? m.slice(0, 18) + '…' : m
})

const shortBase = computed(() => {
  try { return new URL(currentBase.value).host } catch { return currentBase.value }
})

const serverStatusText = computed(() => {
  if (!serverChecked.value) return ''
  return serverLive.value
    ? `✓ ${models.value.length} models available`
    : '✗ Server unreachable'
})

const loadSettings = async () => {
  try {
    const r = await getSettings()
    currentModel.value = r.data?.model || '?'
    currentBase.value = r.data?.base_url || ''
    serverInput.value = (r.data?.base_url || '').replace('/v1', '')
  } catch (_) {}
}

const loadModels = async (url) => {
  loadingModels.value = true
  serverChecked.value = false
  errorMsg.value = ''
  try {
    const r = await listModels(url || undefined)
    models.value = r.data?.models || []
    serverLive.value = r.data?.live ?? models.value.length > 0
    serverChecked.value = true
  } catch (e) {
    serverLive.value = false
    serverChecked.value = true
    errorMsg.value = 'Could not reach server: ' + e.message
  } finally {
    loadingModels.value = false
  }
}

const applyServer = async () => {
  const url = serverInput.value.trim()
  if (!url) return
  serverSaving.value = true
  errorMsg.value = ''
  try {
    const r = await setServer(url)
    if (r.success) {
      currentBase.value = r.data.base_url
      models.value = r.data.models || []
      serverLive.value = r.data.live ?? models.value.length > 0
      serverChecked.value = true
    }
  } catch (e) {
    errorMsg.value = 'Failed to connect: ' + e.message
    serverLive.value = false
    serverChecked.value = true
  } finally {
    serverSaving.value = false
  }
}

const selectModel = async (model) => {
  try {
    await setModel(model)
    currentModel.value = model
    open.value = false
  } catch (e) {
    errorMsg.value = 'Failed: ' + e.message
  }
}

const selectCustom = () => {
  const m = customModel.value.trim()
  if (m) { selectModel(m); customModel.value = '' }
}

const toggle = async () => {
  open.value = !open.value
  if (open.value) {
    await loadSettings()
    if (models.value.length === 0) await loadModels()
  }
}

const sendModelRequest = async () => {
  const m = requestedModel.value.trim()
  if (!m) return
  requestSending.value = true
  requestMsg.value = ''
  try {
    await submitModelRequest(m)
    requestMsg.value = '✓ Request submitted — admin will review'
    requestedModel.value = ''
  } catch (e) {
    requestMsg.value = 'Failed: ' + e.message
  } finally {
    requestSending.value = false
  }
}

const handleOutside = (e) => {
  if (!e.target.closest('.model-chooser')) open.value = false
}

onMounted(async () => {
  document.addEventListener('click', handleOutside)
  await loadSettings()
})

onUnmounted(() => document.removeEventListener('click', handleOutside))
</script>

<style scoped>
.model-chooser { position: relative; display: inline-flex; }

.model-btn {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 5px 10px; border-radius: 4px; border: 1px solid #DEDEDE;
  background: #FAFAFA; font-size: 11px; font-weight: 600; color: #333;
  cursor: pointer; font-family: 'JetBrains Mono', monospace;
  transition: all 0.15s;
}
.model-btn:hover { background: #F0F0F0; border-color: #BBB; }
.model-name { max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.server-dot {
  width: 7px; height: 7px; border-radius: 50%; background: #CCC; flex-shrink: 0;
}
.server-dot.live { background: #1A936F; }
.server-dot.dead { background: #E53E3E; }

/* Dropdown */
.model-dropdown {
  position: absolute; top: calc(100% + 6px); right: 0; width: 340px;
  background: #FFF; border: 1px solid #E0E0E0; border-radius: 6px;
  box-shadow: 0 8px 28px rgba(0,0,0,0.13); z-index: 1000; overflow: hidden;
}

.dropdown-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 14px; border-bottom: 1px solid #F0F0F0;
  font-size: 11px; font-weight: 700; color: #555;
  text-transform: uppercase; letter-spacing: 0.06em; background: #FAFAFA;
}
.close-btn { background: none; border: none; cursor: pointer; font-size: 18px; color: #999; }

/* Server row */
.server-row { padding: 10px 14px; border-bottom: 1px solid #F0F0F0; }
.server-label {
  display: block; font-size: 9px; font-weight: 700; color: #999;
  text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;
}
.server-input-wrap { display: flex; gap: 6px; }
.server-input {
  flex: 1; padding: 6px 8px; border: 1px solid #E0E0E0; border-radius: 3px;
  font-size: 11px; font-family: 'JetBrains Mono', monospace; outline: none; color: #333;
}
.server-input:focus { border-color: #666; }
.server-btn {
  padding: 6px 12px; background: #000; color: #FFF; border: none;
  border-radius: 3px; font-size: 11px; font-weight: 600; cursor: pointer; white-space: nowrap;
}
.server-btn:disabled { opacity: 0.35; cursor: not-allowed; }
.server-status {
  margin-top: 5px; font-size: 10px; color: #999; font-family: 'JetBrains Mono', monospace;
}
.server-status.live { color: #1A936F; }
.server-status.dead { color: #E53E3E; }

/* Model list */
.dropdown-loading, .no-models {
  padding: 14px; text-align: center; font-size: 12px; color: #999;
}

.model-list-header {
  padding: 6px 14px 4px;
  font-size: 9px; font-weight: 700; color: #BBB;
  text-transform: uppercase; letter-spacing: 0.08em;
}

.model-list { max-height: 280px; overflow-y: auto; padding: 4px 0; }

.model-option {
  width: 100%; display: flex; justify-content: space-between; align-items: center;
  padding: 7px 14px; background: none; border: none; cursor: pointer;
  font-size: 12px; color: #333; text-align: left; transition: background 0.1s;
  font-family: 'JetBrains Mono', monospace;
}
.model-option:hover { background: #F5F5F5; }
.model-option.selected { background: #F0F7FF; color: #0055CC; font-weight: 600; }
.model-option.recommended { border-left: 2px solid #FF6D00; }

.rec-badge {
  font-size: 8px; font-weight: 800; color: #FF6D00;
  background: #FFF3E0; padding: 1px 4px; border-radius: 2px;
  margin-right: 4px; white-space: nowrap;
}

.qwen-rec {
  padding: 6px 14px; font-size: 10px; color: #555;
  background: #FFFDE7; border-bottom: 1px solid #FFF9C4;
  line-height: 1.4;
}

/* Custom model */
.custom-model-row {
  display: flex; gap: 8px; padding: 10px 12px;
  border-top: 1px solid #F0F0F0;
}
.custom-input {
  flex: 1; padding: 6px 8px; border: 1px solid #E0E0E0; border-radius: 3px;
  font-size: 11px; font-family: 'JetBrains Mono', monospace; outline: none;
}
.custom-input:focus { border-color: #999; }
.apply-btn {
  padding: 6px 12px; background: #333; color: #FFF; border: none;
  border-radius: 3px; font-size: 11px; font-weight: 600; cursor: pointer;
}
.apply-btn:disabled { opacity: 0.3; cursor: not-allowed; }

.dropdown-error {
  padding: 8px 14px; font-size: 11px; color: #c00; border-top: 1px solid #F0F0F0;
}
</style>
