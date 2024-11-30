<template>
  <div>
    <ProjectSearch :projects="projects" />
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
    projects: [
    { id: 1, title: '社区清洁', description: '帮助清洁社区公园。', date: '2024-10-20', location: '北京市海淀区', publisherName: '张三', publisherAvatar: 'path/to/avatar1.png' },
    // 更多活动条目...
      ],
  };
},
};
</script>

<style scoped>
</style>
