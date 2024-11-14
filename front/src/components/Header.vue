<!-- Header.vue -->
<template>
    <header>
        <nav>
            <img src="../assets/logo.png" width="100px" height="auto">
            <router-link to="/home">主页</router-link>
            <router-link to="/projects">实验</router-link>
            <router-link to="/login">登录</router-link>
        </nav>
    </header>
</template>
  
<script>
export default {
    name: 'Header'
}
</script>
  
<style scoped>
    nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #94070a;
        font-size: 20px;
        padding: 20px;
        padding-right: 60px;
    }
    a {
        color: white;
        text-decoration: none;
    }
</style>
  