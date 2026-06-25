<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import BookList from '../components/BookList.vue'
import { booksApi } from '../services/booksApi'

const books = ref([])
const loading = ref(true)
const error = ref('')
const statusFilter = ref('all')
const sortMode = ref('created')
const searchQuery = ref('')
const filterNote = ref('Показаны все книги')

const filteredBooks = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()

  return books.value.filter((book) => {
    const matchesStatus = statusFilter.value === 'all' || book.status === 'available'
    const matchesSearch =
      !query ||
      book.title.toLowerCase().includes(query) ||
      book.author.toLowerCase().includes(query) ||
      (book.theme || '').toLowerCase().includes(query)

    return matchesStatus && matchesSearch
  })
})

const sortedBooks = computed(() => {
  return [...filteredBooks.value].sort((first, second) => {
    if (sortMode.value === 'title') {
      return first.title.localeCompare(second.title, 'ru')
    }

    return new Date(second.created_at) - new Date(first.created_at)
  })
})

watch([statusFilter, sortMode, searchQuery], () => {
  const statusText = statusFilter.value === 'all' ? 'все статусы' : 'только в наличии'
  const sortText = sortMode.value === 'title' ? 'по алфавиту' : 'по дате добавления'
  filterNote.value = `Фильтр: ${statusText}, сортировка: ${sortText}`
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

function replaceBook(updatedBook) {
  books.value = books.value.map((item) => (item.id === updatedBook.id ? updatedBook : item))
}

async function toggleFavorite(book) {
  try {
    replaceBook(await booksApi.setFavorite(book.id, !book.is_favorite))
  } catch (requestError) {
    error.value = requestError.message
  }
}

async function toggleReserve(book) {
  try {
    replaceBook(await booksApi.setReservation(book.id, !book.is_reserved))
  } catch (requestError) {
    error.value = requestError.message
  }
}

onMounted(loadBooks)
</script>

<template>
  <div class="books-view">
    <div class="toolbar">
      <label>
        <span>Поиск</span>
        <input v-model.trim="searchQuery" type="search" placeholder="Название, автор или тема" />
      </label>

      <label>
        <span>Статус</span>
        <select v-model="statusFilter">
          <option value="all">Все</option>
          <option value="available">В наличии</option>
        </select>
      </label>

      <label>
        <span>Сортировка</span>
        <select v-model="sortMode">
          <option value="created">По дате добавления</option>
          <option value="title">По алфавиту</option>
        </select>
      </label>
    </div>

    <p class="filter-note">{{ filterNote }}. Найдено: {{ sortedBooks.length }}.</p>

    <div v-if="loading" class="state-line">Загрузка каталога...</div>
    <div v-else-if="error" class="state-line state-line--error">{{ error }}</div>

    <BookList
      v-else
      :books="sortedBooks"
      mode="client"
      @toggle-favorite="toggleFavorite"
      @toggle-reserve="toggleReserve"
    >
      <template #empty>
        <h2>Нет книг по выбранным условиям</h2>
        <p>Сбросьте фильтр или создайте новую запись в каталоге.</p>
      </template>
    </BookList>
  </div>
</template>
