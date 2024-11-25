<template>
    <div class="launch-project">
      <h1>发起新项目</h1>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="projectName">项目名称</label>
          <input type="text" id="projectName" v-model="projectName" required />
        </div>
        <div class="form-group">
          <label for="projectDescription">项目描述</label>
          <textarea id="projectDescription" v-model="projectDescription" required></textarea>
        </div>
        <button type="submit">提交</button>
      </form>
    </div>
</template>
  
<script>
export default {
  name: 'ProjectLaunch',
    data() {
      return {
        projectName: '',
        projectDescription: ''
      };
    },
    methods: {
      submitForm() {
        // 在这里处理表单提交逻辑
        console.log('项目名称:', this.projectName);
        console.log('项目描述:', this.projectDescription);
        alert('项目已提交！');
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
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  button:hover {
    background-color: #0056b3;
  }
</style>
  