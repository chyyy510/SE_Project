<!-- Header.vue -->
<template>
    <nav>
        <active :class="{ active: isActive('/user') ,disactive: !isActive('/user')}">
            <router-link to="/user">个人主页</router-link>
        </active>
        <active :class="{ active: isActive('/user/launched') ,disactive: !isActive('/user/launched')}">
            <router-link to="/user/launched">已发布</router-link>
        </active>
        <active :class="{ active: isActive('/user/applied') ,disactive: !isActive('/user/applied')}">
            <router-link to="/user/applied">已申请</router-link>
        </active>
    </nav>
</template>
  
<script>
export default {
    name: 'Header',
    methods: { 
        isActive(path) { 
            return this.$route.path === path; 
        } 
    }
}
</script>
  
<style scoped>
    nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: white;
        font-size: 20px;
        padding: 20px;
        padding-right: 60%;
    }
    .disactive {
        width: 40%; 
        height: 50px; 
        background-color: white; 
        display: flex; 
        align-items: center; 
        justify-content: center;  
        margin: 0px;
    }
    .disactive a{
        color: #94070a;
		text-decoration: none;
    }
    .active {
        width: 40%; 
        height: 50px; 
        background-color: #94070a; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        margin: 0px;
    }
    .active a{
        color: white;
		text-decoration: none;
    }
</style>
  