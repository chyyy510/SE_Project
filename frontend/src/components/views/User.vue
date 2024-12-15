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
            <button @click="editField(field.name)" class="sort-button">修改</button>
          </div>
          <div v-if="editingField === field.name" class="edit-section">
            <label :for="field.name">{{ field.labelchange }}</label>
            <div class="edit-row">
              <input :type="field.name === 'password' ? 'password' : 'text'" v-model="user[field.name]" />
              <button @click="saveField" class="sort-button">保存</button>
              <button @click="cancelEdit" class="sort-button">取消</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <button @click="logout" class="sort-button">退出登录</button>
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
        email: '' // 邮箱
      },
      defaultAvatar: require('../../assets/logo.png'),
      editingField: null, // 当前正在编辑的字段
      fields: [
        { name: 'username', label: '用户名' , labelchange:'修改用户名：'},
        { name: 'password', label: '密码' , labelchange:'修改密码：'},
        { name: 'email', label: '邮箱' , labelchange:'修改绑定邮箱：'}
      ]
    };
  },
  created() {
    this.user = localStorage.getItem('user');
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
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
    editField(field) {
      this.editingField = field;
    },
    saveField() {
      axios.post('/api/update-user', {
        [this.editingField]: this.user[this.editingField]
      })
        .then(() => {
          localStorage.setItem(this.editingField, this.user[this.editingField]);
          alert('用户信息更新成功');
          this.editingField = null; // 关闭编辑模式
        })
        .catch(error => {
          console.error('更新用户信息失败', error);
        });
    },
    cancelEdit() {
      this.editingField = null;
    },
    logout() {
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


