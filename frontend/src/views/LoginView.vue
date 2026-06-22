<template>
  <div class="login-page" :data-theme="theme">
    <!-- Theme toggle -->
    <button class="page-theme-btn" @click="toggleTheme" :title="isDark ? 'Light mode' : 'Dark mode'">
      {{ isDark ? '☀' : '🌙' }}
    </button>

    <div class="login-card">
      <!-- Fish logo -->
      <div class="fish-header">
        <svg class="mini-fish" viewBox="0 0 180 100" xmlns="http://www.w3.org/2000/svg" fill="none">
          <defs>
            <filter id="lg"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
          </defs>
          <g filter="url(#lg)">
            <path d="M 38 50 L 8 28 L 8 72 Z" stroke="currentColor" stroke-width="2" fill="none"/>
            <ellipse cx="90" cy="50" rx="58" ry="30" stroke="currentColor" stroke-width="2.2" fill="none"/>
            <path d="M 80 22 Q 93 4 108 22" stroke="currentColor" stroke-width="1.8" fill="none"/>
            <path d="M 118 62 Q 108 78 96 72" stroke="currentColor" stroke-width="1.5" fill="none" opacity="0.8"/>
            <path d="M 120 80 Q 132 94 145 80" stroke="currentColor" stroke-width="1.5" fill="none" opacity="0.7"/>
            <path d="M 130 25 Q 127 50 130 75" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
            <path d="M 120 22 Q 118 50 120 78" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
            <path d="M 140 32 Q 143 50 140 68" stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.5"/>
            <circle cx="155" cy="43" r="7" stroke="currentColor" stroke-width="1.8" fill="none"/>
            <circle cx="157" cy="41" r="3.5" fill="currentColor"/>
            <circle cx="158.5" cy="39.5" r="1.5" fill="#070B14" opacity="0.8"/>
            <path d="M 165 52 Q 169 56 165 60" stroke="currentColor" stroke-width="1.5" fill="none"/>
          </g>
        </svg>
        <div class="brand-block">
          <div class="brand-name">MIROFISH</div>
          <div class="brand-sub">× MU SIGMA</div>
        </div>
      </div>

      <div class="brand-tagline">Decision Intelligence Simulation Platform</div>

      <!-- Tabs -->
      <div class="tabs">
        <button class="tab" :class="{ active: mode === 'login' }" @click="mode = 'login'; error = ''">Sign In</button>
        <button class="tab" :class="{ active: mode === 'register' }" @click="mode = 'register'; error = ''">Register</button>
      </div>

      <!-- Sign In -->
      <form v-if="mode === 'login'" @submit.prevent="handleLogin" class="form">
        <div class="field">
          <label class="label">Username</label>
          <input v-model="form.username" type="text" class="input" placeholder="Enter username" autocomplete="username" required />
        </div>
        <div class="field">
          <label class="label">Password</label>
          <div class="pw-wrap">
            <input v-model="form.password" :type="showPw ? 'text' : 'password'" class="input pw-input" placeholder="Enter password" autocomplete="current-password" required />
            <button type="button" class="eye-btn" @click="showPw = !showPw" tabindex="-1">
              <svg v-if="!showPw" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              <svg v-else viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
            </button>
          </div>
        </div>
        <div v-if="error" class="error-msg">{{ error }}</div>
        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Signing in…' : 'Sign In →' }}
        </button>
      </form>

      <!-- Register -->
      <form v-else @submit.prevent="handleRegister" class="form">
        <div class="field">
          <label class="label">Username</label>
          <input v-model="form.username" type="text" class="input" placeholder="Choose a username (min 3 chars)" autocomplete="username" required />
        </div>
        <div class="field">
          <label class="label">Email <span class="opt">(optional)</span></label>
          <input v-model="form.email" type="email" class="input" placeholder="your@musigma.com" autocomplete="email" />
        </div>
        <div class="field">
          <label class="label">Password</label>
          <div class="pw-wrap">
            <input v-model="form.password" :type="showPw ? 'text' : 'password'" class="input pw-input" placeholder="Min 6 characters" autocomplete="new-password" required />
            <button type="button" class="eye-btn" @click="showPw = !showPw" tabindex="-1">
              <svg v-if="!showPw" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              <svg v-else viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
            </button>
          </div>
        </div>
        <div v-if="error" class="error-msg">{{ error }}</div>
        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Creating account…' : 'Create Account →' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login as apiLogin, register as apiRegister } from '../api/auth'
import { setAuth } from '../store/auth'
import { theme, isDark, toggleTheme } from '../store/theme'

