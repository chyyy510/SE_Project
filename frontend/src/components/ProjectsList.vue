<template>
    <div class="volunteer-list">
      <input type="text" v-model="searchQuery" placeholder="搜索活动..." />
      <div v-for="activity in filteredActivities" :key="activity.id">
        <VolunteerActivity :activity="activity" />
      </div>
    </div>
  </template>
  
  <script>
  import VolunteerActivity from './VolunteerActivity.vue';
  
  export default {
    name: 'VolunteerList',
    components: {
      VolunteerActivity
    },
    data() {
      return {
        searchQuery: '',
        activities: [
          { id: 1, title: '社区清洁', description: '帮助清洁社区公园。', date: '2024-10-20', location: '北京市海淀区' },
          { id: 2, title: '老人陪伴', description: '陪伴老人聊天，帮助他们解决日常问题。', date: '2024-10-22', location: '北京市朝阳区' },
          // 更多活动条目...
        ]
      };
    },
    computed: {
      filteredActivities() {
        return this.activities.filter(activity => 
          activity.title.includes(this.searchQuery) || 
          activity.description.includes(this.searchQuery) ||
          activity.location.includes(this.searchQuery)
        );
      }
    }
  }
  </script>
  
  <style scoped>
  .volunteer-list {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }
  input[type="text"] {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    box-sizing: border-box;
  }
  </style>
  