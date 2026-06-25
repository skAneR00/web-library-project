<script setup>
import { computed, nextTick, onMounted, reactive, ref, watch } from 'vue'
import LayoutCard from './LayoutCard.vue'

const currentYear = new Date().getFullYear()
const categories = ['0+', '6+', '12+', '16+', '18+']

const props = defineProps({
  initialBook: {
    type: Object,
    default: null,
  },
  mode: {
    type: String,
    default: 'create',
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['submit'])

const titleInput = ref(null)
const touched = ref(false)
const fileError = ref('')
const coverName = ref('')

const form = reactive({
  title: '',
  author: '',
  description: '',
  cover: '',
  publisher: '',
  category: '12+',
  year: currentYear,
  theme: '',
  status: 'available',
  is_favorite: false,
  is_reserved: false,
})

function fillForm(book) {
  Object.assign(form, {
    title: book?.title || '',
    author: book?.author || '',
    description: book?.description || '',
    cover: book?.cover || '',
    publisher: book?.publisher || '',
    category: book?.category || '12+',
    year: book?.year || currentYear,
    theme: book?.theme || '',
    status: book?.status || 'available',
    is_favorite: Boolean(book?.is_favorite),
    is_reserved: Boolean(book?.is_reserved),
  })
}

watch(
  () => props.initialBook,
  (book) => {
    fillForm(book)
  },
  { immediate: true },
)

watch(
  () => form.title,
  (title) => {
    if (!form.theme && title.toLowerCase().includes('vue')) {
      form.theme = 'Веб-разработка'
    }
  },
)

onMounted(() => {
  nextTick(() => titleInput.value?.focus())
})

const errors = computed(() => {
  const nextErrors = {}

  if (!form.title.trim()) {
    nextErrors.title = 'Введите заголовок книги'
  }

  if (!form.author.trim()) {
    nextErrors.author = 'Введите автора'
  }

  if (form.description.trim().length < 20) {
    nextErrors.description = 'Описание должно быть не короче 20 символов'
  }

  if (!form.publisher) {
    nextErrors.publisher = 'Введите издательство'
  }

  if (!form.category) {
    nextErrors.category = 'Выберите возрастную категорию'
  }

  if (!Number.isInteger(Number(form.year)) || form.year < 1450 || form.year > currentYear + 1) {
    nextErrors.year = `Год должен быть от 1450 до ${currentYear + 1}`
  }

  return nextErrors
})

const isValid = computed(() => Object.keys(errors.value).length === 0 && !fileError.value)
const submitText = computed(() => (props.mode === 'edit' ? 'Сохранить изменения' : 'Создать книгу'))

function showError(field) {
  return touched.value && errors.value[field]
}

function handleCover(event) {
  const file = event.target.files?.[0]
  fileError.value = ''
  coverName.value = ''

  if (!file) {
    return
  }

  if (file.type !== 'image/jpeg') {
    fileError.value = 'Загрузите обложку в формате JPG'
    event.target.value = ''
    return
  }

  coverName.value = file.name
  const reader = new FileReader()
  reader.onload = () => {
    form.cover = reader.result
  }
  reader.readAsDataURL(file)
}

function submitForm() {
  touched.value = true

  if (!isValid.value) {
    return
  }

  emit('submit', {
    ...form,
    title: form.title.trim(),
    author: form.author.trim(),
    description: form.description.trim(),
    publisher: form.publisher.trim(),
    theme: form.theme.trim(),
    year: Number(form.year),
  })
}
</script>

<template>
  <LayoutCard class="book-form-card" :accent="submitText">
    <template #header>
      <h2>{{ mode === 'edit' ? 'Редактирование книги' : 'Новая книга' }}</h2>
      <p>Поля соответствуют базовому библиографическому описанию: заголовок, автор, выходные данные.</p>
    </template>

    <form class="book-form" @submit.prevent="submitForm">
      <label>
        <span>Заголовок</span>
        <input ref="titleInput" v-model.trim="form.title" type="text" placeholder="Название книги" />
        <small v-if="showError('title')">{{ errors.title }}</small>
      </label>

      <label>
        <span>Автор</span>
        <input v-model.trim="form.author" type="text" placeholder="Фамилия И. О." />
        <small v-if="showError('author')">{{ errors.author }}</small>
      </label>

      <label>
        <span>Описание</span>
        <textarea v-model.trim="form.description" rows="5" placeholder="Краткая аннотация" />
        <small v-if="showError('description')">{{ errors.description }}</small>
      </label>

      <div class="form-grid">
        <label>
          <span>Издательство</span>
          <input v-model.trim="form.publisher" type="text" placeholder="Например, Эксмо" />
          <small v-if="showError('publisher')">{{ errors.publisher }}</small>
        </label>

        <label>
          <span>Год издания</span>
          <input v-model.number="form.year" type="number" min="1450" :max="currentYear + 1" />
          <small v-if="showError('year')">{{ errors.year }}</small>
        </label>
      </div>

      <label>
        <span>Тематическая подборка</span>
        <input v-model.trim="form.theme" type="text" placeholder="Например, Фантастика" />
      </label>

      <fieldset>
        <legend>Категория</legend>
        <label v-for="category in categories" :key="category" class="radio-pill">
          <input v-model="form.category" type="radio" name="category" :value="category" />
          <span>{{ category }}</span>
        </label>
        <small v-if="showError('category')">{{ errors.category }}</small>
      </fieldset>

      <label class="file-field">
        <span>Обложка JPG</span>
        <input type="file" accept="image/jpeg" @change="handleCover" />
        <em>{{ coverName || (form.cover ? 'Обложка уже загружена' : 'Файл не выбран') }}</em>
        <small v-if="fileError">{{ fileError }}</small>
      </label>

      <div class="form-actions">
        <button class="button button--primary" type="submit" :disabled="loading">
          {{ loading ? 'Сохранение...' : submitText }}
        </button>
      </div>
    </form>
  </LayoutCard>
</template>
