import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import SplashView from '../views/SplashView.vue'
import LoginView from '../views/LoginView.vue'
import Process from '../views/MainView.vue'
import SimulationView from '../views/SimulationView.vue'
import SimulationRunView from '../views/SimulationRunView.vue'
import ReportView from '../views/ReportView.vue'
import InteractionView from '../views/InteractionView.vue'
import { isLoggedIn, loadFromStorage } from '../store/auth'

const PUBLIC_ROUTES = ['Login', 'Splash']

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/splash',
    name: 'Splash',
    component: SplashView
  },
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/process/:projectId',
    name: 'Process',
    component: Process,
    props: true
  },
  {
    path: '/simulation/:simulationId',
    name: 'Simulation',
    component: SimulationView,
    props: true
  },
  {
    path: '/simulation/:simulationId/start',
    name: 'SimulationRun',
    component: SimulationRunView,
    props: true
  },
  {
    path: '/report/:reportId',
    name: 'Report',
    component: ReportView,
    props: true
  },
  {
    path: '/interaction/:reportId',
    name: 'Interaction',
    component: InteractionView,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory('/mirofish'),
  routes
})

router.beforeEach((to, from) => {
  loadFromStorage()

  // Public routes pass through
  if (PUBLIC_ROUTES.includes(to.name)) return

  // Require auth for all other routes
  if (!isLoggedIn.value) {
    return { name: 'Login' }
  }

  // Show splash once per session (only for authenticated users heading to Home)
  if (to.name === 'Home' && !sessionStorage.getItem('mirofish_splash_seen')) {
    sessionStorage.setItem('mirofish_splash_seen', '1')
    return { name: 'Splash' }
  }
})

export default router
