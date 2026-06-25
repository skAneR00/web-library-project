<script setup>
import { computed, onMounted, ref } from 'vue'
import BookList from '../components/BookList.vue'
import { booksApi } from '../services/booksApi'

const books = ref([])
const loading = ref(true)
const error = ref('')

const favoriteBooks = computed(() => books.value.filter((book) => book.is_favorite))

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
  <section class="favorites-view">
    <div class="section-heading">
      <div>
        <p class="eyebrow">Пользовательская зона</p>
        <h1>Избранные книги</h1>
      </div>
    </div>

    <div v-if="loading" class="state-line">Загрузка избранного...</div>
    <div v-else-if="error" class="state-line state-line--error">{{ error }}</div>

    <BookList
      v-else
      :books="favoriteBooks"
      mode="client"
      @toggle-favorite="toggleFavorite"
      @toggle-reserve="toggleReserve"
    >
      <template #empty>
        <h2>Избранных книг пока нет</h2>
        <p>Добавьте книги сердечком в электронном каталоге.</p>
      </template>
    </BookList>
  </section>
</template>
