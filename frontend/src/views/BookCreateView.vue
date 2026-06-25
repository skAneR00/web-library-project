<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BookForm from '../components/BookForm.vue'
import { booksApi } from '../services/booksApi'

const router = useRouter()
const loading = ref(false)
const error = ref('')

async function createBook(book) {
  loading.value = true
  error.value = ''

  try {
    const createdBook = await booksApi.createBook(book)
    router.push({ name: 'admin-book-edit', params: { id: createdBook.id } })
  } catch (requestError) {
    error.value = requestError.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="form-view">
    <div class="section-heading">
      <div>
        <p class="eyebrow">Админка</p>
        <h1>Добавление книги</h1>
      </div>
    </div>
    <BookForm mode="create" :loading="loading" @submit="createBook" />
    <p v-if="error" class="state-line state-line--error">{{ error }}</p>
  </section>
</template>
