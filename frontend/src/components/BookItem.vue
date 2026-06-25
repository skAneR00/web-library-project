<script setup>
import { computed } from 'vue'
import LayoutCard from './LayoutCard.vue'

const props = defineProps({
  book: {
    type: Object,
    required: true,
  },
  mode: {
    type: String,
    default: 'client',
  },
})

defineEmits(['edit', 'delete', 'toggle-status', 'toggle-favorite', 'toggle-reserve'])

const statusLabel = computed(() =>
  props.book.status === 'available' ? 'В наличии' : 'Нет в наличии',
)

const statusAccent = computed(() =>
  props.book.status === 'available' ? 'Можно бронировать' : 'Только просмотр',
)

const yearLabel = computed(() => props.book.year || 'год не указан')
</script>

<template>
  <LayoutCard class="book-item" :accent="statusAccent">
    <template #header>
      <div class="book-item__title-line">
        <div class="book-cover" :class="{ 'book-cover--image': book.cover }">
          <img v-if="book.cover" :src="book.cover" :alt="`Обложка книги ${book.title}`" />
          <span v-else>{{ book.title.slice(0, 1).toUpperCase() }}</span>
        </div>
        <div>
          <h3>{{ book.title }}</h3>
          <p>{{ book.author }}</p>
        </div>
      </div>
    </template>

    <template #actions>
      <button
        v-if="mode === 'client'"
        class="icon-button"
        type="button"
        :title="book.is_favorite ? 'Убрать из любимого' : 'Добавить в любимое'"
        @click="$emit('toggle-favorite', book)"
      >
        {{ book.is_favorite ? '♥' : '♡' }}
      </button>
    </template>

    <div class="book-item__content">
      <p class="book-description">{{ book.description }}</p>

      <dl class="book-meta">
        <div>
          <dt>Издательство</dt>
          <dd>{{ book.publisher }}</dd>
        </div>
        <div>
          <dt>Год</dt>
          <dd>{{ yearLabel }}</dd>
        </div>
        <div>
          <dt>Категория</dt>
          <dd>{{ book.category }}</dd>
        </div>
        <div>
          <dt>Подборка</dt>
          <dd>{{ book.theme || 'без темы' }}</dd>
        </div>
      </dl>
    </div>

    <template #footer="{ accent }">
      <div class="book-item__footer">
        <div class="badges">
          <span class="badge" :class="book.status === 'available' ? 'badge--ok' : 'badge--muted'">
            {{ statusLabel }}
          </span>
          <span v-if="book.is_reserved" class="badge badge--warn">Забронирована</span>
          <span class="badge badge--soft">{{ accent }}</span>
        </div>

        <div class="book-actions">
          <button
            v-if="mode === 'admin'"
            class="button button--ghost"
            type="button"
            @click="$emit('edit', book)"
          >
            Редактировать
          </button>
          <button
            v-if="mode === 'admin'"
            class="button button--ghost"
            type="button"
            @click="$emit('toggle-status', book)"
          >
            Изменить статус
          </button>
          <button
            v-if="mode === 'client'"
            class="button button--ghost"
            type="button"
            :disabled="book.status !== 'available'"
            @click="$emit('toggle-reserve', book)"
          >
            {{ book.is_reserved ? 'Снять бронь' : 'Забронировать' }}
          </button>
          <button
            v-if="mode === 'admin'"
            class="button button--danger"
            type="button"
            @click="$emit('delete', book)"
          >
            Удалить
          </button>
        </div>
      </div>
    </template>
  </LayoutCard>
</template>
