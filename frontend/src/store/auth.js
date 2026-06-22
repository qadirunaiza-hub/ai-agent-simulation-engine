import { ref, computed } from 'vue'

const _user = ref(null)

export const currentUser = _user
export const isLoggedIn = computed(() => !!_user.value)
export const isAdmin = computed(() => _user.value?.role === 'admin')

export function loadFromStorage() {
  const token = localStorage.getItem('mirofish_token')
  const raw = localStorage.getItem('mirofish_user')
  if (token && raw) {
    try { _user.value = JSON.parse(raw) } catch { clearAuth() }
  }
}

export function setAuth(token, user) {
  localStorage.setItem('mirofish_token', token)
  localStorage.setItem('mirofish_user', JSON.stringify(user))
  _user.value = user
}

export function clearAuth() {
  localStorage.removeItem('mirofish_token')
  localStorage.removeItem('mirofish_user')
  _user.value = null
}
