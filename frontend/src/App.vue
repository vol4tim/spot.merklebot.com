<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Deck</RouterLink>
      <RouterLink to="/result">Result</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>

<style></style>
