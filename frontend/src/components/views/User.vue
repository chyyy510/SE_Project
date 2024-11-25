<template>
  <div class="user-center">
    <h2>个人中心</h2>
    <div class="left-section">
      <div class="avatar-section">
        <img :src="user.avatar || defaultAvatar" alt="User Avatar" />
      </div>
      <div class="info-section">
        <span class="username">{{ user.username }}</span>
      </div>
      <button @click="toggleEditMode">更新信息</button>
    </div>
    <div v-if="editMode" class="edit-section">
      <label for="username">用户名</label>
      <input type="text" v-model="user.username" />
      <label for="password">密码</label>
      <input type="password" v-model="user.password" />
      <label for="avatar">更换头像</label>
      <input type="file" @change="uploadAvatar" />
      <button @click="updateUserInfo">保存更改</button>
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
        password: '', // 密码
        email: '' // 邮箱
      },
      defaultAvatar: require('../../assets/logo.png'),
      editMode: false // 编辑模式开关
    };
  },
  created() {
    this.user.username = localStorage.getItem('username');
  },
  methods: {
    uploadAvatar(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('avatar', file);
      axios.post('/api/upload-avatar', formData)
        .then(response => {
          this.user.avatar = response.data.avatarUrl;
        })
        .catch(error => {
          console.error('上传头像失败', error);
        });
    },
    toggleEditMode() {
      this.editMode = !this.editMode;
    },
    updateUserInfo() {
      axios.post('/api/update-user', {
        username: this.user.username,
        password: this.user.password,
        email: this.user.email
      })
        .then(() => {
          localStorage.setItem('username', this.user.username);
          alert('用户信息更新成功');
          this.editMode = false; // 关闭编辑模式
        })
        .catch(error => {
          console.error('更新用户信息失败', error);
        });
    },
    logout() {
      localStorage.setItem('loginFlag', 'false');
      localStorage.setItem('username', '');
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