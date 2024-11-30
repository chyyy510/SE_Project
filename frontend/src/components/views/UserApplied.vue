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
        { id: 2, title: '老人陪伴', description: '陪伴老人聊天，帮助他们解决日常问题。', date: '2024-10-22', location: '北京市朝阳区', publisherName: '李四', publisherAvatar: 'path/to/avatar2.png' },
          // 更多活动条目...
        ],
    };
  },
  };
  </script>
  
  <style scoped>
  </style>
  