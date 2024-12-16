import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/views/Home.vue'
import Login from '@/components/views/Login.vue'
import Register from '@/components/views/Register.vue'
import User from '../components/views/User.vue'
import ProjectDetail from '../components/views/ProjectDetail.vue'
import ProjectLaunch from '@/components/views/ProjectLaunch.vue'
import UserApplied from '@/components/views/UserApplied.vue'
import UserLaunched from '@/components/views/UserLaunched.vue'
import Projects from '@/components/views/Projects.vue'
import Qualify from '@/components/views/Qualify.vue'

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
      name: 'Projects',
      component: Projects
    },
    {
      path: '/projects/launch',
      name: 'ProjectLaunch',
      component: ProjectLaunch,
      meta:{
        requiresLogin: 'true'
      }
    },
    {
      path: '/projects/:id',
      name: 'ProjectDetail',
      component: ProjectDetail,
    },
    {
      path: '/user/launched',
      name: 'UserLaunched',
      component: UserLaunched,
      meta:{
        requiresLogin: 'true'
      }
    },
    {
      path: '/user/applied',
      name: 'UserApplied',
      component: UserApplied,
      meta:{
        requiresLogin: 'true'
      }
    },
    {
      path: '/projects/:id/qualify',
      name: 'Qualify',
      component: Qualify,
      meta:{
        requiresLogin: 'true'
      }
    }
  ]
})