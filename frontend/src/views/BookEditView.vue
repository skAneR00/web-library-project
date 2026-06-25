<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import BookForm from '../components/BookForm.vue'
import { booksApi } from '../services/booksApi'

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
})

const router = useRouter()
const book = ref(null)
const loading = ref(false)
const pageLoading = ref(true)
const error = ref('')

async function loadBook() {
  pageLoading.value = true
  error.value = ''

  try {
    book.value = await booksApi.getBook(props.id)
  } catch (requestError) {
    error.value = requestError.message
  } finally {
    pageLoading.value = false
  }
}

async function saveBook(payload) {
  loading.value = true
  error.value = ''

  try {
    await booksApi.updateBook(props.id, payload)
    router.push({ name: 'admin' })
  } catch (requestError) {
    error.value = requestError.message
  } finally {
    loading.value = false
  }
}

onMounted(loadBook)
</script>

<template>
  <section class="form-view">
    <div class="section-heading">
      <div>
        <p class="eyebrow">Админка</p>
        <h1>Редактирование книги</h1>
      </div>
    </div>
    <div v-if="pageLoading" class="state-line">Загрузка книги...</div>
    <div v-else-if="error && !book" class="state-line state-line--error">{{ error }}</div>
    <BookForm v-else mode="edit" :initial-book="book" :loading="loading" @submit="saveBook" />
    <p v-if="error && book" class="state-line state-line--error">{{ error }}</p>
  </section>
</template>
