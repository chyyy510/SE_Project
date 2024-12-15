<template>
    <div v-for="applier in appliers" :key="applier.username" class="applier-item">
        <Applier :applier="applier" />
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
				appliers:[]
			}
  },
};
</script>
  
<style scoped>
.applier-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #fff;
  cursor: pointer;
}
</style>  