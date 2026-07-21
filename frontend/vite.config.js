import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  base: '/mirofish',
  plugins: [vue()],
  server: {
    port: 3000,
    open: false,
    allowedHosts: ['ird.mu-sigma.com', 'qa.ird.mu-sigma.com', '.ird.mu-sigma.com'],
    proxy: {
      '/mirofish/api': {
        target: 'http://localhost:5010',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/mirofish/, '')
      },
      '/api': {
        target: 'http://localhost:5010',
        changeOrigin: true,
        secure: false
      }
    }
  },
  preview: {
    port: 3000,
    host: true,
    allowedHosts: ['ird.mu-sigma.com', 'qa.ird.mu-sigma.com', '.ird.mu-sigma.com'],
    proxy: {
      '/mirofish/api': {
        target: 'http://localhost:5010',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/mirofish/, '')
      },
      '/api': {
        target: 'http://localhost:5010',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
