<template>
  <div v-if="question" class="question-banner" :class="{ expanded: isExpanded }">
    <div class="qb-left" @click="isExpanded = !isExpanded">
      <span class="qb-label">OBJECTIVE</span>
      <svg class="qb-quote" viewBox="0 0 24 24" width="12" height="12" fill="currentColor">
        <path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"/>
        <path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"/>
      </svg>
      <span class="qb-text" :title="question">{{ question }}</span>
      <svg class="qb-chevron" :class="{ open: isExpanded }" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </div>
    <div class="qb-right" v-if="docNames.length">
      <span v-for="(name, i) in docNames" :key="i" class="qb-doc-chip" :title="name">
        <svg viewBox="0 0 24 24" width="9" height="9" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
        </svg>
        {{ truncateDoc(name) }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  projectData: Object
})

const isExpanded = ref(false)

const question = computed(() => props.projectData?.simulation_requirement || '')

const docNames = computed(() => {
  return (props.projectData?.files || []).map(f => f.original_filename || f.filename).filter(Boolean)
})

const truncateDoc = (name) => name.length > 28 ? name.slice(0, 26) + '…' : name
</script>

<style scoped>
.question-banner {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 7px 18px;
  background: #080F1E;
  border-bottom: 1px solid #1A2A48;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  min-height: 32px;
  transition: min-height 0.25s ease;
  overflow: hidden;
}

.qb-left {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  flex: 1;
  min-width: 0;
  cursor: pointer;
  padding-top: 1px;
}

.qb-label {
  font-size: 8px;
  font-weight: 700;
  color: #4A9EFF;
  letter-spacing: 0.12em;
  white-space: nowrap;
  flex-shrink: 0;
  margin-top: 1px;
}

.qb-quote {
  color: #2A4A80;
  flex-shrink: 0;
  margin-top: 1px;
}

.qb-text {
  color: #C8D8F0;
  line-height: 1.5;
  flex: 1;
  min-width: 0;
}

/* Collapsed: one line, truncated */
.question-banner:not(.expanded) .qb-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Expanded: full text, wrap */
.question-banner.expanded {
  align-items: flex-start;
}
.question-banner.expanded .qb-text {
  white-space: pre-wrap;
  word-break: break-word;
}

.qb-chevron {
  flex-shrink: 0;
  color: #3A5A8A;
  margin-top: 2px;
  transition: transform 0.2s ease;
}
.qb-chevron.open {
  transform: rotate(180deg);
}

.qb-right {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
  flex-wrap: wrap;
  padding-top: 1px;
}

.qb-doc-chip {
  display: flex;
  align-items: center;
  gap: 4px;
  background: #111C30;
  border: 1px solid #1E3050;
  border-radius: 3px;
  padding: 2px 7px;
  font-size: 9px;
  color: #6A9AC0;
  white-space: nowrap;
  cursor: default;
}
</style>
