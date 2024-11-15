<template>
  <div class="register-container">
    <form @submit.prevent="register">
      <h2>注册</h2>
      <div class="form-group">
        <label for="username">用户名</label>
        <input type="text" id="username" v-model="username" required 
        oninvalid="this.setCustomValidity('请输入用户名')"
        oninput="this.setCustomValidity('')"/>
      </div>
      <div class="form-group">
        <label for="email">邮箱</label>
        <input type="email" id="email" v-model="email" required 
        oninvalid="this.setCustomValidity('请输入正确的邮箱')"
        oninput="this.setCustomValidity('')" />
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input type="password" id="password" v-model="password" required 
        oninvalid="this.setCustomValidity('请输入密码')"
        oninput="this.setCustomValidity('')"/>
      </div>
      <div class="form-group form-inline">
        <router-link to="/login">登录</router-link>
      </div>
      <button type="submit">注册</button>
    </form>
  </div>
</template>

<script>
import { postRegister } from '../api/api';
import axios from 'axios';
export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password: ''
    };
  },
  methods: {
    register() {
      postRegister(this.email, this.username, this.password);
      
      alert("注册成功");
      /*axios.get('http://localhost:8000/users')
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    if (error.response) {
      // 请求成功发出且服务器也响应了状态码，但状态代码超出了 2xx 的范围
      console.log('1');//error.response.data
      console.log('2');//error.response.status
      console.log('3');//error.response.headers
    } else if (error.request) {
      // 请求已经成功发起，但没有收到响应
      console.log('error1',error.request);//,error.request
    } else {
      // 发送请求时出了点问题
      console.log('Error2',error.message);// error.message
    }
    console.log('4');//error.config
  });

      this.$router.push('/login');*/
    }
  }
};
</script>

<style scoped>
.register-container {
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
label {
  display: block;
  margin-bottom: 5px;
}
input[type="text"],
input[type="email"],
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