<template>
  <div>
    <ProjectSearch :searchTag="tag" />
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
      tag:'apply'
    };
  },
};
</script>
  
<style scoped>
</style>
  