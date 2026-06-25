<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import LayoutCard from '../components/LayoutCard.vue'
import { booksApi } from '../services/booksApi'

const books = ref([])
const loading = ref(true)

const stats = computed(() => ({
  total: books.value.length,
  available: books.value.filter((book) => book.status === 'available').length,
  favorite: books.value.filter((book) => book.is_favorite).length,
  reserved: books.value.filter((book) => book.is_reserved).length,
}))

const recentBooks = computed(() =>
  [...books.value]
    .sort((first, second) => new Date(second.created_at) - new Date(first.created_at))
    .slice(0, 4),
)

onMounted(async () => {
  try {
    books.value = await booksApi.getBooks()
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="home-view">
    <div class="dashboard-hero">
      <div>
        <p class="eyebrow">SPA на Vue 3 и FastAPI</p>
        <h1>ElectoLibrary</h1>
        <p class="lead">
          Электронный каталог для учета книг, бронирования, любимых изданий и тематических подборок.
        </p>
        <div class="hero-actions">
          <RouterLink class="button button--primary" :to="{ name: 'books' }">
            Электронный каталог
          </RouterLink>
          <RouterLink class="button button--ghost" :to="{ name: 'favorites' }">
            Избранное
          </RouterLink>
        </div>
      </div>

      <div class="cover-stack" aria-label="Последние книги">
        <article v-for="book in recentBooks" :key="book.id" class="cover-stack__book">
          <span>{{ book.category }}</span>
          <strong>{{ book.title }}</strong>
          <small>{{ book.author }}</small>
        </article>
        <article v-if="!recentBooks.length && !loading" class="cover-stack__book">
          <span>EL</span>
          <strong>Каталог пуст</strong>
          <small>Добавьте первую книгу</small>
        </article>
      </div>
    </div>

    <div class="stats-grid">
      <LayoutCard v-for="item in [
        ['Всего книг', stats.total],
        ['В наличии', stats.available],
        ['Любимые', stats.favorite],
        ['Брони', stats.reserved],
      ]" :key="item[0]" dense>
        <span class="stat-value">{{ loading ? '...' : item[1] }}</span>
        <span class="stat-label">{{ item[0] }}</span>
      </LayoutCard>
    </div>
  </section>
</template>
