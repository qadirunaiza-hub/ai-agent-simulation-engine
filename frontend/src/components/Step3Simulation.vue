<template>
  <div class="simulation-panel">
    <!-- Live Scrape Banner -->
    <ScrapeBanner />

    <!-- LLM Transparency Floating Popup -->
    <LlmPopup v-if="showLlmLog" :simulation-id="simulationId" @close="showLlmLog = false" />
    <!-- Top Control Bar -->
    <div class="control-bar">
      <div class="status-group">
        <!-- Twitter Platform Progress -->
        <div class="platform-status twitter" :class="{ active: runStatus.twitter_running, completed: runStatus.twitter_completed }">
          <div class="platform-header">
            <svg class="platform-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
            </svg>
            <span class="platform-name">Info Plaza</span>
            <span v-if="runStatus.twitter_completed" class="status-badge">
              <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </span>
          </div>
          <div class="platform-stats">
            <span class="stat">
              <span class="stat-label">ROUND</span>
              <span class="stat-value mono">{{ runStatus.twitter_current_round || 0 }}<span class="stat-total">/{{ runStatus.total_rounds || maxRounds || '-' }}</span></span>
            </span>
            <span class="stat">
              <span class="stat-label">Elapsed Time</span>
              <span class="stat-value mono">{{ twitterElapsedTime }}</span>
            </span>
            <span class="stat">
              <span class="stat-label">ACTS</span>
              <span class="stat-value mono">{{ runStatus.twitter_actions_count || 0 }}</span>
            </span>
          </div>
          <!-- Available Actions Tooltip -->
          <div class="actions-tooltip">
            <div class="tooltip-title">Available Actions</div>
            <div class="tooltip-actions">
              <span class="tooltip-action">POST</span>
              <span class="tooltip-action">LIKE</span>
              <span class="tooltip-action">REPOST</span>
              <span class="tooltip-action">QUOTE</span>
              <span class="tooltip-action">FOLLOW</span>
              <span class="tooltip-action">IDLE</span>
            </div>
          </div>
        </div>
        
        <!-- Reddit Platform Progress -->
        <div class="platform-status reddit" :class="{ active: runStatus.reddit_running, completed: runStatus.reddit_completed }">
          <div class="platform-header">
            <svg class="platform-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
            </svg>
            <span class="platform-name">Topic Community</span>
            <span v-if="runStatus.reddit_completed" class="status-badge">
              <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </span>
          </div>
          <div class="platform-stats">
            <span class="stat">
              <span class="stat-label">ROUND</span>
              <span class="stat-value mono">{{ runStatus.reddit_current_round || 0 }}<span class="stat-total">/{{ runStatus.total_rounds || maxRounds || '-' }}</span></span>
            </span>
            <span class="stat">
              <span class="stat-label">Elapsed Time</span>
              <span class="stat-value mono">{{ redditElapsedTime }}</span>
            </span>
            <span class="stat">
              <span class="stat-label">ACTS</span>
              <span class="stat-value mono">{{ runStatus.reddit_actions_count || 0 }}</span>
            </span>
          </div>
          <!-- Available Actions Tooltip -->
          <div class="actions-tooltip">
            <div class="tooltip-title">Available Actions</div>
            <div class="tooltip-actions">
              <span class="tooltip-action">POST</span>
              <span class="tooltip-action">COMMENT</span>
              <span class="tooltip-action">LIKE</span>
              <span class="tooltip-action">DISLIKE</span>
              <span class="tooltip-action">SEARCH</span>
              <span class="tooltip-action">TREND</span>
              <span class="tooltip-action">FOLLOW</span>
              <span class="tooltip-action">MUTE</span>
              <span class="tooltip-action">REFRESH</span>
              <span class="tooltip-action">IDLE</span>
            </div>
          </div>
        </div>
      </div>

      <div class="action-controls">
        <!-- Pause / Resume -->
        <button
          v-if="phase === 1"
          class="action-btn secondary"
          :disabled="isPausing"
          @click="handlePause"
        >{{ isPausing ? 'Pausing…' : 'Pause & Rearrange' }}</button>

        <button
          v-if="isPaused"
          class="action-btn secondary"
          @click="handleResume"
        >Resume</button>

        <!-- Sidebar toggles -->
        <button class="action-btn icon-btn" :class="{ active: showOntology }" @click="showOntology = !showOntology" title="Bag Ontology">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"></path></svg>
        </button>
        <button class="action-btn icon-btn" :class="{ active: showLlmLog }" @click="toggleLlmLog" title="LLM Transparency">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        </button>

        <button
          class="action-btn primary"
          :disabled="phase !== 2 || isGeneratingReport"
          @click="handleNextStep"
        >
          <span v-if="isGeneratingReport" class="loading-spinner-small"></span>
          {{ isGeneratingReport ? 'Starting...' : 'Start Generating Report' }}
          <span v-if="!isGeneratingReport" class="arrow-icon">→</span>
        </button>
      </div>
    </div>

    <!-- Main Content: Dual Timeline -->
    <div class="main-content-area" ref="scrollContainer">
      <!-- Timeline Header -->
      <div class="timeline-header" v-if="allActions.length > 0">
        <div class="timeline-stats">
          <span class="total-count">TOTAL EVENTS: <span class="mono">{{ allActions.length }}</span></span>
          <span class="platform-breakdown">
            <span class="breakdown-item twitter">
              <svg class="mini-icon" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
              <span class="mono">{{ twitterActionsCount }}</span>
            </span>
            <span class="breakdown-divider">/</span>
            <span class="breakdown-item reddit">
              <svg class="mini-icon" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
              <span class="mono">{{ redditActionsCount }}</span>
            </span>
          </span>
        </div>
      </div>
      
      <!-- Timeline Feed -->
      <div class="timeline-feed">
        <div class="timeline-axis"></div>
        
        <TransitionGroup name="timeline-item">
          <div 
            v-for="action in chronologicalActions" 
            :key="action._uniqueId || action.id || `${action.timestamp}-${action.agent_id}`" 
            class="timeline-item"
            :class="action.platform"
          >
            <div class="timeline-marker">
              <div class="marker-dot"></div>
            </div>
            
            <div class="timeline-card">
              <div class="card-header">
                <div class="agent-info">
                  <div class="avatar-placeholder">{{ (action.agent_name || 'A')[0] }}</div>
                  <span class="agent-name">{{ action.agent_name }}</span>
                </div>
                
                <div class="header-meta">
                  <div class="platform-indicator">
                    <svg v-if="action.platform === 'twitter'" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
                    <svg v-else viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
                  </div>
                  <div class="action-badge" :class="getActionTypeClass(action.action_type)">
                    {{ getActionTypeLabel(action.action_type) }}
                  </div>
                </div>
              </div>
              
              <div class="card-body">
                <!-- CREATE_POST: Post Publication -->
                <div v-if="action.action_type === 'CREATE_POST' && action.action_args?.content" class="content-text main-text">
                  {{ action.action_args.content }}
                </div>

                <!-- QUOTE_POST: Quote Post -->
                <template v-if="action.action_type === 'QUOTE_POST'">
                  <div v-if="action.action_args?.quote_content" class="content-text">
                    {{ action.action_args.quote_content }}
                  </div>
                  <div v-if="action.action_args?.original_content" class="quoted-block">
                    <div class="quote-header">
                      <svg class="icon-small" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
                      <span class="quote-label">@{{ action.action_args.original_author_name || 'User' }}</span>
                    </div>
                    <div class="quote-text">
                      {{ truncateContent(action.action_args.original_content, 150) }}
                    </div>
                  </div>
                </template>

                <!-- REPOST: Repost -->
                <template v-if="action.action_type === 'REPOST'">
                  <div class="repost-info">
                    <svg class="icon-small" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="17 1 21 5 17 9"></polyline><path d="M3 11V9a4 4 0 0 1 4-4h14"></path><polyline points="7 23 3 19 7 15"></polyline><path d="M21 13v2a4 4 0 0 1-4 4H3"></path></svg>
                    <span class="repost-label">Reposted from @{{ action.action_args?.original_author_name || 'User' }}</span>
                  </div>
                  <div v-if="action.action_args?.original_content" class="repost-content">
                    {{ truncateContent(action.action_args.original_content, 200) }}
                  </div>
                </template>

                <!-- LIKE_POST: Like Post -->
                <template v-if="action.action_type === 'LIKE_POST'">
                  <div class="like-info">
                    <svg class="icon-small filled" viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
                    <span class="like-label">Liked @{{ action.action_args?.post_author_name || 'User' }}'s post</span>
                  </div>
                  <div v-if="action.action_args?.post_content" class="liked-content">
                    "{{ truncateContent(action.action_args.post_content, 120) }}"
                  </div>
                </template>

                <!-- CREATE_COMMENT: Create Comment -->
                <template v-if="action.action_type === 'CREATE_COMMENT'">
                  <div v-if="action.action_args?.content" class="content-text">
                    {{ action.action_args.content }}
                  </div>
                  <div v-if="action.action_args?.post_id" class="comment-context">
                    <svg class="icon-small" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
                    <span>Reply to post #{{ action.action_args.post_id }}</span>
                  </div>
                </template>

                <!-- SEARCH_POSTS: Search Posts -->
                <template v-if="action.action_type === 'SEARCH_POSTS'">
                  <div class="search-info">
                    <svg class="icon-small" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    <span class="search-label">Search Query:</span>
                    <span class="search-query">"{{ action.action_args?.query || '' }}"</span>
                  </div>
                </template>

                <!-- FOLLOW: Follow User -->
                <template v-if="action.action_type === 'FOLLOW'">
                  <div class="follow-info">
                    <svg class="icon-small" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="20" y1="8" x2="20" y2="14"></line><line x1="23" y1="11" x2="17" y2="11"></line></svg>
                    <span class="follow-label">Followed @{{ action.action_args?.target_user || action.action_args?.user_id || 'User' }}</span>
                  </div>
                </template>

                <!-- UPVOTE / DOWNVOTE -->
                <template v-if="action.action_type === 'UPVOTE_POST' || action.action_type === 'DOWNVOTE_POST'">
                  <div class="vote-info">
                    <svg v-if="action.action_type === 'UPVOTE_POST'" class="icon-small" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="18 15 12 9 6 15"></polyline></svg>
                    <svg v-else class="icon-small" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
                    <span class="vote-label">{{ action.action_type === 'UPVOTE_POST' ? 'Upvoted' : 'Downvoted' }} Post</span>
                  </div>
                  <div v-if="action.action_args?.post_content" class="voted-content">
                    "{{ truncateContent(action.action_args.post_content, 120) }}"
                  </div>
                </template>

                <!-- DO_NOTHING: No Action (Idle) -->
                <template v-if="action.action_type === 'DO_NOTHING'">
                  <div class="idle-info">
                    <svg class="icon-small" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                    <span class="idle-label">Action Skipped</span>
                  </div>
                </template>

                <!-- Generic Fallback: Unknown types or content not handled above -->
                <div v-if="!['CREATE_POST', 'QUOTE_POST', 'REPOST', 'LIKE_POST', 'CREATE_COMMENT', 'SEARCH_POSTS', 'FOLLOW', 'UPVOTE_POST', 'DOWNVOTE_POST', 'DO_NOTHING'].includes(action.action_type) && action.action_args?.content" class="content-text">
                  {{ action.action_args.content }}
                </div>
              </div>

              <div class="card-footer">
                <span class="time-tag">R{{ action.round_num }} • {{ formatActionTime(action.timestamp) }}</span>
                <!-- Platform tag removed as it is in header now -->
              </div>
            </div>
          </div>
        </TransitionGroup>

        <div v-if="allActions.length === 0" class="waiting-state">
          <div class="pulse-ring"></div>
          <span>Waiting for agent actions...</span>
        </div>
      </div>
    </div>

    <!-- Pause / Rearrange Overlay -->
    <div v-if="isPaused" class="rearrange-overlay">
      <div class="rearrange-panel">
      <div class="rp-header">
        <span class="rp-title">PAUSED — Rearrange Agents</span>
        <button class="rp-close" @click="isPaused = false">×</button>
      </div>

      <!-- Inject Event -->
      <div class="rp-section">
        <div class="rp-section-title">Inject Event into Simulation</div>
        <div class="inject-row">
          <input v-model="injectContent" class="inject-input" placeholder="Type a breaking-news post or event…" />
          <button class="inject-btn" @click="doInjectEvent" :disabled="!injectContent.trim()">Inject</button>
        </div>
        <div v-if="injectMsg" class="inject-msg">{{ injectMsg }}</div>
      </div>

      <!-- Agent List -->
      <div class="rp-section">
        <div class="rp-section-title">Agent Activity & Stance</div>
        <div class="agent-list">
          <div v-for="(ag, idx) in editableAgents" :key="ag.agent_id" class="agent-row">
            <span class="ag-rank">{{ idx + 1 }}</span>
            <div class="ag-info">
              <span class="ag-name">{{ ag.entity_name || ag.name || 'Agent ' + ag.agent_id }}</span>
              <span class="ag-type">{{ ag.entity_type }}</span>
            </div>
            <div class="ag-controls">
              <label class="ag-label">Activity</label>
              <input type="range" min="0" max="1" step="0.05" v-model.number="ag.activity_level" class="ag-slider" />
              <span class="ag-val">{{ (ag.activity_level * 100).toFixed(0) }}%</span>
              <select v-model="ag.stance" class="ag-select">
                <option value="neutral">Neutral</option>
                <option value="supportive">Supportive</option>
                <option value="opposing">Opposing</option>
                <option value="observer">Observer</option>
              </select>
            </div>
            <div class="ag-order-btns">
              <button @click="moveAgent(idx, -1)" :disabled="idx === 0">↑</button>
              <button @click="moveAgent(idx, 1)" :disabled="idx === editableAgents.length - 1">↓</button>
            </div>
          </div>
        </div>
      </div>

      <div class="rp-footer">
        <button class="rp-save" @click="saveAndResume">Save & Resume</button>
        <button class="rp-cancel" @click="isPaused = false">Cancel</button>
      </div>
      </div>
    </div>

    <!-- Ontology Panel -->
    <div v-if="showOntology" class="side-panel ontology-panel">
      <div class="sp-header">
        <span>BAG ONTOLOGY</span>
        <button class="sp-close" @click="showOntology = false">×</button>
      </div>
      <div v-if="ontologyLoading" class="sp-loading">Loading…</div>
      <div v-else-if="ontology" class="sp-content">
        <div class="onto-section">
          <div class="onto-section-title">Entity Types ({{ ontology.entity_types?.length || 0 }})</div>
          <div v-for="et in ontology.entity_types" :key="et.name" class="onto-item">
            <span class="onto-name">{{ et.name }}</span>
            <span class="onto-desc">{{ et.description }}</span>
            <div v-if="et.examples?.length" class="onto-examples">eg: {{ et.examples.slice(0,2).join(', ') }}</div>
          </div>
        </div>
        <div class="onto-section">
          <div class="onto-section-title">Edge Types ({{ ontology.edge_types?.length || 0 }})</div>
          <div v-for="edge in ontology.edge_types" :key="edge.name" class="onto-item">
            <span class="onto-name edge">{{ edge.name }}</span>
            <span class="onto-desc">{{ edge.description }}</span>
          </div>
        </div>
      </div>
      <div v-else class="sp-empty">No ontology data available.</div>
    </div>

    <!-- LLM Transparency Panel -->
    <!-- LLM popup is now a floating draggable window (see <LlmPopup> at top) -->

    <!-- Bottom Info / Logs -->
    <div class="system-logs">
      <div class="log-header">
        <span class="log-title">SIMULATION MONITOR</span>
        <span class="log-id">{{ simulationId || 'NO_SIMULATION' }}</span>
      </div>
      <div class="log-content" ref="logContent">
        <div class="log-line" v-for="(log, idx) in systemLogs" :key="idx">
          <span class="log-time">{{ log.time }}</span>
          <span class="log-msg">{{ log.msg }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import LlmPopup from './LlmPopup.vue'
import ScrapeBanner from './ScrapeBanner.vue'
import {
  startSimulation,
  stopSimulation,
  getRunStatus,
  getRunStatusDetail
} from '../api/simulation'
import { generateReport } from '../api/report'
import {
  pauseSimulation,
  resumeSimulation,
  updateAgentConfigs,
  injectEvent,
  getSimulationOntology,
  getSimulationLlmCalls
} from '../api/settings'

const props = defineProps({
  simulationId: String,
  maxRounds: Number, // Max rounds passed from Step2
  minutesPerRound: {
    type: Number,
    default: 30 // Default: 30 minutes per round
  },
  projectData: Object,
  graphData: Object,
  systemLogs: Array
})

const emit = defineEmits(['go-back', 'next-step', 'add-log', 'update-status'])

const router = useRouter()

// State
const isGeneratingReport = ref(false)
const phase = ref(0) // 0: Not started, 1: Running, 2: Completed
const isStarting = ref(false)
const isStopping = ref(false)
const isPausing = ref(false)
const isPaused = ref(false)
const startError = ref(null)
const runStatus = ref({})
const allActions = ref([]) // All actions (incremental accumulation)
const actionIds = ref(new Set()) // Action IDs set for deduplication
const scrollContainer = ref(null)

// Ontology
const showOntology = ref(false)
const ontology = ref(null)
const ontologyLoading = ref(false)

// LLM Transparency
const showLlmLog = ref(false)
const llmCalls = ref([])
const expandedCall = ref(null)
let llmPollTimer = null

// Rearrange
const editableAgents = ref([])
const injectContent = ref('')
const injectMsg = ref('')

// Computed
// Display actions in chronological order (newest at the bottom)
const chronologicalActions = computed(() => {
  return allActions.value
})

// Count actions per platform
const twitterActionsCount = computed(() => {
  return allActions.value.filter(a => a.platform === 'twitter').length
})

const redditActionsCount = computed(() => {
  return allActions.value.filter(a => a.platform === 'reddit').length
})

// Format simulated elapsed time (calculated based on rounds and minutes per round)
const formatElapsedTime = (currentRound) => {
  if (!currentRound || currentRound <= 0) return '0h 0m'
  const totalMinutes = currentRound * props.minutesPerRound
  const hours = Math.floor(totalMinutes / 60)
  const minutes = totalMinutes % 60
  return `${hours}h ${minutes}m`
}

// Simulated elapsed time for Twitter platform
const twitterElapsedTime = computed(() => {
  return formatElapsedTime(runStatus.value.twitter_current_round || 0)
})

// Simulated elapsed time for Reddit platform
const redditElapsedTime = computed(() => {
  return formatElapsedTime(runStatus.value.reddit_current_round || 0)
})

// Methods
const addLog = (msg) => {
  emit('add-log', msg)
}

// Reset all states (for restarting simulation)
const resetAllState = () => {
  phase.value = 0
  runStatus.value = {}
  allActions.value = []
  actionIds.value = new Set()
  prevTwitterRound.value = 0
  prevRedditRound.value = 0
  startError.value = null
  isStarting.value = false
  isStopping.value = false
  stopPolling()  // Stop any existing polling
}

// Start simulation
const doStartSimulation = async () => {
  if (!props.simulationId) {
    addLog('Error: Missing simulationId')
    return
  }

  // Reset all states first to avoid impact from previous simulation
  resetAllState()

  isStarting.value = true
  startError.value = null
  addLog('Starting dual-platform parallel simulation...')
  emit('update-status', 'processing')

  try {
    const params = {
      simulation_id: props.simulationId,
      platform: 'parallel',
      force: true,  // Force restart
      enable_graph_memory_update: true  // Enable dynamic graph update
    }

    if (props.maxRounds) {
      params.max_rounds = props.maxRounds
      addLog(`Set max simulation rounds: ${props.maxRounds}`)
    }

    addLog('Dynamic graph update mode enabled')

    const res = await startSimulation(params)

    if (res.success && res.data) {
      if (res.data.force_restarted) {
        addLog('✓ Cleaned old simulation logs and restarted simulation')
      }
      addLog('✓ Simulation engine started successfully')
      addLog(`  ├─ PID: ${res.data.process_pid || '-'}`)

      phase.value = 1
      runStatus.value = res.data

      startStatusPolling()
      startDetailPolling()
    } else {
      startError.value = res.error || 'Start failed'
      addLog(`✗ Start failed: ${res.error || 'Unknown error'}`)
      emit('update-status', 'error')
    }
  } catch (err) {
    startError.value = err.message
    addLog(`✗ Start exception: ${err.message}`)
    emit('update-status', 'error')
  } finally {
    isStarting.value = false
  }
}

// Stop simulation
const handleStopSimulation = async () => {
  if (!props.simulationId) return

  isStopping.value = true
  addLog('Stopping simulation...')

  try {
    const res = await stopSimulation({ simulation_id: props.simulationId })

    if (res.success) {
      addLog('✓ Simulation stopped')
      phase.value = 2
      stopPolling()
      emit('update-status', 'completed')
    } else {
      addLog(`Stop failed: ${res.error || 'Unknown error'}`)
    }
  } catch (err) {
    addLog(`Stop exception: ${err.message}`)
  } finally {
    isStopping.value = false
  }
}

// Polling status
let statusTimer = null
let detailTimer = null

const startStatusPolling = () => {
  statusTimer = setInterval(fetchRunStatus, 2000)
}

const startDetailPolling = () => {
  detailTimer = setInterval(fetchRunStatusDetail, 3000)
}

const stopPolling = () => {
  if (statusTimer) {
    clearInterval(statusTimer)
    statusTimer = null
  }
  if (detailTimer) {
    clearInterval(detailTimer)
    detailTimer = null
  }
}

// Track previous rounds for each platform to detect changes and output logs
const prevTwitterRound = ref(0)
const prevRedditRound = ref(0)

const fetchRunStatus = async () => {
  if (!props.simulationId) return

  try {
    const res = await getRunStatus(props.simulationId)

    if (res.success && res.data) {
      const data = res.data

      runStatus.value = data

      // Detect round changes for each platform and output logs
      if (data.twitter_current_round > prevTwitterRound.value) {
        addLog(`[Info Plaza] R${data.twitter_current_round}/${data.total_rounds} | T:${data.twitter_simulated_hours || 0}h | A:${data.twitter_actions_count}`)
        prevTwitterRound.value = data.twitter_current_round
      }

      if (data.reddit_current_round > prevRedditRound.value) {
        addLog(`[Topic Community] R${data.reddit_current_round}/${data.total_rounds} | T:${data.reddit_simulated_hours || 0}h | A:${data.reddit_actions_count}`)
        prevRedditRound.value = data.reddit_current_round
      }

      // Check if simulation is complete (via runner_status or platform completion status)
      const isCompleted = data.runner_status === 'completed' || data.runner_status === 'stopped'

      // Additional check: if backend hasn't updated runner_status yet, but platforms have reported completion
      // Check via twitter_completed and reddit_completed status
      const platformsCompleted = checkPlatformsCompleted(data)

      if (isCompleted || platformsCompleted) {
        if (platformsCompleted && !isCompleted) {
          addLog('✓ Detected all platform simulations have ended')
        }
        addLog('✓ Simulation completed')
        phase.value = 2
        stopPolling()
        emit('update-status', 'completed')
      }
    }
  } catch (err) {
    console.warn('Failed to fetch run status:', err)
  }
}

// Check if all enabled platforms have completed
const checkPlatformsCompleted = (data) => {
  // If no platform data, return false
  if (!data) return false

  // Check completion status for each platform
  const twitterCompleted = data.twitter_completed === true
  const redditCompleted = data.reddit_completed === true

  // If at least one platform completed, check if all enabled platforms are complete
  // Determine if platform is enabled via actions_count (count > 0 or running was true)
  const twitterEnabled = (data.twitter_actions_count > 0) || data.twitter_running || twitterCompleted
  const redditEnabled = (data.reddit_actions_count > 0) || data.reddit_running || redditCompleted

  // If no platform is enabled, return false
  if (!twitterEnabled && !redditEnabled) return false

  // Check if all enabled platforms are complete
  if (twitterEnabled && !twitterCompleted) return false
  if (redditEnabled && !redditCompleted) return false

  return true
}

const fetchRunStatusDetail = async () => {
  if (!props.simulationId) return

  try {
    const res = await getRunStatusDetail(props.simulationId)

    if (res.success && res.data) {
      // Use all_actions to get complete action list
      const serverActions = res.data.all_actions || []

      // Incrementally add new actions (with deduplication)
      let newActionsAdded = 0
      serverActions.forEach(action => {
        // Generate unique ID
        const actionId = action.id || `${action.timestamp}-${action.platform}-${action.agent_id}-${action.action_type}`

        if (!actionIds.value.has(actionId)) {
          actionIds.value.add(actionId)
          allActions.value.push({
            ...action,
            _uniqueId: actionId
          })
          newActionsAdded++
        }
      })

      // Don't auto-scroll, let user freely view timeline
      // New actions will be appended at the bottom
    }
  } catch (err) {
    console.warn('Failed to fetch detailed status:', err)
  }
}

// Helpers
const getActionTypeLabel = (type) => {
  const labels = {
    'CREATE_POST': 'POST',
    'REPOST': 'REPOST',
    'LIKE_POST': 'LIKE',
    'CREATE_COMMENT': 'COMMENT',
    'LIKE_COMMENT': 'LIKE',
    'DO_NOTHING': 'IDLE',
    'FOLLOW': 'FOLLOW',
    'SEARCH_POSTS': 'SEARCH',
    'QUOTE_POST': 'QUOTE',
    'UPVOTE_POST': 'UPVOTE',
    'DOWNVOTE_POST': 'DOWNVOTE'
  }
  return labels[type] || type || 'UNKNOWN'
}

const getActionTypeClass = (type) => {
  const classes = {
    'CREATE_POST': 'badge-post',
    'REPOST': 'badge-action',
    'LIKE_POST': 'badge-action',
    'CREATE_COMMENT': 'badge-comment',
    'LIKE_COMMENT': 'badge-action',
    'QUOTE_POST': 'badge-post',
    'FOLLOW': 'badge-meta',
    'SEARCH_POSTS': 'badge-meta',
    'UPVOTE_POST': 'badge-action',
    'DOWNVOTE_POST': 'badge-action',
    'DO_NOTHING': 'badge-idle'
  }
  return classes[type] || 'badge-default'
}

const truncateContent = (content, maxLength = 100) => {
  if (!content) return ''
  if (content.length > maxLength) return content.substring(0, maxLength) + '...'
  return content
}

const formatActionTime = (timestamp) => {
  if (!timestamp) return ''
  try {
    return new Date(timestamp).toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })
  } catch {
    return ''
  }
}

