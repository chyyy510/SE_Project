<template>
  <div class="project-detail">
    <img :src="project.publisherAvatar" alt="Publisher Avatar" class="avatar" />
    <h2>{{ project.title }}</h2>
    <p><strong>发布者：</strong>{{ project.publisherName }}</p>
    <p><strong>描述：</strong>{{ project.description }}</p>
    <p><strong>日期：</strong>{{ project.date }}</p>
    <p><strong>地点：</strong>{{ project.location }}</p>
    <button @click="applyForProject">申请参与</button>
  </div>
</template>

<script>
export default {
  name: 'ProjectDetail',
  props: {
    project: {
      type: Object,
      required: true
    }
  },
  methods: {
    applyForProject() {
      if(localStorage.getItem("loginFlag") == "true"){
          alert('申请成功！');
      }
      else{
          alert("请登录以继续");
          this.$router.push('/login');
      }
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
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style>
