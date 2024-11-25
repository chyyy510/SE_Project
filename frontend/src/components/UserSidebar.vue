<template>
    <div class="sidebar">
      <ul>
        <li><router-link to="/user">个人中心</router-link></li>
        <li><router-link to="/user/launched">已发布</router-link></li>
        <li><router-link to="/user/applied">已参与</router-link></li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'UserSidebar'
  }
  </script>
  
  <style scoped>
  .sidebar {
    width: 200px;
    height: 100vh;
    background-color: #94070a;
    color: white;
    position: fixed;
    top: 0;
    left: 0;
    padding: 20px;
    margin-top: 145px;
    margin-left: 8px;
  }
  .sidebar ul {
    list-style: none;
    padding: 0;
  }
  .sidebar li {
    margin: 20px 0;
  }
  .sidebar a {
    color: white;
    text-decoration: none;
  }
  </style>
  