const handleNextStep = async () => {
  if (!props.simulationId) {
    addLog('Error: Missing simulationId')
    return
  }

  if (isGeneratingReport.value) {
    addLog('Report generation request sent, please wait...')
    return
  }

  isGeneratingReport.value = true
  addLog('Starting report generation...')

  try {
    const res = await generateReport({
      simulation_id: props.simulationId,
      force_regenerate: true
    })

    if (res.success && res.data) {
      const reportId = res.data.report_id
      addLog(`✓ Report generation task started: ${reportId}`)

      // Navigate to report page
      router.push({ name: 'Report', params: { reportId } })
    } else {
      addLog(`✗ Failed to start report generation: ${res.error || 'Unknown error'}`)
      isGeneratingReport.value = false
    }
  } catch (err) {
    addLog(`✗ Report generation exception: ${err.message}`)
    isGeneratingReport.value = false
  }
}

// ===== Pause / Resume / Rearrange =====

const handlePause = async () => {
  if (!props.simulationId) return
  isPausing.value = true
  addLog('Pausing simulation…')
  try {
    await pauseSimulation(props.simulationId)
    stopPolling()
    phase.value = 0
    isPaused.value = true
    addLog('✓ Simulation paused. Rearrange agents and resume when ready.')
    emit('update-status', 'paused')
    // Load agents for rearranging
    await loadEditableAgents()
  } catch (e) {
    addLog('✗ Pause failed: ' + e.message)
  } finally {
    isPausing.value = false
  }
}

