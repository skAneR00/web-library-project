<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <section class="books-layout">
    <div class="section-heading">
      <div>
        <p class="eyebrow">Каталог</p>
        <h1>Книги библиотеки</h1>
      </div>
      <div class="section-heading__actions">
        <RouterLink class="button button--ghost" :to="{ name: 'book-collections' }">
          Подборки
        </RouterLink>
        <RouterLink class="button button--primary" :to="{ name: 'favorites' }">
          Избранное
        </RouterLink>
      </div>
    </div>

    <RouterView />
  </section>
</template>
