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
    async getRsaCode (str){ // 注册方法
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
    async register() {
      try{
        await postRegister(this.email, this.username, this.getRsaCode(this.password));
        alert("注册成功");
        this.$router.push('/login');
      }
      catch(error){
        return null;
      };

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