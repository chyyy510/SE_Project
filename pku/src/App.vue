<!-- App.vue -->
<template>
  <div>
      <Header />
      <router-view/>
  </div>
</template>

<script>
import Header from './components/Header.vue';
export default {
  name: 'App',
  components: {
    Header
  }
}
</script>

<style scoped>
h1 {
  color: #dd0a0a;
}
</style>
