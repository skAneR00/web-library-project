<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import BookList from '../components/BookList.vue'
import LayoutCard from '../components/LayoutCard.vue'
import { adminAuth } from '../services/adminAuth'
import { booksApi } from '../services/booksApi'

const router = useRouter()
const books = ref([])
const password = ref('')
const loading = ref(false)
const loginLoading = ref(false)
const isAuthorized = ref(adminAuth.isAuthenticated())
const error = ref('')
const statusFilter = ref('all')

const visibleBooks = computed(() => {
  if (statusFilter.value === 'all') {
    return books.value
  }

  return books.value.filter((book) => book.status === statusFilter.value)
})

async function loadBooks() {
  loading.value = true
  error.value = ''

  try {
    books.value = await booksApi.getBooks()
  } catch (requestError) {
    error.value = requestError.message
  } finally {
    loading.value = false
  }
}

async function login() {
  loginLoading.value = true
  error.value = ''

  try {
    await adminAuth.login(password.value)
    password.value = ''
    isAuthorized.value = true
    await loadBooks()
  } catch (requestError) {
    error.value = requestError.message
  } finally {
    loginLoading.value = false
  }
}

function logout() {
  adminAuth.logout()
  isAuthorized.value = false
  books.value = []
}

function editBook(book) {
  router.push({ name: 'admin-book-edit', params: { id: book.id } })
}

function createBook() {
  router.push({ name: 'admin-book-new' })
}

async function updateBook(book, patch) {
  const updatedBook = await booksApi.updateBook(book.id, { ...book, ...patch })
  books.value = books.value.map((item) => (item.id === updatedBook.id ? updatedBook : item))
}

async function removeBook(book) {
  if (!confirm(`Удалить книгу "${book.title}"?`)) {
    return
  }

  try {
    await booksApi.deleteBook(book.id)
    books.value = books.value.filter((item) => item.id !== book.id)
  } catch (requestError) {
    error.value = requestError.message
  }
}

async function toggleStatus(book) {
  const nextStatus = book.status === 'available' ? 'unavailable' : 'available'

  try {
    await updateBook(book, {
      status: nextStatus,
      is_reserved: nextStatus === 'available' ? book.is_reserved : false,
    })
  } catch (requestError) {
    error.value = requestError.message
  }
}

onMounted(() => {
  if (isAuthorized.value) {
    loadBooks()
  }
})
</script>

<template>
  <section class="admin-view">
    <div class="section-heading">
      <div>
        <p class="eyebrow">Админка</p>
        <h1>Управление каталогом</h1>
      </div>
      <div v-if="isAuthorized" class="section-heading__actions">
        <button class="button button--ghost" type="button" @click="logout">Выйти</button>
        <button class="button button--primary" type="button" @click="createBook">Добавить книгу</button>
      </div>
    </div>

    <LayoutCard v-if="!isAuthorized" class="login-card">
      <template #header>
        <h2>Вход администратора</h2>
        <p>Пароль по умолчанию: admin123. Его можно изменить через переменную ADMIN_PASSWORD.</p>
      </template>

      <form class="login-form" @submit.prevent="login">
        <label>
          <span>Пароль</span>
          <input v-model.trim="password" type="password" autocomplete="current-password" />
        </label>
        <button class="button button--primary" type="submit" :disabled="loginLoading || !password">
          {{ loginLoading ? 'Проверка...' : 'Войти' }}
        </button>
      </form>
    </LayoutCard>

    <template v-else>
      <div class="toolbar admin-toolbar">
        <label>
          <span>Статус</span>
          <select v-model="statusFilter">
            <option value="all">Все</option>
            <option value="available">В наличии</option>
            <option value="unavailable">Нет в наличии</option>
          </select>
        </label>
      </div>

      <div v-if="loading" class="state-line">Загрузка админки...</div>
      <div v-else-if="error" class="state-line state-line--error">{{ error }}</div>

      <BookList
        v-else
        :books="visibleBooks"
        mode="admin"
        @edit="editBook"
        @delete="removeBook"
        @toggle-status="toggleStatus"
      >
        <template #empty>
          <h2>Книг нет</h2>
          <p>Создайте первую книгу через кнопку добавления.</p>
        </template>
      </BookList>
    </template>
  </section>
</template>
