import { ref, computed } from 'vue'

const _theme = ref(localStorage.getItem('mirofish_theme') || 'dark')

export const theme = _theme
export const isDark = computed(() => _theme.value === 'dark')

export function toggleTheme() {
  _theme.value = _theme.value === 'dark' ? 'light' : 'dark'
  localStorage.setItem('mirofish_theme', _theme.value)
  document.documentElement.setAttribute('data-theme', _theme.value)
}

export function initTheme() {
  const t = localStorage.getItem('mirofish_theme') || 'dark'
  _theme.value = t
  document.documentElement.setAttribute('data-theme', t)
}
