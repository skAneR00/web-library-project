const API_BASE = import.meta.env.VITE_API_URL || '/api'
const ADMIN_TOKEN_KEY = 'electolibrary_admin_token'

function adminHeaders() {
  const token = localStorage.getItem(ADMIN_TOKEN_KEY)
  return token ? { Authorization: `Bearer ${token}` } : {}
}

function jsonBody(payload) {
  return typeof payload === 'string' ? payload : JSON.stringify(payload)
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  })

  if (!response.ok) {
    let message = 'Ошибка запроса к серверу'

    try {
      const error = await response.json()
      message = error.detail || message
    } catch {
      message = response.statusText || message
    }

    throw new Error(message)
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

export const booksApi = {
  login(password) {
    return request('/auth/login', {
      method: 'POST',
      body: jsonBody({ password }),
    })
  },
  getBooks() {
    return request('/books')
  },
  getBook(id) {
    return request(`/books/${id}`)
  },
  createBook(book) {
    return request('/books', {
      method: 'POST',
      headers: adminHeaders(),
      body: jsonBody(book),
    })
  },
  updateBook(id, book) {
    return request(`/books/${id}`, {
      method: 'PUT',
      headers: adminHeaders(),
      body: jsonBody(book),
    })
  },
  deleteBook(id) {
    return request(`/books/${id}`, {
      method: 'DELETE',
      headers: adminHeaders(),
    })
  },
  setFavorite(id, value) {
    return request(`/books/${id}/favorite`, {
      method: 'PATCH',
      body: jsonBody({ value }),
    })
  },
  setReservation(id, value) {
    return request(`/books/${id}/reserve`, {
      method: 'PATCH',
      body: jsonBody({ value }),
    })
  },
}
