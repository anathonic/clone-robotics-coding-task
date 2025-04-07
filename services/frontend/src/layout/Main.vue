<template>
  <Navigation/>
  <router-view />
  <Footer/>
</template>

<script setup lang="ts">
import Footer from "@/layout/Footer.vue";
import Navigation from "@/layout/Navigation.vue";
</script>