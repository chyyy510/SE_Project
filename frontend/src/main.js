// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
//import './assets/global.css'

Vue.config.productionTip = false
Vue.prototype.$axios = axios;
//axios.defaults.baseURL = 'http://backend-ip:8000';
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})


router.beforeEach((to, from, next)=>{
  if(to.meta.requiresLogin == "true"){
      // 需要登录状态的页面
      if(localStorage.getItem("user")){
          next();
      }
      else{
          alert("请登录以继续");
          next('/login');
      }
  }
  else{
        next();
    }
})
