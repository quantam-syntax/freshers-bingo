const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

function getHeaders(isFormData = false) {
  const headers = {}
  const token = localStorage.getItem('token')
  if (token) headers['Authorization'] = `Bearer ${token}`
  if (!isFormData) headers['Content-Type'] = 'application/json'
  return headers
}

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: { ...getHeaders(options.isFormData), ...options.headers },
  })
  const data = await response.json()
  if (response.status === 401) {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('role')
    window.location.href = '/'
    return
  }
  if (!response.ok) throw { status: response.status, ...data }
  return data
}

export const api = {
  signup(rollNo, name) {
    return request('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ roll_no: rollNo, name }),
    })
  },

  adminLogin(username, password) {
    return request('/api/admin/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    })
  },

  getMyCard() {
    return request('/api/bingo/me')
  },

  uploadCellPhoto(cellId, file) {
    const formData = new FormData()
    formData.append('photo', file)
    return request(`/api/bingo/cells/${cellId}/upload`, {
      method: 'POST',
      body: formData,
      isFormData: true,
    })
  },

  getChallenges() {
    return request('/api/challenges')
  },

  addChallenge(text) {
    return request('/api/challenges', {
      method: 'POST',
      body: JSON.stringify({ text }),
    })
  },

  updateChallenge(id, text) {
    return request(`/api/challenges/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ text }),
    })
  },

  deleteChallenge(id) {
    return request(`/api/challenges/${id}`, { method: 'DELETE' })
  },

  pickChallenge() {
    return request('/api/challenges/pick', { method: 'POST' })
  },

  undoChallenge(id) {
    return request(`/api/challenges/${id}/undo`, { method: 'POST' })
  },

  getWinners() {
    return request('/api/winners')
  },

  getStats() {
    return request('/api/stats')
  },

  getFreshers() {
    return request('/api/stats/freshers')
  },
}
