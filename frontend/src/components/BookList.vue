<script setup>
import BookItem from './BookItem.vue'

defineProps({
  books: {
    type: Array,
    required: true,
  },
  mode: {
    type: String,
    default: 'client',
  },
})

defineEmits(['edit', 'delete', 'toggle-status', 'toggle-favorite', 'toggle-reserve'])
</script>

<template>
  <div v-if="books.length" class="book-list">
    <BookItem
      v-for="book in books"
      :key="book.id"
      :book="book"
      :mode="mode"
      @edit="$emit('edit', $event)"
      @delete="$emit('delete', $event)"
      @toggle-status="$emit('toggle-status', $event)"
      @toggle-favorite="$emit('toggle-favorite', $event)"
      @toggle-reserve="$emit('toggle-reserve', $event)"
    />
  </div>

  <div v-else class="empty-state">
    <slot name="empty">
      <h2>Книги не найдены</h2>
      <p>Измените фильтр или добавьте первую книгу в каталог.</p>
    </slot>
  </div>
</template>
