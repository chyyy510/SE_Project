<template>
  <div class="login-container">
    <form @submit.prevent="login">
      <h2>登录</h2>
      <div class="form-group">
        <label for="email">邮箱</label>
        <input type="text" id="email" v-model="email" required oninvalid="this.setCustomValidity('请输入邮箱')"
          oninput="this.setCustomValidity('')" />
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input type="password" id="password" v-model="password" required oninvalid="this.setCustomValidity('请输入密码')"
          oninput="this.setCustomValidity('')" />
      </div>
      <div class="form-group form-inline">
        <router-link to="/register">注册</router-link>
        <div class="form-inline"><input type="checkbox" id="remember" v-model="remember" />
          <label for="remember">记住我</label>
        </div>
      </div>
      <button type="submit">登录</button>
    </form>
  </div>
</template>


<script>
import { postLogin } from '../api/api';
import JSEncrypt from 'jsencrypt';
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
    getRsaCode(str) { // 注册方法
      let pubKey = `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmIzophqDebSpnL77RK0l
6l8TECsiW7t1+7ilLuc0OtPBFgRaIyEUhjV90XY1LJcWZ3UmdZ77GBoHRcZa0UAE
8DF7seDu2yyXy2xE0i4gFo41WhOwIkV0SVlT7hQ+llf2w8Nk48efjjpz9v5Nf62I
VxRBcDQq3BUbvq/ZHbkUs7jiAIp2DeW4FBL3gj7C4yaCkis0HOHFSqCGxDfDr8Vg
Y9quJIoKfLDqMeXylBICW9tAdUSBC6nf8fdiFflvdenVb1VhZ64oseJMp+8Bqt5R
wTHjucdOXlXbhM+pooTEKu+FyVQcwbwkjL0MM8SnZcfozP9ZAlSiO+5vewrqiOhB
NwIDAQAB
-----END PUBLIC KEY-----`;// ES6 模板字符串 引用 rsa 公钥
      let encryptStr = new JSEncrypt();
      encryptStr.setPublicKey(pubKey); // 设置 加密公钥
      let data = encryptStr.encrypt(str.toString());  // 进行加密
      return data;
    },
    async login() {
      try{
        await postLogin(this.email, this.getRsaCode(this.password));
        alert("登录成功");
        localStorage.setItem('user', response.data.user);
        this.$router.push('/user');
      }
      catch(error){
        alert(error.response.data.detail);
        console.log(error.response.data.detail);
        return null;
      }
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
