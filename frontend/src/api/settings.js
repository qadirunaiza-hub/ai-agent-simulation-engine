import service from './index'

export const getSettings = () => service.get('api/settings')
export const listModels = (url) => service.get('api/settings/models', url ? { params: { url } } : {})
export const setModel = (model) => service.post('api/settings/model', { model })
export const resetModel = () => service.delete('api/settings/model')
export const setServer = (url) => service.post('api/settings/server', { url })
export const resetServer = () => service.delete('api/settings/server')
export const getGlobalLlmCalls = (limit = 100) => service.get('api/settings/llm-calls', { params: { limit } })

// Scraper
export const getScrapeStatus = () => service.get('api/scrape')
export const refreshScrape = (topic = '') => service.post('api/scrape/refresh', { topic })
export const getSeedPosts = () => service.get('api/scrape/seed-posts')

export const getSimulationOntology = (simulationId) =>
  service.get(`api/simulation/${simulationId}/ontology`)

export const pauseSimulation = (simulationId) =>
  service.post('api/simulation/pause', { simulation_id: simulationId })

export const resumeSimulation = (simulationId, opts = {}) =>
  service.post('api/simulation/resume', { simulation_id: simulationId, ...opts })

export const updateAgentConfigs = (simulationId, agents, order) =>
  service.put(`api/simulation/${simulationId}/agents`, { agents, order })

export const injectEvent = (simulationId, content, author = 'User') =>
  service.post(`api/simulation/${simulationId}/inject-event`, { content, author })

export const getSimulationLlmCalls = (simulationId, limit = 50) =>
  service.get(`api/simulation/${simulationId}/llm-calls`, { params: { limit } })
