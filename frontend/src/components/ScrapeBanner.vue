<template>
  <div class="scrape-banner-wrapper">
    <div class="scrape-banner" :class="freshnessClass">
      <div class="scrape-left">
        <span class="scrape-icon">🌐</span>
        <div class="scrape-meta">
          <span class="scrape-label">INFORMATION BASIS</span>
          <span class="scrape-ts" v-if="scrapeData">
            <span class="basis-tag">Latest available reliable information</span>
            · Snapshot: <b>{{ formattedTime }}</b>
            · <b>{{ scrapeData.count }}</b> articles
            · <span class="source-list">{{ sourceList }}</span>
          </span>
          <span class="scrape-ts" v-else>Sourcing latest available reliable information…</span>
        </div>
      </div>

      <div class="scrape-headlines" v-if="scrapeData && headlines.length">
        <span
          v-for="(h, i) in headlines"
          :key="i"
          class="headline-chip"
          :title="h"
        >{{ h }}</span>
      </div>

      <div class="scrape-right">
        <span class="freshness-badge" :class="freshnessClass">{{ freshnessLabel }}</span>
        <button class="refresh-btn" @click="doRefresh" :disabled="refreshing">
          <span v-if="refreshing" class="spin">⟳</span>
          <span v-else>⟳ Refresh</span>
        </button>
      </div>
    </div>

    <!-- Fading activity log strip -->
    <transition-group name="scrape-log" tag="div" class="scrape-log-feed">
      <div v-for="log in logFeed" :key="log.id" class="scrape-log-item" :class="log.type">
        <span class="log-dot"></span>
        <span class="log-text">{{ log.text }}</span>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getScrapeStatus, refreshScrape } from '../api/settings'

const scrapeData = ref(null)
const refreshing = ref(false)
let pollTimer = null

// Fading log feed
const logFeed = ref([])
let logIdCounter = 0

const pushLog = (text, type = 'info', duration = 5000) => {
  const id = ++logIdCounter
  logFeed.value.push({ id, text, type })
  setTimeout(() => {
    logFeed.value = logFeed.value.filter(l => l.id !== id)
  }, duration)
}

const formattedTime = computed(() => {
  if (!scrapeData.value?.scraped_at) return ''
  const d = new Date(scrapeData.value.scraped_at)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) +
         ' · ' + d.toLocaleDateString([], { month: 'short', day: 'numeric' })
})

const sourceList = computed(() => {
  return (scrapeData.value?.sources || []).slice(0, 4).join(' · ')
})

const headlines = computed(() => {
  return (scrapeData.value?.articles || []).slice(0, 4).map(a => a.title.slice(0, 55))
})

const ageMinutes = computed(() => {
  if (!scrapeData.value?.scraped_at) return 999
  return (Date.now() - new Date(scrapeData.value.scraped_at)) / 60000
})

const freshnessClass = computed(() => {
  const m = ageMinutes.value
  if (m < 15) return 'fresh'
  if (m < 60) return 'recent'
  return 'stale'
})

const freshnessLabel = computed(() => {
  const m = Math.round(ageMinutes.value)
  if (m < 2) return 'JUST NOW'
  if (m < 60) return `${m}m ago`
  return `${Math.round(m / 60)}h ago`
})

const load = async () => {
  try {
    const res = await getScrapeStatus()
    if (res.data) scrapeData.value = res.data
  } catch (_) {}
}

const doRefresh = async () => {
  refreshing.value = true
  pushLog('Sourcing latest available reliable information...', 'active')
  try {
    const res = await refreshScrape()
    if (res.data) {
      scrapeData.value = res.data
      const sources = (res.data.sources || []).slice(0, 4).join(' · ')
      const count = res.data.count || 0
      pushLog(`✓ Sourced ${count} articles from latest available reliable information — ${sources}`, 'success', 6000)
    }
  } catch (_) {
    pushLog('Could not reach external sources — using cached data', 'warn', 5000)
  } finally {
    refreshing.value = false
  }
}

