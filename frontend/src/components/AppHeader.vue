<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <header class="app-header">
    <RouterLink class="brand" :to="{ name: 'home' }" aria-label="ElectoLibrary">
      <span class="brand-mark">EL</span>
      <span>
        <strong>ElectoLibrary</strong>
        <small>электронная библиотека</small>
      </span>
    </RouterLink>

    <nav class="nav-links" aria-label="Главное меню">
      <RouterLink :to="{ name: 'home' }">Главная</RouterLink>
      <RouterLink :to="{ name: 'books' }">Каталог</RouterLink>
      <RouterLink :to="{ name: 'favorites' }">Избранное</RouterLink>
      <RouterLink :to="{ name: 'book-collections' }">Подборки</RouterLink>
      <RouterLink class="nav-action" :to="{ name: 'admin' }">Админка</RouterLink>
    </nav>
  </header>
</template>
