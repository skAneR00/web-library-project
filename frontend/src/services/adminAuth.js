import { booksApi } from './booksApi'

const TOKEN_KEY = 'electolibrary_admin_token'

export const adminAuth = {
  getToken() {
    return localStorage.getItem(TOKEN_KEY)
  },
  isAuthenticated() {
    return Boolean(this.getToken())
  },
  async login(password) {
    const { token } = await booksApi.login(password)
    localStorage.setItem(TOKEN_KEY, token)
    return token
  },
  logout() {
    localStorage.removeItem(TOKEN_KEY)
  },
  getHeaders() {
    const token = this.getToken()
    return token ? { Authorization: `Bearer ${token}` } : {}
  },
}
