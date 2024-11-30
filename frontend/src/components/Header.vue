<!-- Header.vue -->
<template>
    <nav>
        <img src="../assets/logo.png" width="60px" height="auto">
        <div class="block">
            <div class="chosen" v-if="isActive('/home')">>></div>
                <router-link to="/home">主页</router-link>
            <div class="chosen" v-if="isActive('/home')"><<</div>
        </div>
        <div class="block">
            <div class="chosen" v-if="isActive('/projects')">>></div>
                <router-link to="/projects">实验</router-link>
            <div class="chosen" v-if="isActive('/projects')"><<</div>
        </div>
        <div class="block">
            <div class="chosen" v-if="isActive('/user')">>></div>
                <router-link to="/user">我的</router-link>
            <div class="chosen" v-if="isActive('/user')"><<</div>
        </div>
    </nav>
</template>
  
<script>
export default {
    name: 'Header',
    methods: { 
        isActive(path) { 
            return this.$route.path.startsWith(path); 
        } 
    }
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
    .block {
        width: 50px; 
        height: 50px; 
        background-color: #94070a; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        margin: 0px;
    }
    .block a{
        color: white;
        text-decoration: none;
    }
    .chosen{
        color: white;
    }
</style>
  