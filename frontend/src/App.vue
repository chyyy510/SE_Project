<!-- App.vue -->
<template>
  <div>
      <Header/>
      <UserHeader v-if="showSidebar"/>
      <router-view/>
  </div>
</template>

<script>
import Header from './components/Header.vue';
import UserHeader from './components/UserHeader.vue';
export default {
  name: 'App',
  components: {
    Header,
    UserHeader
  },
  data() { 
    return { 
      showSidebar: false // 初始状态下隐藏侧边栏 
    } 
  }, 
  watch: {
    $route(to) {
      this.showSidebar = this.checkRoute(to) 
    } 
  },
  created() { // 初始化时检查当前路由 
    this.showSidebar = this.checkRoute(this.$route) 
  },
  methods: { 
    checkRoute(route) { // 根据路由路径判断是否显示侧边栏 
      const routesWithSidebar = ['/user','/user/launched','/user/applied'];
      return routesWithSidebar.includes(route.path) 
    } 
  }
}
</script>

<style>
</style>
