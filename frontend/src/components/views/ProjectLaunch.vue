<template>
    <ProjectEdit :project="project" :banner="banner" :mode="mode"/>
</template>
  
<script>
import ProjectEdit from '../ProjectEdit.vue';
export default {
  name: 'ProjectLaunch',
  components: {
    ProjectEdit
  },
    data() {
      return {
        mode:'create',
        banner:'发起新项目',
        project: {
          id :'',
          title :'',
          description :'',
          activity_time :'',
          activity_location :'',
          money_per_person :'',
          person_wanted :''
        },
      };
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
  