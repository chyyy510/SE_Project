<template>
  <div>
    <ProjectSearch :mode="mode" />
  </div>
</template>

<script>
import ProjectSearch from '../ProjectSearch.vue';

export default {
  name: 'UserApplied',
  components: {
    ProjectSearch,
  },
  data() {
    return {
        mode:'create'
      };
  },
};
</script>

<style scoped>
</style>
