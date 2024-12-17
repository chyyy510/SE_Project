<template>
  <div class="project-list">
    <div v-if="appliers.length === 0">暂无人申请</div>
    <div v-else>
      <div v-for="applier in appliers" :key="applier.username" class="applier-item">
        <Applier :applier="applier" :id="id"/>
      </div>
    </div>
  </div>
</template>
  
<script>
import { getApplier } from '../api/api';
import Applier from '../Applier.vue';

export default {
  name: 'Qualify',
	components: {
		Applier
	},
  data() {
      return {
        id: '',
				appliers:[],
        button_text_qualify:'资质审核通过',
			}
  },
  created() {
    this.getInfo();
    /*const username=JSON.parse(localStorage.getItem('user')).username;
    if(username!=project.publisherName)
    {
      console.log('无查看权限');
      alert("无查看权限");
      this.$router.push('\projects');
    }*/
  },
  methods:{
    getInfo(){
      const currentUrl = window.location.href;
      const idMatch = currentUrl.match(/\/projects\/(\d+)\/qualify$/);
      if (idMatch) {
        this.id = idMatch[1];
        console.log('Project ID:', this.id);
        this.fetchAppliers();
      } 
      else {
        console.log('未找到项目 ID');
        alert("未找到项目");
        this.$router.push('\projects');
      }
    },
    fetchAppliers() {
      const access=JSON.parse(localStorage.getItem('access'));
      getApplier(access, this.id)
        .then(response => {
          this.appliers = response.data.results;
        })
        .catch(error => {
          console.error('Error fetching appliers:', error);
        });
    }
  }
};
</script>
  
<style scoped>
.project-list {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.applier-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #fff;
}
</style>  