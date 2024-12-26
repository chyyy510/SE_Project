<template>
  <div class="project-list">
    <div class="search-container">
      <input type="text" v-model="searchKey" placeholder="搜索关键字..." class="search-input"/>
      <button @click="fetchProjects()" class="search-button">搜索</button>
    </div>
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
      <span v-for="tag in tags" @click="toggleTag(tag)" :class="{ selected: index&(1<<(tag.id-1)) }">{{ tag.name }}</span>
    </div>
    <div v-if="projects.length === 0">没有找到相关活动</div>
    <div v-else>
      <div v-for="project in projects" :key="project.id" @click="showProjectDetail(project)" class="project-item">
        <Project :project="project" /> 
      </div>
    </div>
    <div class="pagination-buttons">
      <button @click="fetchPreviousPage" :disabled="!previous" class="pagination-button">上一页</button>
      <button @click="fetchNextPage" :disabled="!next" class="pagination-button">下一页</button>
    </div>
  </div>
</template>

<script>
import Project from './Project.vue';
import ProjectDetail from './views/ProjectDetail.vue';
import { getSearch, getLaunchSearch, getApplySearch, getTag } from './api/api';

export default {
  name: 'ProjectSearch',
  components: {
    ProjectDetail,
    Project
  },
  props: {
    mode: {
      type: String,
      Required: true
    },
  },
  data() {
    return {
      searchKey: '',
      previous: '',
      next: '',
      projects: [],
      tags: [],
      index:0,
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
  methods: {
  fetchProjects(url = null) {
    console.error()
    console.log(this.searchKey, this.sortOrder, this.sortBy);
    console.log(this.mode);
    if (this.mode == '') {
      getSearch(this.searchKey, this.sortBy, this.sortOrder, url,this.index)
        .then(response => {
          this.projects = response.data.results;
          this.previous = response.data.previous;
          this.next = response.data.next;
          console.log(response.data.previous, response.data.next);
        })
        .catch(error => {
          console.error('Error fetching projects:', error);
        });
    } else {
      const access = JSON.parse(localStorage.getItem('access'));
      if (this.mode == 'create')
        getLaunchSearch(access, this.searchKey, this.sortBy, this.sortOrder, url)
          .then(response => {
            this.projects = response.data.results;
            this.previous = response.data.previous;
            this.next = response.data.next;
          })
          .catch(error => {
            console.error('Error fetching projects:', error);
          });
      if (this.mode == 'engage')
        getApplySearch(access, this.searchKey, this.sortBy, this.sortOrder, url)
          .then(response => {
            this.projects = response.data.results;
            this.previous = response.data.previous;
            this.next = response.data.next;
          })
          .catch(error => {
            console.error('Error fetching projects:', error);
          });
    }
  },
  fetchPreviousPage() {
    if (this.previous) {
      this.fetchProjects(this.previous);
    }
  },
  fetchNextPage() {
    if (this.next) {
      this.fetchProjects(this.next);
    }
  },
    fetchTags() {
      getTag()
        .then(response => {
          this.tags = response.data;
          console.log('Tag',this.tags);
        })
        .catch(error => {
          console.error('Error fetching tags:', error);
        });
    },
    toggleTag(tag) {
      this.index^=1<<(tag.id-1);
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
      this.$router.push({ path: `/projects/${project.id}`, params: { projectId: project.id } });
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
.search-container {
  display: flex;
  margin-bottom: 20px;
}
.search-input {
  flex: 1;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 5px 0 0 5px;
}
.search-button {
  padding: 10px 20px;
  background-color: #94070a;
  color: white;
  border: none;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
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
.pagination-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
.pagination-button {
  padding: 10px 20px;
  background-color: #94070a;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.pagination-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
