import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/views/Home.vue'
import Login from '@/components/views/Login.vue'
import Register from '@/components/views/Register.vue'
import Projects from '@/components/views/Projects.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/home'
    },{
      path: '/home',
      name: 'Home',
      component: Home
    },{
      path: '/login',
      name: 'Login',
      component: Login
    },{
      path: '/register',
      name: 'Register',
      component: Register
    },{
      path: '/projects',
      name: 'projects',
      component: Projects
    }
  ]
})