const loadEditableAgents = async () => {
  if (!props.simulationId) return
  try {
    const { getSimulationConfig } = await import('../api/simulation')
    const res = await getSimulationConfig(props.simulationId)
    if (res.success && res.data?.agent_configs) {
      editableAgents.value = res.data.agent_configs.map(a => ({ ...a }))
    }
  } catch (_) {}
}

const moveAgent = (idx, dir) => {
  const arr = editableAgents.value
  const target = idx + dir
  if (target < 0 || target >= arr.length) return
  const tmp = arr[idx]; arr[idx] = arr[target]; arr[target] = tmp
  editableAgents.value = [...arr]
}

const doInjectEvent = async () => {
  const content = injectContent.value.trim()
  if (!content || !props.simulationId) return
  try {
    await injectEvent(props.simulationId, content, 'User')
    injectMsg.value = '✓ Event injected — will appear in next run'
    injectContent.value = ''
    setTimeout(() => { injectMsg.value = '' }, 4000)
  } catch (e) {
    injectMsg.value = '✗ ' + e.message
  }
}

const saveAndResume = async () => {
  if (!props.simulationId) return
  try {
    // Save agent patches + order
    const order = editableAgents.value.map(a => a.agent_id)
    await updateAgentConfigs(props.simulationId, editableAgents.value, order)
    addLog('✓ Agent configs saved')
    isPaused.value = false
    await handleResume()
  } catch (e) {
    addLog('✗ Save failed: ' + e.message)
  }
}

