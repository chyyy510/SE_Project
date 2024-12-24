<template>
  <div class="launch-project">
    <h1>{{banner}}</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="title">项目名称</label>
        <input type="text" id="title" v-model="project.title" required />
      </div>
      <div class="form-group">
        <label for="date">日期</label>
        <input type="date" id="date" v-model="project.activity_time" required />
      </div>
      <div class="form-group">
        <label for="location">地点</label>
        <input type="text" id="location" v-model="project.activity_location" required />
      </div>
      <div class="form-group">
        <label for="person">所需人数</label>
        <input type="number" id="person" v-model="project.person_wanted" required />
      </div>
      <div class="form-group">
        <label for="money">人均报酬</label>
        <input type="number" id="money" v-model="project.money_per_person" required />
      </div>
      <div class="form-group">
        <label for="description">项目描述</label>
        <textarea id="description" v-model="project.description" required></textarea>
      </div>
      <div class="form-group">
        <label>添加标签</label>
        <div class="tag-box">
          <span v-for="tag in tags" @click="toggleTag(tag)" :class="{ selected: selectedTags.includes(tag) }">{{ tag.name }}</span>
        </div>
      </div>
      <button type="submit">提交</button>
    </form>
  </div>
</template>
<script>
import { getTag, postProject } from './api/api';

export default {
  name: 'ProjectEdit',
  props: {
    banner: {
      type: String,
      Required: true
    },
    mode: {
      type: String,
      Required: true
    },
    project: {
      type: Object,
      Required: true
    }
  },
  data() {
    return {
      tags: [],
      selectedTags: []
    };
  },
  created() {
    this.fetchTags();
  },
  methods: {
    fetchTags() {
      /*this.tags = [ { name: '标签1' }, { name: '标签2' }, { name: '标签3' } ];*/
      getTag()
        .then(response => {
          this.tags = response.data;
          console.log(this.tags);
        })
        .catch(error => {
          console.error('Error fetching tags:', error);
        });
    },
    toggleTag(tag) {
      const index = this.selectedTags.indexOf(tag);
      console.log(index);
      if (index === -1) {
        this.selectedTags.push(tag);
      } else {
        this.selectedTags.splice(index, 1);
      }
    },
    async submitForm() {
      this.project.tags = this.selectedTags;
      // 在这里处理表单提交逻辑
      const access = JSON.parse(localStorage.getItem('access'));
      try {
        await postProject(access, this.mode, this.project.id, this.project.title, this.project.activity_time, this.project.activity_location,
          this.project.person_wanted, this.project.money_per_person, this.project.description, project.tags);//等后端更新post函数：添加提交标签选项
        alert('项目已提交！');
        this.$router.push('/projects');
      } catch (error) {
        console.log(error.response.data.detail);
        return null;
      }
    }
  }
};
</script>
<style scoped>
.launch-project {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  color: #94070a;
}
textarea {
  width: 500px; /* 固定宽度 */
  resize: vertical;
}

.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
}
input, textarea {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #94070a;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
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
</style>
