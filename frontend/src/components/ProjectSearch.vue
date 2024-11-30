<template>
    <div class="project-list">
      <input type="text" v-model="searchQuery" placeholder="搜索活动..." v-if="!showDetail" />
      <div v-if="filteredProjects.length === 0">没有找到相关活动</div>
      <div v-else>
        <div v-for="project in filteredProjects" :key="project.id" @click="showProjectDetail(project)" class="project-item">
            <Project :project="project" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Project from './views/Project.vue';
  import ProjectDetail from './views/ProjectDetail.vue';
  import { debounce } from 'lodash';
  
  export default {
    name: 'ProjectSearch',
    components: {
      ProjectDetail,
      Project
    },
    props: {
      projects: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        searchQuery: '',
        projects: [
          { id: 1, title: '社区清洁', description: '帮助清洁社区公园。', date: '2024-10-20', location: '北京市海淀区', publisherName: '张三', publisherAvatar: 'path/to/avatar1.png' },
          { id: 2, title: '老人陪伴', description: '陪伴老人聊天，帮助他们解决日常问题。', date: '2024-10-22', location: '北京市朝阳区', publisherName: '李四', publisherAvatar: 'path/to/avatar2.png' },
          // 更多活动条目...
        ],
        showDetail: false,
        selectedProject: null
      };
    },
    computed: {
      filteredProjects() {
        return this.projects.filter(project => 
          project.title.includes(this.searchQuery) || 
          project.description.includes(this.searchQuery) ||
          project.location.includes(this.searchQuery)||
          project.date.includes(this.searchQuery)
        );
      }
    },
    watch: {
      searchQuery: debounce(function(newQuery) {
        this.searchQuery = newQuery;
      }, 300)
    },
    methods: {
      showProjectDetail(project) {
        this.$router.push(`/projects/${project.id}`);
      },
      launchProject(){
        this.$router.push('/projects/launch');
      }
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
  .project-item {
    margin-bottom: 20px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: #fff;
    cursor: pointer;
  }
  .project-item:hover {
    background-color: #f0f0f0;
  }
  </style>
  