const handleResume = async () => {
  if (!props.simulationId) return
  addLog('Resuming simulation…')
  try {
    const res = await resumeSimulation(props.simulationId, { platform: 'parallel' })
    if (res.success) {
      phase.value = 1
      isPaused.value = false
      runStatus.value = res.data
      startStatusPolling()
      startDetailPolling()
      addLog('✓ Simulation resumed')
      emit('update-status', 'processing')
    } else {
      addLog('✗ Resume failed: ' + (res.error || 'unknown'))
    }
  } catch (e) {
    addLog('✗ Resume error: ' + e.message)
  }
}

// ===== Ontology =====

const loadOntology = async () => {
  if (!props.simulationId || ontology.value) return
  ontologyLoading.value = true
  try {
    const res = await getSimulationOntology(props.simulationId)
    if (res.success) ontology.value = res.data?.ontology
  } catch (_) {}
  finally { ontologyLoading.value = false }
}

watch(showOntology, (v) => { if (v) loadOntology() })

// ===== LLM Transparency =====

const fetchLlmCalls = async () => {
  if (!props.simulationId || !showLlmLog.value) return
  try {
    const res = await getSimulationLlmCalls(props.simulationId, 60)
    if (res.success) llmCalls.value = res.data?.calls || []
  } catch (_) {}
}

