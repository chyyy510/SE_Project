<template>
    <div>
        <ProjectSearch :searchTag="tag"/>
        <button class="circle-button" @click="launchProject()">+</button>
    </div>
</template>
  
<script>
import ProjectSearch from '../ProjectSearch.vue';
  
export default {
    name: 'Projects',
    components: {
        ProjectSearch,
    },
    data(){
        return{
            tag:null
        }
    },
    methods: {
        launchProject(){
            this.$router.push('/projects/launch');
        }
    }
  };
</script>
  
<style scoped>
.circle-button { 
    position: fixed; 
    bottom: 20px; 
    right: 20px;
    width: 50px; 
    height: 50px; 
    border: none; 
    background-color: #94070a; 
    color: white; 
    border-radius: 50%; /* 设置为圆形 */ 
    font-size: 24px; 
    cursor: pointer; 
}
</style>  