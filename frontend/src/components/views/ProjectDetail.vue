<template>
  <div class="project-detail" v-if="!editMode">
    <img :src="project.publisherAvatar" alt="Publisher Avatar" class="avatar" />
    <div class="project-header">
      <h2>{{ project.title }}</h2>
      <span class="project-tag">{{ project.tag }}</span> <!-- 在这里展示 tag -->
    </div>
    <p><strong>发布者：</strong>{{ project.creator }}</p>
    <p><strong>内容：</strong>{{ project.description }}</p>
    <p><strong>日期：</strong>{{ project.activity_time }}</p>
    <p><strong>地点：</strong>{{ project.activity_location }}</p>
    <p><strong>人均报酬：</strong>{{ project.money_per_person }}</p>
    <p><strong>人数：</strong>{{ project.person_already }}/{{ project.person_wanted }}</p>
    <div v-if="project.relationship=='creator'">
      <button @click="changeEditMode">编辑实验信息</button>
      <button @click="qualifyApplier">审核候选人</button>
    </div>
    <div v-else>
      <div v-if="project.relationship=='passer-by'||project.relationship=='to-qualify-user'">
        <button @click="applyForProject">{{button_text_apply}}</button>
      </div>
      <div v-else >
        <button class="applied">{{button_text_apply}}</button>
      </div>
    </div>
    <!-- 新增图片展示 -->
    <div class="image-container" @click="showImage = true">
      <img :src="project.image" alt="Project Image" class="project-image" />
    </div>
    <!-- 图片放大显示 -->
    <div v-if="showImage" class="image-modal" @click="showImage = false">
      <img :src="project.image" alt="Project Image" class="project-image-large" />
    </div>
  </div>
  <div v-else>
    <button @click="changeEditMode">结束编辑</button>
    <ProjectEdit :project="project" :banner="banner" :mode="mode"/>
  </div>
</template>

<script>
import { getProject, postApply, postDisApply } from '../api/api';
import ProjectEdit from '../ProjectEdit.vue';

export default {
  name: 'ProjectDetail',
  components: {
    ProjectEdit
  },
  data() {
    return {
      banner: '编辑项目信息',
      mode: 'edit',
      project: {
        id: '',
        title: '',
        publisherName: '',
        description: '',
        activity_time: '',
        activity_location: '',
        money_per_person: '',
        person_applied: '',
        person_wanted: '',
        relationship: '',
<<<<<<< HEAD
        tags: []
=======
        tag: '',
        image: '' // 新增图片字段
>>>>>>> 587f8d26a67781d284fc0d0c51ed9595b70fe071
      },
      user: {
        avatar: '', // 用户头像URL
        username: '', // 用户名
        email: '', // 邮箱
        is_active: ''
      },
      applied: false,
      button_text_apply: '',
      editMode: false,
      showImage: false // 控制图片放大显示
    }
  },
  created() {
    this.getInfo();
    //this.project.tag='tag1';//test
  },
  methods: {
    getInfo() {
      const currentUrl = window.location.href;
      const idMatch = currentUrl.match(/\/projects\/(\d+)$/);
      if (idMatch) {
        this.project.id = idMatch[1];
        console.log('Project ID:', this.project.id);
        const access = JSON.parse(localStorage.getItem('access'));
        getProject(access, this.project.id)
          .then(response => {
            this.project = response.data;
            this.project.image=`http://10.129.241.91:8000/${response.data.image}`
            if (this.project.relationship == 'passer-by')
              this.button_text_apply = '申请参与';
            if (this.project.relationship == 'to-qualify-user')
              this.button_text_apply = '取消申请';
            if(this.project.relationship == 'to-check-result')
              this.button_text_apply = '审核已通过';
            if(this.project.relationship == 'finish')
              this.button_text_apply = '已完成';
            console.log("关系", this.project.relationship);
            console.log("文本", this.button_text_apply);
          })
          .catch(error => {
            console.error('Error fetching project:', error);
          });
      } else {
        console.log('未找到项目 ID');
        alert("未找到项目");
        this.$router.push('\projects');
      }
    },
    async applyForProject() {
      if (localStorage.getItem("loginFlag") == 'true') {
        const access = JSON.parse(localStorage.getItem('access'));
        if(this.project.relationship=='passer-by')
        {
          await postApply(access, this.project.id)
            .catch(error => {
              console.error('Error Apply:', error);
              alert('申请失败！',error.response.data.detail);
            });
            alert('申请成功！');
        }
        if(this.project.relationship=='to-qualify-user')
        {
          await postDisApply(access, this.project.id)
            .catch(error => {
              console.log(error.response.data.detail);
              console.error('Error Apply:', error);
              alert('取消申请失败！', error.response.data.detail);
            });
            alert('取消申请成功！');
        }
        location.reload();
      } else {
        alert("请登录以继续");
        this.$router.push('/login');
      }
    },
    qualifyApplier() {
      this.$router.push(`/projects/${this.project.id}/qualify`);
    },
    changeEditMode() {
      this.editMode = !this.editMode;
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
.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.project-tag {
  background-color: #94070a;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  margin-left: 10px; /* 确保标签与标题之间有间距 */
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
button.applied {
  cursor: default;
}
.image-container {
  margin-top: 20px;
  text-align: center;
}
.project-image {
  max-width: 100%;
  cursor: pointer;
}
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}
.project-image-large {
  max-width: 90%;
  max-height: 90%;
}
</style>
