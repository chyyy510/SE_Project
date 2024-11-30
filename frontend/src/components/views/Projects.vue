<template>
    <div>
        <ProjectSearch :projects="projects" />
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
    data() {
        return {
            projects: [
            { id: 1, title: '社区清洁', description: '帮助清洁社区公园。', date: '2024-10-20', location: '北京市海淀区', publisherName: '张三', publisherAvatar: 'path/to/avatar1.png' },
            { id: 2, title: '老人陪伴', description: '陪伴老人聊天，帮助他们解决日常问题。', date: '2024-10-22', location: '北京市朝阳区', publisherName: '李四', publisherAvatar: 'path/to/avatar2.png' },
            // 更多活动条目...
            ],
        };
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