const router = useRouter()
const mode = ref('login')
const loading = ref(false)
const error = ref('')
const showPw = ref(false)
const form = ref({ username: '', password: '', email: '' })

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  try {
    const res = await apiLogin({ username: form.value.username, password: form.value.password })
    setAuth(res.data.token, res.data.user)
    router.push({ name: 'Home' })
  } catch (e) {
    error.value = e.serverMessage || e.response?.data?.error || e.message || 'Login failed'
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  error.value = ''
  loading.value = true
  try {
    const res = await apiRegister({ username: form.value.username, password: form.value.password, email: form.value.email })
    setAuth(res.data.token, res.data.user)
    router.push({ name: 'Home' })
  } catch (e) {
    error.value = e.serverMessage || e.response?.data?.error || e.message || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'JetBrains Mono', monospace;
  padding: 24px;
  position: relative;
  /* Grid background */
  background-image:
    linear-gradient(rgba(0,255,200,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,255,200,0.04) 1px, transparent 1px);
  background-size: 40px 40px;
  transition: background 0.3s;
}

.page-theme-btn {
  position: fixed;
  top: 20px;
  right: 20px;
  background: var(--bg2);
  border: 1px solid var(--border2);
  color: var(--text);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: all 0.2s;
}
.page-theme-btn:hover { border-color: var(--neon); box-shadow: var(--neon-glow); }

.login-card {
  width: 420px;
  max-width: 100%;
  background: var(--bg2);
  border: 1px solid var(--border);
  padding: 40px 36px;
  box-shadow: 0 0 40px rgba(0,255,200,0.06), 0 0 80px rgba(0,0,0,0.4);
  transition: background 0.3s, border-color 0.3s;
}

/* Fish header */
.fish-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 6px;
}

.mini-fish {
  width: 88px;
  height: 48px;
  color: var(--neon);
  filter: drop-shadow(0 0 5px var(--neon)) drop-shadow(0 0 12px var(--neon-dim));
  animation: fishFloat 3s ease-in-out infinite;
}

@keyframes fishFloat {
  0%,100% { transform: translateY(0); }
  50%      { transform: translateY(-5px); }
}

.brand-block { line-height: 1.2; }
.brand-name {
  font-size: 1.2rem;
  font-weight: 800;
  letter-spacing: 2px;
  color: var(--text);
}
.brand-sub {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: var(--neon);
  text-shadow: var(--neon-glow);
}

.brand-tagline {
  font-size: 0.65rem;
  color: var(--text3);
  letter-spacing: 0.8px;
  margin-bottom: 28px;
  text-transform: uppercase;
}

/* Tabs */
.tabs {
  display: flex;
  border-bottom: 1px solid var(--border);
  margin-bottom: 26px;
}
.tab {
  flex: 1;
  padding: 9px;
  background: none;
  border: none;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text3);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: all 0.15s;
  letter-spacing: 0.5px;
}
.tab.active {
  color: var(--neon);
  border-bottom-color: var(--neon);
  text-shadow: 0 0 8px var(--neon);
}

/* Form */
.form { display: flex; flex-direction: column; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.label { font-size: 0.68rem; font-weight: 700; color: var(--text2); text-transform: uppercase; letter-spacing: 0.5px; }
.opt { font-weight: 400; text-transform: none; color: var(--text3); }

.input {
  padding: 10px 12px;
  border: 1px solid var(--border);
  background: var(--bg3);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.88rem;
  color: var(--text);
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.input:focus {
  border-color: var(--neon);
  box-shadow: 0 0 0 2px rgba(0,255,200,0.12);
  background: var(--bg2);
}
.input::placeholder { color: var(--text3); }

.pw-wrap { position: relative; display: flex; align-items: center; }
.pw-input { flex: 1; padding-right: 40px !important; }
.eye-btn {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text3);
  display: flex;
  align-items: center;
  padding: 0;
  transition: color 0.15s;
}
.eye-btn:hover { color: var(--neon); }

.error-msg {
  font-size: 0.78rem;
  color: #f87171;
  background: rgba(248,113,113,0.08);
  border: 1px solid rgba(248,113,113,0.25);
  padding: 8px 12px;
}

.submit-btn {
  width: 100%;
  padding: 13px;
  background: var(--btn-primary);
  color: var(--btn-text);
  border: 1px solid var(--neon);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.88rem;
  font-weight: 700;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.18s;
  margin-top: 4px;
  box-shadow: var(--neon-glow);
}
.submit-btn:hover:not(:disabled) { filter: brightness(1.15); transform: translateY(-1px); }
.submit-btn:disabled { opacity: 0.45; cursor: not-allowed; box-shadow: none; transform: none; }
</style>
