<template>
    <div class="project-list">
      <input type="text" v-model="searchQuery" placeholder="搜索活动..." v-if="!showDetail" />
      <div v-if="!showDetail">
        <div v-if="filteredActivities.length === 0">没有找到相关活动</div>
        <div v-else>
          <div v-for="activity in filteredActivities" :key="activity.id" @click="showActivityDetail(activity)" class="activity-item">
            <Project :activity="activity" />
          </div>
        </div>
      </div>
      <div v-else>
        <button @click="showDetail = false">返回</button>
        <ProjectDetail :project="selectedActivity" />
      </div>
    </div>
  </template>
  
  <script>
  import Project from './Project.vue';
  import ProjectDetail from './ProjectDetail.vue';
  import { debounce } from 'lodash';
  
  export default {
    name: 'UserApplied',
    components: {
      ProjectDetail,
      Project
    },
    data() {
      return {
        searchQuery: '',
        activities: [
          { id: 2, title: '老人陪伴', description: '陪伴老人聊天，帮助他们解决日常问题。', date: '2024-10-22', location: '北京市朝阳区', publisherName: '李四', publisherAvatar: 'path/to/avatar2.png' },
          // 更多活动条目...
        ],
        showDetail: false,
        selectedActivity: null
      };
    },
    computed: {
      filteredActivities() {
        return this.activities.filter(activity => 
          activity.title.includes(this.searchQuery) || 
          activity.description.includes(this.searchQuery) ||
          activity.location.includes(this.searchQuery)||
          activity.date.includes(this.searchQuery)
        );
      }
    },
    watch: {
      searchQuery: debounce(function(newQuery) {
        this.searchQuery = newQuery;
      }, 300)
    },
    methods: {
      showActivityDetail(activity) {
        this.selectedActivity = activity;
        this.showDetail = true;
      },
    }
  };
  </script>
  
  <style scoped>
  .project-list {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  input[type="text"] {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  .activity-item {
    margin-bottom: 20px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: #fff;
    cursor: pointer;
  }
  .activity-item:hover {
    background-color: #f0f0f0;
  }
  </style>
  