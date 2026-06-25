<script setup>
defineProps({
  accent: {
    type: String,
    default: 'Спокойный режим',
  },
  dense: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <article class="layout-card" :class="{ 'layout-card--dense': dense }">
    <header v-if="$slots.header || $slots.actions" class="layout-card__header">
      <div>
        <slot name="header" />
      </div>
      <div v-if="$slots.actions" class="layout-card__actions">
        <slot name="actions" />
      </div>
    </header>

    <div class="layout-card__body">
      <slot />
    </div>

    <footer v-if="$slots.footer" class="layout-card__footer">
      <slot name="footer" :accent="accent" :dense="dense" />
    </footer>
  </article>
</template>
