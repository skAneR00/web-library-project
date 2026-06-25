<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="not-found">
    <p class="eyebrow">404</p>
    <h1>Страница не найдена</h1>
    <p class="lead">Такого маршрута нет в ElectoLibrary.</p>
    <RouterLink class="button button--primary" :to="{ name: 'books' }">
      Вернуться в каталог
    </RouterLink>
  </section>
</template>
