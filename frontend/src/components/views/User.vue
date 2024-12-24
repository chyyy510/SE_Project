<template>
  <div class="user-center">
    <h2>个人中心</h2>
    <div class="left-section">
      <div class="avatar-section">
        <img :src="user.avatar || defaultAvatar" alt="User Avatar" />
        <button @click="triggerFileInput" class="sort-button edit-button">修改</button>
        <input type="file" ref="fileInput" @change="uploadAvatar" style="display: none;" />
      </div>
      <div class="info-section">
        <div class="info-item" v-for="field in fields" :key="field.name">
          <div class="info-row">
            <span class="label">{{ field.label }}:</span>
            <span class="value">{{ field.name === 'password' ? '******' : user[field.name] }}</span>
            <button v-if="field.name !== 'email'" @click="editField(field.name)" class="sort-button">修改</button>
          </div>
          <div v-if="editingField === field.name" class="edit-section">
            <label :for="field.name">{{ field.labelchange }}</label>
            <div class="edit-row">
              <input v-if="field.name === 'password'" type="password" v-model="oldPassword" placeholder="旧密码" />
              <input v-if="field.name === 'password'" type="password" v-model="newPassword" placeholder="新密码" />
              <input v-else :type="field.name === 'password' ? 'password' : 'text'" v-model="editingValue" />
              <button @click="saveField" class="sort-button">保存</button>
              <button @click="cancelEdit" class="sort-button">取消</button>
            </div>
          </div>
        </div>
        <div class="info-item">
          <div class="info-row">
            <span class="label">邮箱:</span>
            <span class="value">{{ user.email }}</span>
          </div>
        </div>
        <div class="info-item">
          <div class="info-row">
            <span class="label">个人点数:</span>
            <span class="value">{{ user.point }} 摆币</span>
            <button @click="rechargePoints" class="sort-button">充值</button>
          </div>
        </div>
      </div>
    </div>
    <button @click="logout" class="sort-button">退出登录</button>
  </div>
</template>

<script>
import { updateUserInfo, updateUserPassword, getUser, postUserAvatar } from '../api/api';
import JSEncrypt from 'jsencrypt';

export default {
  data() {
    return {
      user: {
        avatar: '', // 用户头像URL
        username: '', // 用户名
        email: '', // 邮箱
        introduction: '', // 个人简介
        point: '' // 个人点数
      },
      defaultAvatar: require('../../assets/logo.png'),
      editingField: null, // 当前正在编辑的字段
      editingValue: '', // 当前编辑的值
      oldPassword: '', // 旧密码
      newPassword: '', // 新密码
      fields: [
        { name: 'username', label: '用户名', labelchange: '修改用户名：' },
        { name: 'password', label: '密码', labelchange: '修改密码：' },
        { name: 'introduction', label: '个人简介', labelchange: '修改个人简介：' }
      ]
    };
  },
  created() {
    this.user = JSON.parse(localStorage.getItem('user'));
    const user_name = this.user.username;
    getUser(user_name)
      .then(response => {
        console.log(response.data);
        this.user.introduction = response.data.introduction;
        this.user.avatar = `http://10.129.241.91:8000/${response.data.avatar}`;
        console.log(this.user.avatar);
        this.user.username = '';
        this.user.username = user_name;//解决异步冲突
        this.user.point = response.data.point
      })
      .catch(error => {
        console.error('Error fetching user data:', error);
      });
  },
  methods: {
    getRsaCode(str) { // 加密方法
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
    refreshUserInfo(Avatar) {
      const user_name = this.user.username;
      getUser(user_name)
        .then(response => {
          console.log(response.data);
          this.user.introduction = response.data.introduction;
          this.user.avatar = Avatar;
          console.log(this.user.avatar);
          this.user.username = '';
          this.user.username = user_name;
        })
        .catch(error => {
          console.error('Error fetching user data:', error);
        });
    },
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    uploadAvatar(event) {
      const access = JSON.parse(localStorage.getItem('access'));
      const file = event.target.files[0];
      if (!file) {
        console.error('未选择文件');
        return;
      }

      const formData = new FormData();
      formData.append('avatar', file);
      console.log('FormData内容:', formData.get('avatar')); // 添加日志
      postUserAvatar(access, formData)
          .then(response => {
            const Avatar = `http://10.129.241.91:8000/${response.data.avatar}`;
            this.refreshUserInfo(Avatar);
            console.log(this.user.avatar);
          })
          .catch(error => {
            console.error('上传头像失败', error);
          });
    },
    editField(field) {
      this.editingField = field;
      this.editingValue = this.user[field];
    },
    saveField() {
      const access = JSON.parse(localStorage.getItem('access'));
      if (this.editingField === 'password') {
        console.log(this.oldPassword, this.newPassword);
        updateUserPassword(access,
          this.getRsaCode(this.oldPassword),
          this.getRsaCode(this.newPassword))
          .then(() => {
            alert('密码更新成功');
            this.editingField = null; // 关闭编辑模式
            this.oldPassword = '';
            this.newPassword = '';
          })
          .catch(error => {
            console.error('更新密码失败', error);
          });
      } else {
        // 更新其他字段逻辑
        updateUserInfo(access, {
          [this.editingField]: this.editingValue
        })
          .then(() => {
            this.user[this.editingField] = this.editingValue;
            localStorage.setItem(this.editingField, this.editingValue);
            alert('用户信息更新成功');
            this.editingField = null; // 关闭编辑模式
          })
          .catch(error => {
            console.error('更新用户信息失败', error);
          });
      }
    },
    cancelEdit() {
      this.editingField = null;
      this.editingValue = '';
      this.oldPassword = '';
      this.newPassword = '';
    },
    rechargePoints() {
      this.$router.push('/pay');
    },//充值逻辑在这里
    logout() {
      localStorage.setItem('loginFlag', 'false');
      localStorage.setItem('user', null);
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
  margin-bottom: 10px;
  position: relative;
}
.avatar-section {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
}
.avatar-section img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 20px;
}
.avatar-section .edit-button {
  margin-left: auto;
}
.info-section {
  margin-bottom: 20px;
}
.info-item {
  margin-bottom: 10px;
}
.info-row {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
}
.info-row .label {
  width: 80px;
  font-weight: bold;
}
.info-row .value {
  flex: 1;
}
.edit-section {
  margin-top: 10px;
}
.edit-row {
  display: flex;
  align-items: center;
}
.edit-row input {
  margin-right: 10px;
}
.sort-button {
  padding: 5px 10px;
  margin: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #fff;
  cursor: pointer;
}
.sort-button:hover {
  background-color: #94070a;
  color: #fff;
  border-color: #94070a;
}
</style>
