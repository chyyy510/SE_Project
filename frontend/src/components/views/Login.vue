<template>
  <div class="login-container">
    <form @submit.prevent="login">
      <h2>登录</h2>
      <div class="form-group">
        <label for="username">用户名</label>
        <input type="text" id="username" v-model="username" required 
        oninvalid="this.setCustomValidity('请输入用户名')"
        oninput="this.setCustomValidity('')"/>
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input type="password" id="password" v-model="password" required 
        oninvalid="this.setCustomValidity('请输入密码')"
        oninput="this.setCustomValidity('')"/>
      </div>
      <div class="form-group form-inline">
        <router-link to="/register">注册</router-link>
        <div class="form-inline"><input type="checkbox" id="remember" v-model="remember" />
        <label for="remember">记住我</label></div>
      </div>
      <button type="submit">登录</button>
    </form>
  </div>
</template>


<script>
import { user_login } from '../api/api';
import axios from 'axios';
export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      username: '',
      remember: false
    };
  },
  methods: {
    async login() { 
      try { 
        this.$router.push({ name: 'User' });
        const response = await user_login(this.email, this.password);
        if (response.data.is_active) { 
          // 登录成功，跳转到 User.vue 
          this.$router.push({ name: 'User' }); } 
        else { 
          // 登录失败，显示错误信息 
          this.errorMessage = 'Login failed. Please check your email and password.'; } 
        } 
          catch (error) { 
            // 处理请求错误 
            this.errorMessage = 'An error occurred. Please try again later.'; } 
          }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  color: #94070a;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.form-group {
  margin-bottom: 15px;
}
.form-inline {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
label {
  display: block;
  margin-bottom: 5px;
}
input[type="text"],
input[type="password"] {
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
a {
  color: #94070a;
  text-decoration: none;
}
</style>