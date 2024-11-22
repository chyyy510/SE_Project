<template>
  <div class="user-center">
    <h2>个人中心</h2>
    <div class="avatar-section">
      <img :src="user.avatar||require('../../assets/logo.png')" alt="User Avatar" />
      <input type="file" @change="uploadAvatar" />
    </div>
    <div class="info-section">
      <label for="username">用户名</label>
      <input type="text" v-model="user.username" />
      <label for="password">密码</label>
      <input type="password" v-model="user.password" />
      <button @click="updateUserInfo">更新信息</button>
      
    </div>
    <button @click="logout">退出登录</button>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      user: {
        avatar: '', // 用户头像URL
        username: '', // 用户名
        password: '' // 密码
      },
      defaultAvatar: '../../assets/logo.png'
    };
  },
  methods: {
    uploadAvatar(event) {
      const file = event.target.files[0];
      // 上传头像逻辑
      // 例如：使用FormData上传到服务器
      const formData = new FormData();
      formData.append('avatar', file);
      // 假设我们有一个上传头像的API
      axios.post('/api/upload-avatar', formData)
        .then(response => {
          this.user.avatar = response.data.avatarUrl;
        })
        .catch(error => {
          console.error('上传头像失败', error);
        });
    },
    updateUserInfo() {
      // 更新用户信息逻辑
      // 例如：发送请求到服务器更新用户名和密码
      axios.post('/api/update-user', {
        username: this.user.username,
        password: this.user.password
      })
        .then(response => {
          alert('用户信息更新成功');
        })
        .catch(error => {
          console.error('更新用户信息失败', error);
        });
    },
    logout() {
      localStorage.setItem('loginFlag', 'false');
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.user-center {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
}
.avatar-section {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
.avatar-section img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 20px;
}
.info-section label {
  display: block;
  margin-top: 10px;
}
.info-section input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  margin-bottom: 10px;
}

h1 {
   align-items: center;
   color: #94070a;
}
</style>  