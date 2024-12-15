<template>
  <div class="project-list">
    <input type="text" v-model="searchQuery" placeholder="搜索活动..." @input="fetchProjects" v-if="!showDetail" />
    <div class="sort-buttons">
      <div class="sift-buttons">
        <button @click="toggleTagBox" :class="{ 'active': showTagBox }" class="tag-button">按标签筛选</button>
      </div>
      <div class="list-buttons">
        <button @click="toggleSortOrder" class="sort-button">{{ sortOrder === 'asc' ? '顺序显示' : '逆序显示' }}</button>
        <button @click="toggleSortBy" class="sort-button">{{ sortBy === 'id' ? '发布顺序' : '时间顺序' }}</button>
      </div>
    </div>
    <div v-if="showTagBox" class="tag-box">
      <span v-for="tag in tags" :key="tag.id" @click="toggleTag(tag)" :class="{ selected: selectedTags.includes(tag) }">{{ tag.name }}</span>
    </div>
    <div v-if="projects.length === 0">没有找到相关活动</div>
    <div v-else>
      <div v-for="project in projects" :key="project.id" @click="showProjectDetail(project)" class="project-item">
        <Project :project="project" />
      </div>
    </div>
  </div>
</template>


<script>
import Project from './Project.vue';
import ProjectDetail from './views/ProjectDetail.vue';
import { debounce } from 'lodash';
import { getSearch } from './api/api';

export default {
  name: 'ProjectSearch',
  components: {
    ProjectDetail,
    Project
  },
  props: {
    searchTag: {
      type: Object,
      Required: true
    },
  },
  data() {
    return {
      searchQuery: '',
      projects: [],
      tags: [],
      selectedTags: [],
      sortOrder: 'asc', // 默认排序顺序
      sortBy: 'id', // 默认排序依据
      showTagBox: false, // 标签选择框显示状态
      showDetail: false,
      selectedProject: null
    };
  },
  created() {
    this.fetchTags();
    this.fetchProjects();
  },
  watch: {
    searchQuery: debounce(function(newQuery) {
      this.fetchProjects();
    }, 300)
  },
  methods: {
    
  fetchProjects() {
    const tagVector = this.tags.map(tag => this.selectedTags.includes(tag) ? 1 : 0).join('');
    console.log(tagVector,this.searchQuery,this.sortOrder,this.sortBy);
    console.log(this.searchTag)
    /*getSearch(tagVector, this.searchQuery, this.sortOrder, this.sortBy)
      .then(response => {
        this.projects = response.data;
      })
      .catch(error => {
        console.error('Error fetching projects:', error);
      });*/
  
      this.projects= [
            { id: 100, title: '社区清洁', description: '帮助清洁社区公园。', date: '2024-10-20', location: '北京市海淀区', publisherName: '张三', publisherAvatar: 'path/to/avatar1.png' },
            { id: 2, title: '老人陪伴', description: '陪伴老人聊天，帮助他们解决日常问题。', date: '2024-10-22', location: '北京市朝阳区', publisherName: '李四', publisherAvatar: 'path/to/avatar2.png' },
          ];
    },
    fetchTags() {
      /*axios.get('/api/tags')
        .then(response => {
          this.tags = response.data;
        })
        .catch(error => {
          console.error('Error fetching tags:', error);
      });*/
        this.tags=[{ id: 1, name: '环保' }, { id: 2, name: '社区服务' }, { id: 3, name: '教育' },]
    },
    toggleTag(tag) {
      const index = this.selectedTags.indexOf(tag);
      if (index === -1) {
        this.selectedTags.push(tag);
      } else {
        this.selectedTags.splice(index, 1);
      }
      this.fetchProjects();
    },
    toggleTagBox() {
      this.showTagBox = !this.showTagBox;
    },
    toggleSortOrder() {
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      this.fetchProjects();
    },
    toggleSortBy() {
      this.sortBy = this.sortBy === 'id' ? 'time' : 'id';
      this.fetchProjects();
    },
    showProjectDetail(project) {
      this.$router.push({path: `/projects/${project.id}`,params:{projectId: project.id}});
    },
    launchProject() {
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
.sort-buttons {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
.sift-buttons {
  display: flex;
}
.list-buttons {
  display: flex;
}
.tag-button, .sort-button {
  padding: 5px 10px;
  margin: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #fff;
  cursor: pointer;
}
.tag-button.active, .sort-button:hover {
  background-color: #94070a;
  color: #fff;
  border-color: #94070a;
}
.tag-box {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 20px;
}
.tag-box span {
  display: inline-block;
  padding: 5px 10px;
  margin: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
}
.tag-box span.selected {
  background-color: #94070a;
  color: #fff;
  border-color: #94070a;
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