onMounted(async () => {
  pushLog('Sourcing latest available reliable information...', 'active')
  await load()
  if (scrapeData.value) {
    const sources = (scrapeData.value.sources || []).slice(0, 4).join(' · ')
    const count = scrapeData.value.count || 0
    pushLog(`✓ Information basis ready — ${count} articles from ${sources}`, 'success', 6000)
  }
  pollTimer = setInterval(load, 30000)
})
onUnmounted(() => clearInterval(pollTimer))
</script>

<style scoped>
.scrape-banner-wrapper {
  font-family: 'JetBrains Mono', monospace;
  background: #0A1628;
  position: relative;
}

.scrape-banner {
  display: flex; align-items: center; gap: 12px;
  padding: 7px 16px;
  border-bottom: 2px solid #1A3A5C;
  font-size: 10px; color: #AAA;
  flex-wrap: nowrap; overflow: hidden;
}
.scrape-banner.fresh { border-bottom-color: #1A936F; }
.scrape-banner.recent { border-bottom-color: #F59E0B; }
.scrape-banner.stale { border-bottom-color: #EF4444; }

.scrape-left { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.scrape-icon { font-size: 14px; }
.scrape-meta { display: flex; flex-direction: column; gap: 1px; }
.scrape-label {
  font-size: 8px; font-weight: 700; color: #4A9EFF;
  letter-spacing: 0.1em;
}
.scrape-ts { font-size: 9px; color: #88A; white-space: nowrap; }
.basis-tag { color: #5BCFA0; font-weight: 600; }
.source-list { color: #5A8; }

.scrape-headlines {
  display: flex; gap: 6px; flex: 1; overflow: hidden;
  align-items: center;
}
.headline-chip {
  background: #1A2540; color: #8AADCC;
  border: 1px solid #2A3F60; border-radius: 3px;
  padding: 2px 7px; font-size: 9px; white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis; max-width: 200px;
  cursor: default;
}

.scrape-right { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }

.freshness-badge {
  font-size: 8px; font-weight: 700; padding: 2px 6px;
  border-radius: 3px; text-transform: uppercase; letter-spacing: 0.05em;
  background: #1A2A1A; color: #4CAF50;
}
.freshness-badge.recent { background: #2A2010; color: #F59E0B; }
.freshness-badge.stale { background: #2A1010; color: #EF4444; }

.refresh-btn {
  background: #1A3A5C; border: 1px solid #2A5A8C; color: #4A9EFF;
  border-radius: 3px; font-size: 9px; font-weight: 600;
  padding: 3px 9px; cursor: pointer; font-family: inherit;
}
.refresh-btn:hover:not(:disabled) { background: #2A4A6C; }
.refresh-btn:disabled { opacity: 0.4; cursor: not-allowed; }

.spin { display: inline-block; animation: rotate 1s linear infinite; }
@keyframes rotate { from { transform: rotate(0deg) } to { transform: rotate(360deg) } }

/* Fading log feed */
.scrape-log-feed {
  display: flex;
  flex-direction: column;
  gap: 0;
  overflow: hidden;
}

.scrape-log-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 3px 16px;
  font-size: 9px;
  letter-spacing: 0.04em;
  border-bottom: 1px solid rgba(74, 158, 255, 0.08);
}

.scrape-log-item.active { color: #6ABFFF; }
.scrape-log-item.success { color: #5BCFA0; }
.scrape-log-item.warn { color: #F59E0B; }
.scrape-log-item.info { color: #8899AA; }

.log-dot {
  width: 5px; height: 5px;
  border-radius: 50%;
  flex-shrink: 0;
  background: currentColor;
  animation: pulse-dot 1.2s ease-in-out infinite;
}
.scrape-log-item.success .log-dot,
.scrape-log-item.warn .log-dot { animation: none; }

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

/* Vue TransitionGroup */
.scrape-log-enter-active {
  transition: opacity 0.4s ease, max-height 0.3s ease;
  max-height: 30px;
}
.scrape-log-leave-active {
  transition: opacity 1.2s ease, max-height 0.4s ease 0.8s;
  max-height: 30px;
}
.scrape-log-enter-from { opacity: 0; max-height: 0; }
.scrape-log-leave-to { opacity: 0; max-height: 0; }
</style>