const toggleLlmLog = () => {
  showLlmLog.value = !showLlmLog.value
  if (showLlmLog.value) {
    fetchLlmCalls()
    llmPollTimer = setInterval(fetchLlmCalls, 4000)
  } else {
    clearInterval(llmPollTimer); llmPollTimer = null
  }
}

const formatLlmTime = (ts) => {
  if (!ts) return ''
  try { return new Date(ts).toLocaleTimeString('en-US', { hour12: false }) } catch { return '' }
}

// Scroll log to bottom
const logContent = ref(null)
watch(() => props.systemLogs?.length, () => {
  nextTick(() => {
    if (logContent.value) {
      logContent.value.scrollTop = logContent.value.scrollHeight
    }
  })
})

onMounted(() => {
  addLog('Step3 Simulation initialization')
  if (props.simulationId) {
    doStartSimulation()
  }
})

onUnmounted(() => {
  stopPolling()
  if (llmPollTimer) clearInterval(llmPollTimer)
})
</script>

<style scoped>
.simulation-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--bg2);
  font-family: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  overflow: hidden;
}

/* --- Control Bar --- */
.control-bar {
  background: var(--bg2);
  padding: 12px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #EAEAEA;
  z-index: 10;
  height: 64px;
}

.status-group {
  display: flex;
  gap: 12px;
}

