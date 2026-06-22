import service from './index'

export const login = (data) => service.post('api/auth/login', data)
export const register = (data) => service.post('api/auth/register', data)
export const logout = () => service.post('api/auth/logout')
export const getMe = () => service.get('api/auth/me')

export const getModelRequests = () => service.get('api/auth/model-requests')
export const submitModelRequest = (model) => service.post('api/auth/model-request', { model })
export const approveModelRequest = (id) => service.post(`api/auth/model-requests/${id}/approve`)
export const denyModelRequest = (id) => service.post(`api/auth/model-requests/${id}/deny`)
