import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/views/Home.vue'
import Login from '@/components/views/Login.vue'
import Register from '@/components/views/Register.vue'
import User from '../components/views/User.vue'
import ProjectSearch from '../components/views/ProjectSearch.vue'
import ProjectDetail from '../components/views/ProjectDetail.vue'
import ProjectLaunch from '@/components/views/ProjectLaunch.vue'

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
    },
    { path: '/user', 
      name: 'User', 
      component: User ,
      meta:{
        requiresLogin: 'true'
      }
    },
    { path: '/projects',
      name: 'ProjectSearch',
      component: ProjectSearch
    },
    {
      path: '/projects/:id',
      name: 'ProjectDetail',
      component: ProjectDetail,
      props: true
    },
    {
      path: '/projects/launch',
      name: 'ProjectLaunch',
      component: ProjectLaunch,
      meta:{
        requiresLogin: 'true'
      }
    }
  ]
})