/* Platform Status Cards */
.platform-status {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 6px 12px;
  border-radius: 4px;
  background: var(--bg3);
  border: 1px solid #EAEAEA;
  opacity: 0.7;
  transition: all 0.3s;
  min-width: 140px;
  position: relative;
  cursor: pointer;
}

.platform-status.active {
  opacity: 1;
  border-color: var(--text);
  background: var(--bg2);
}

.platform-status.completed {
  opacity: 1;
  border-color: #1A936F;
  background: #F2FAF6;
}

/* Actions Tooltip */
.actions-tooltip {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-top: 8px;
  padding: 10px 14px;
  background: #000;
  color: #FFF;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s ease;
  z-index: 100;
  min-width: 180px;
  pointer-events: none;
}

.actions-tooltip::before {
  content: '';
  position: absolute;
  top: -6px;
  left: 50%;
  transform: translateX(-50%);
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-bottom: 6px solid #000;
}

.platform-status:hover .actions-tooltip {
  opacity: 1;
  visibility: visible;
}

.tooltip-title {
  font-size: 10px;
  font-weight: 600;
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 8px;
}

.tooltip-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tooltip-action {
  font-size: 10px;
  font-weight: 600;
  padding: 3px 8px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 2px;
  color: #FFF;
  letter-spacing: 0.03em;
}

.platform-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 2px;
}

