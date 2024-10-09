import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/views/Home.vue'
import Log from '@/components/views/Log.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/home',
      name: 'Home',
      component: Home
    },{
      path: '/login',
      name: 'Log',
      component: Log
    }
  ]
})
