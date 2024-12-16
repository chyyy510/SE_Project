<template>
  <div class="project-list">
    <div v-if="appliers.length === 0">暂无人申请</div>
    <div v-else>
      <div v-for="applier in appliers" :key="applier.username" class="applier-item">
        <Applier :applier="applier" />
        <button @click="qualified(applier)">{{ button_text_qualify }}</button>
      </div>
    </div>
  </div>
</template>
  
<script>
import Applier from '../Applier.vue';

export default {
  name: 'Qualify',
	components: {
		Applier
	},
  data() {
      return {
        project:'',
				appliers:[],
        button_text_qualify:'通过',
			}
  },
  created() {
    /*this.getId();
    //const username=JSON.parse(localStorage.getItem('user')).username;
    //const project=getProject(this.project.id);
    if(username!=project.publisherName)
    {
      console.log('无查看权限');
      alert("无查看权限");
      this.$router.push('\projects');
    }*/
    console.log('项目ID');
    this.appliers=[{username:'6',description:'666',status:'passed'},{username:'1',description:'No.1',status:'not passed'}];
  },
  methods:{
    getId(){
      const currentUrl = window.location.href;
      const idMatch = currentUrl.match(/\/projects\/(\d+)$/);
      if (idMatch) {
        this.project.id = idMatch[1];
        console.log('Project ID:', this.project.id);
        this.project=getProject(this.project.id);
      } 
      else {
        console.log('未找到项目 ID');
        alert("未找到项目");
        this.$router.push('\projects');
      }
    },
    qualified(applier)
    {

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
button {
  padding: 10px 20px;
  background-color: #94070a;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>  