.platform-name {
  font-size: 11px;
  font-weight: 700;
  color: var(--text);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.platform-status.twitter .platform-icon { color: var(--text); }
.platform-status.reddit .platform-icon { color: var(--text); }

.platform-stats {
  display: flex;
  gap: 10px;
}

.stat {
  display: flex;
  align-items: baseline;
  gap: 3px;
}

.stat-label {
  font-size: 8px;
  color: var(--text3);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 11px;
  font-weight: 600;
  color: var(--text);
}

.stat-total, .stat-unit {
  font-size: 9px;
  color: var(--text3);
  font-weight: 400;
}

.status-badge {
  margin-left: auto;
  color: #1A936F;
  display: flex;
  align-items: center;
}

/* Action Button */
.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  font-size: 13px;
  font-weight: 600;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.action-btn.primary {
  background: #000;
  color: #FFF;
}

.action-btn.primary:hover:not(:disabled) {
  background: #333;
}

.action-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* --- Main Content Area --- */
.main-content-area {
  flex: 1;
  overflow-y: auto;
  position: relative;
  background: var(--bg2);
}

/* Timeline Header */
.timeline-header {
  position: sticky;
  top: 0;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  padding: 12px 24px;
  border-bottom: 1px solid #EAEAEA;
  z-index: 5;
  display: flex;
  justify-content: center;
}

.timeline-stats {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 11px;
  color: var(--text2);
  background: #F5F5F5;
  padding: 4px 12px;
  border-radius: 20px;
}

.total-count {
  font-weight: 600;
  color: var(--text);
}

.platform-breakdown {
  display: flex;
  align-items: center;
  gap: 8px;
}

.breakdown-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.breakdown-divider { color: #DDD; }
.breakdown-item.twitter { color: var(--text); }
.breakdown-item.reddit { color: var(--text); }

/* --- Timeline Feed --- */
.timeline-feed {
  padding: 24px 0;
  position: relative;
  min-height: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.timeline-axis {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 1px;
  background: #EAEAEA; /* Cleaner line */
  transform: translateX(-50%);
}

.timeline-item {
  display: flex;
  justify-content: center;
  margin-bottom: 32px;
  position: relative;
  width: 100%;
}

.timeline-marker {
  position: absolute;
  left: 50%;
  top: 24px;
  width: 10px;
  height: 10px;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 50%;
  transform: translateX(-50%);
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
}

.marker-dot {
  width: 4px;
  height: 4px;
  background: #CCC;
  border-radius: 50%;
}

.timeline-item.twitter .marker-dot { background: #000; }
.timeline-item.reddit .marker-dot { background: #000; }
.timeline-item.twitter .timeline-marker { border-color: var(--text); }
.timeline-item.reddit .timeline-marker { border-color: var(--text); }

/* Card Layout */
.timeline-card {
  width: calc(100% - 48px);
  background: var(--bg2);
  border-radius: 2px;
  padding: 16px 20px;
  border: 1px solid #EAEAEA;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
  position: relative;
  transition: all 0.2s;
}

.timeline-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  border-color: #DDD;
}

/* Left side (Twitter) */
.timeline-item.twitter {
  justify-content: flex-start;
  padding-right: 50%;
}
.timeline-item.twitter .timeline-card {
  margin-left: auto;
  margin-right: 32px; /* Gap from axis */
}

/* Right side (Reddit) */
.timeline-item.reddit {
  justify-content: flex-end;
  padding-left: 50%;
}
.timeline-item.reddit .timeline-card {
  margin-right: auto;
  margin-left: 32px; /* Gap from axis */
}

/* Card Content Styles */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #F5F5F5;
}

.agent-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar-placeholder {
  width: 24px;
  height: 24px;
  background: #000;
  color: #FFF;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}

.agent-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
}

.header-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.platform-indicator {
  color: var(--text3);
  display: flex;
  align-items: center;
}

.action-badge {
  font-size: 9px;
  padding: 2px 6px;
  border-radius: 2px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px solid transparent;
}

/* Monochromatic Badges */
.badge-post { background: #F0F0F0; color: var(--text); border-color: #E0E0E0; }
.badge-comment { background: #F0F0F0; color: var(--text2); border-color: #E0E0E0; }
.badge-action { background: var(--bg2); color: var(--text2); border: 1px solid #E0E0E0; }
.badge-meta { background: var(--bg3); color: var(--text3); border: 1px dashed #DDD; }
.badge-idle { opacity: 0.5; }

.content-text {
  font-size: 13px;
  line-height: 1.6;
  color: var(--text);
  margin-bottom: 10px;
}

.content-text.main-text {
  font-size: 14px;
  color: var(--text);
}

/* Info Blocks (Quote, Repost, etc) */
.quoted-block, .repost-content {
  background: #F9F9F9;
  border: 1px solid var(--border);
  padding: 10px 12px;
  border-radius: 2px;
  margin-top: 8px;
  font-size: 12px;
  color: #555;
}

.quote-header, .repost-info, .like-info, .search-info, .follow-info, .vote-info, .idle-info, .comment-context {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
  font-size: 11px;
  color: var(--text2);
}

.icon-small {
  color: var(--text3);
}
.icon-small.filled {
  color: var(--text3); /* Keep icons neutral unless highlighted */
}

.search-query {
  font-family: 'JetBrains Mono', monospace;
  background: #F0F0F0;
  padding: 0 4px;
  border-radius: 2px;
}

.card-footer {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
  font-size: 10px;
  color: #BBB;
  font-family: 'JetBrains Mono', monospace;
}

/* Waiting State */
.waiting-state {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  color: #CCC;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.pulse-ring {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid #EAEAEA;
  animation: ripple 2s infinite;
}

@keyframes ripple {
  0% { transform: scale(0.8); opacity: 1; border-color: #CCC; }
  100% { transform: scale(2.5); opacity: 0; border-color: #EAEAEA; }
}

/* Animation */
.timeline-item-enter-active,
.timeline-item-leave-active {
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.timeline-item-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.timeline-item-leave-to {
  opacity: 0;
}

/* Logs */
.system-logs {
  background: #000;
  color: #DDD;
  padding: 16px;
  font-family: 'JetBrains Mono', monospace;
  border-top: 1px solid #222;
  flex-shrink: 0;
}

.log-header {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #333;
  padding-bottom: 8px;
  margin-bottom: 8px;
  font-size: 10px;
  color: var(--text2);
}

.log-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  height: 100px;
  overflow-y: auto;
  padding-right: 4px;
}

.log-content::-webkit-scrollbar { width: 4px; }
.log-content::-webkit-scrollbar-thumb { background: #333; border-radius: 2px; }

.log-line {
  font-size: 11px;
  display: flex;
  gap: 12px;
  line-height: 1.5;
}

.log-time { color: #555; min-width: 75px; }
.log-msg { color: #BBB; word-break: break-all; }
.mono { font-family: 'JetBrains Mono', monospace; }

/* Loading spinner for button */
.loading-spinner-small {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #FFF;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 6px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Secondary action button */
.action-btn.secondary {
  background: var(--bg2);
  color: var(--text);
  border: 1px solid var(--border);
}
.action-btn.secondary:hover:not(:disabled) { background: #F5F5F5; }
.action-btn.icon-btn {
  padding: 8px 10px;
  background: var(--bg3);
  color: #555;
  border: 1px solid #E0E0E0;
}
.action-btn.icon-btn.active { background: #000; color: #FFF; border-color: var(--text); }

/* ======== Side Panels (ontology + llm log) ======== */
.side-panel {
  position: fixed;
  top: 0; right: 0; bottom: 0;
  width: 380px;
  background: var(--bg2);
  border-left: 1px solid #E0E0E0;
  box-shadow: -4px 0 20px rgba(0,0,0,0.08);
  z-index: 500;
  display: flex;
  flex-direction: column;
  font-family: 'JetBrains Mono', monospace;
}

.sp-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #E0E0E0;
  font-size: 11px; font-weight: 700; color: var(--text);
  text-transform: uppercase; letter-spacing: 0.08em;
  background: var(--bg3);
}

.sp-close {
  background: none; border: none; cursor: pointer;
  font-size: 18px; color: var(--text3); line-height: 1;
}

.sp-loading, .sp-empty {
  padding: 24px 16px; font-size: 12px; color: var(--text3); text-align: center;
}

.sp-content { flex: 1; overflow-y: auto; padding: 12px 16px; }

/* Ontology */
.onto-section { margin-bottom: 20px; }
.onto-section-title {
  font-size: 10px; font-weight: 700; color: #888;
  text-transform: uppercase; letter-spacing: 0.08em;
  margin-bottom: 8px; padding-bottom: 4px;
  border-bottom: 1px solid #F0F0F0;
}
.onto-item { margin-bottom: 10px; }
.onto-name {
  display: inline-block; font-size: 12px; font-weight: 600; color: var(--text);
  background: #F0F0F0; padding: 2px 6px; border-radius: 3px;
  margin-bottom: 3px;
}
.onto-name.edge { background: #E8F0FE; color: #1A56DB; }
.onto-desc { display: block; font-size: 11px; color: var(--text2); line-height: 1.4; }
.onto-examples { font-size: 10px; color: var(--text3); margin-top: 2px; }

/* LLM calls */
.llm-content { padding: 8px; }
.llm-call-card {
  border: 1px solid #EAEAEA; border-radius: 4px; margin-bottom: 8px;
  cursor: pointer; transition: border-color 0.15s;
  overflow: hidden;
}
.llm-call-card:hover { border-color: #CCC; }
.llm-call-card.expanded { border-color: var(--text); }

.llm-call-header {
  display: flex; align-items: center; gap: 8px; padding: 8px 10px;
  background: var(--bg3);
}
.llm-tag {
  font-size: 9px; font-weight: 700; padding: 2px 6px;
  background: #000; color: #FFF; border-radius: 2px;
  text-transform: uppercase; letter-spacing: 0.05em;
}
.llm-model-tag { font-size: 10px; color: #555; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.llm-time-tag { font-size: 10px; color: #888; }
.llm-ts { font-size: 10px; color: #BBB; }

.llm-call-body { padding: 10px; border-top: 1px solid #EAEAEA; }
.llm-msg { margin-bottom: 8px; }
.llm-role {
  display: inline-block; font-size: 9px; font-weight: 700; padding: 1px 5px;
  border-radius: 2px; margin-bottom: 4px; text-transform: uppercase;
  background: #E8F0FE; color: #1A56DB;
}
.llm-msg.system .llm-role { background: #F0F0F0; color: #555; }
.llm-msg.user .llm-role { background: #FFF3E0; color: #E65100; }
.response-role { background: #E8F5E9; color: #1B5E20; }
.llm-response-block { margin-top: 6px; }
.llm-text {
  font-size: 11px; line-height: 1.5; color: var(--text);
  white-space: pre-wrap; word-break: break-word;
  background: var(--bg3); border: 1px solid #F0F0F0;
  padding: 6px 8px; border-radius: 3px; margin: 0;
  max-height: 200px; overflow-y: auto;
}

/* ======== Rearrange / Pause Panel ======== */
.rearrange-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5); z-index: 800;
  display: flex; align-items: center; justify-content: center;
}
.rearrange-panel {
  display: flex; flex-direction: column;
  width: 100%; max-width: 720px; max-height: 90vh; overflow: hidden;
  border-radius: 6px; box-shadow: 0 16px 48px rgba(0,0,0,0.3);
}

.rp-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px 20px;
  background: #000; color: #FFF;
  font-size: 12px; font-weight: 700; letter-spacing: 0.08em;
  text-transform: uppercase;
  width: 100%; max-width: 720px; border-radius: 6px 6px 0 0;
}
.rp-close { background: none; border: none; color: #FFF; font-size: 20px; cursor: pointer; }

.rp-section {
  background: var(--bg2); width: 100%; padding: 16px 20px; overflow-y: auto;
}
.rp-section-title {
  font-size: 10px; font-weight: 700; color: #888; text-transform: uppercase;
  letter-spacing: 0.08em; margin-bottom: 10px;
}

.inject-row { display: flex; gap: 8px; }
.inject-input {
  flex: 1; padding: 8px 10px; border: 1px solid var(--border); border-radius: 4px;
  font-size: 13px; outline: none;
}
.inject-input:focus { border-color: var(--text); }
.inject-btn {
  padding: 8px 16px; background: #333; color: #FFF; border: none;
  border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer;
}
.inject-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.inject-msg { margin-top: 6px; font-size: 11px; color: #1A936F; }

.agent-list { max-height: 260px; overflow-y: auto; }
.agent-row {
  display: flex; align-items: center; gap: 12px;
  padding: 8px 0; border-bottom: 1px solid #F5F5F5;
  font-family: 'Space Grotesk', system-ui, sans-serif;
}
.ag-rank { font-size: 11px; color: #BBB; min-width: 20px; text-align: right; }
.ag-info { flex: 1; min-width: 0; }
.ag-name { font-size: 13px; font-weight: 600; color: var(--text); display: block; }
.ag-type { font-size: 10px; color: #888; }
.ag-controls { display: flex; align-items: center; gap: 8px; }
.ag-label { font-size: 10px; color: var(--text3); white-space: nowrap; }
.ag-slider { width: 80px; }
.ag-val { font-size: 11px; color: #555; min-width: 30px; font-family: 'JetBrains Mono', monospace; }
.ag-select {
  padding: 3px 6px; border: 1px solid var(--border); border-radius: 3px;
  font-size: 11px; color: var(--text); background: var(--bg2);
}
.ag-order-btns { display: flex; flex-direction: column; gap: 2px; }
.ag-order-btns button {
  padding: 2px 6px; border: 1px solid #E0E0E0; border-radius: 2px;
  background: var(--bg3); font-size: 11px; cursor: pointer; color: #555;
}
.ag-order-btns button:disabled { opacity: 0.3; cursor: not-allowed; }

.rp-footer {
  display: flex; justify-content: flex-end; gap: 10px; padding: 14px 20px;
  background: var(--bg3); border-top: 1px solid #E0E0E0;
  width: 100%;
}
.rp-save {
  padding: 9px 20px; background: #000; color: #FFF; border: none;
  border-radius: 4px; font-size: 13px; font-weight: 600; cursor: pointer;
}
.rp-cancel {
  padding: 9px 20px; background: var(--bg2); color: var(--text); border: 1px solid var(--border);
  border-radius: 4px; font-size: 13px; font-weight: 600; cursor: pointer;
}
</style>