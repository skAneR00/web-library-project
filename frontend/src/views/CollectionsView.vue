<script setup>
import { computed, onMounted, ref } from 'vue'
import LayoutCard from '../components/LayoutCard.vue'
import { booksApi } from '../services/booksApi'

const books = ref([])
const loading = ref(true)
const error = ref('')

const collections = computed(() => {
  const groups = new Map()

  for (const book of books.value) {
    const theme = book.theme || book.category || 'Без темы'
    const current = groups.get(theme) || []
    current.push(book)
    groups.set(theme, current)
  }

  return [...groups.entries()].sort(([first], [second]) => first.localeCompare(second, 'ru'))
})

const favorites = computed(() => books.value.filter((book) => book.is_favorite))
const reserved = computed(() => books.value.filter((book) => book.is_reserved))

onMounted(async () => {
  try {
    books.value = await booksApi.getBooks()
  } catch (requestError) {
    error.value = requestError.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="collections-view">
    <div v-if="loading" class="state-line">Загрузка подборок...</div>
    <div v-else-if="error" class="state-line state-line--error">{{ error }}</div>

    <template v-else>
      <div class="collection-summary">
        <LayoutCard dense>
          <span class="stat-value">{{ collections.length }}</span>
          <span class="stat-label">Тематические подборки</span>
        </LayoutCard>
        <LayoutCard dense>
          <span class="stat-value">{{ favorites.length }}</span>
          <span class="stat-label">Любимые книги</span>
        </LayoutCard>
        <LayoutCard dense>
          <span class="stat-value">{{ reserved.length }}</span>
          <span class="stat-label">Забронировано</span>
        </LayoutCard>
      </div>

      <div v-if="collections.length" class="collections-grid">
        <LayoutCard v-for="[theme, items] in collections" :key="theme">
          <template #header>
            <h2>{{ theme }}</h2>
            <p>{{ items.length }} книг в подборке</p>
          </template>

          <ul class="collection-list">
            <li v-for="book in items" :key="book.id">
              <strong>{{ book.title }}</strong>
              <span>{{ book.author }}, {{ book.year }}</span>
            </li>
          </ul>
        </LayoutCard>
      </div>

      <div v-else class="empty-state">
        <h2>Подборки пока не составлены</h2>
        <p>Добавьте книги и заполните поле тематической подборки.</p>
      </div>
    </template>
  </section>
</template>
