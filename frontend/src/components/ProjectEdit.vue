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
        <button type="submit">提交</button>
      </form>
    </div>
</template>
  
<script>
import { postProject } from './api/api';

export default {
  name: 'ProjectLaunch',
  props:{
    banner:{
      type:Object,
      Required:true
    },
    mode:{
      type:Object,
      Required:true
    },
    project:{
      type:Object,
      Required:true
    }
  },
    methods: {
      async submitForm() {
        // 在这里处理表单提交逻辑
        const access=JSON.parse(localStorage.getItem('access'));
        try{
          await postProject(access, this.mode, this.project.title, this.project.activity_time, this.project.activity_location,
                        this.project.person_wanted, this.project.money_per_person, this.project.description);
          alert('项目已提交！');
          this.$router.push('/projects');
        }
        catch(error) {
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
</style>
  