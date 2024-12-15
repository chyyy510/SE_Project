<template>
  <div class="project-detail" v-if="!editMode">
    <img :src="project.publisherAvatar" alt="Publisher Avatar" class="avatar" />
    <h2>{{ project.title }}</h2>
    <p><strong>发布者：</strong>{{ project.publisherName }}</p>
    <p><strong>描述：</strong>{{ project.description }}</p>
    <p><strong>日期：</strong>{{ project.date }}</p>
    <p><strong>地点：</strong>{{ project.location }}</p>
    <p><strong>人均报酬：</strong>{{ project.money_per_person }}</p>
	  <p><strong>人数：</strong>{{ project.person_applied }}/{{ project.person_wanted }}</p>
    <div v-if="user.username==project.publisherName">
      <button @click="changeEditMode">{{button_text_edit}}</button>
      <button @click="qualifyApplier">{{button_text_qualify}}</button>
    </div>
    <div v-else>
      <button @click="applyForProject">{{button_text_apply}}</button>
    </div>
    
  </div>
  <div v-else>
    <button @click="changeEditMode">{{button_text_close_edit}}</button>
    <ProjectEdit :project="project" :banner="banner"/>
  </div>
</template>

<script>
import { getProject, postApply } from '../api/api';
import ProjectEdit from '../ProjectEdit.vue';

export default {
  name: 'ProjectDetail',
  components: {
    ProjectEdit
  },
  data() {
    return {
      banner:'编辑项目信息',
      project: {
        id:'',
        title :'',
        publisherName :'',
        description :'',
        date :'',
        location :'',
        money_per_person :'',
        person_applied :'',
        person_wanted :''
      },
      user: {
        avatar: '', // 用户头像URL
        username: '', // 用户名
        email: '', // 邮箱
        is_active:''
      },
      applied:false,
      button_text_apply:'申请参与',
      button_text_edit:'编辑实验信息',
      button_text_qualify:'审核候选人',
      button_text_close_edit:'结束编辑',
      editMode:false
    }
  },
  created()
    {
      this.getId();
      if(localStorage.getItem('user'))
      this.user = localStorage.getItem('user');
    },
  methods: {
    getId(){
      const currentUrl = window.location.href;
      const idMatch = currentUrl.match(/\/projects\/(\d+)$/);
      if (idMatch) {
        this.project.id = idMatch[1];
        console.log('Project ID:', this.project.id);
        this.project=getProject(this.project.id);
      } 
      else {
        console.log('未找到项目 ID');
        alert("未找到项目");
        this.$router.push('\projects');
      }
    },
    async applyForProject() {
      if(localStorage.getItem("user").is_active) {
        await postApply(this.user.name,this)
          alert('申请成功！');
          this.applied=true;
          this.button_text_apply='取消申请'
      }
      else{
          alert("请登录以继续");
          this.$router.push('/login');
      }
    },
    qualifyApplier() {
      this.$router.push(`/projects/${this.projectId}/qualify`);
    },
    changeEditMode() {
      this.editMode=!this.editMode;  
    }
  }
};
</script>

<style scoped>
.project-detail {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 20px;
}
button {
  padding: 10px 20px;
  background-color: #94070a;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #94070a;
}
</style>
