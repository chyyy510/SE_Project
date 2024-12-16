<template>
  <div class="project-item">
    <h3>{{ project.title }}</h3>
    <p>{{ project.description }}</p>
    <p><strong>发布者：</strong>{{ project.creator }}</p>
    <p><strong>日期：</strong>{{ project.activity_time }}</p>
    <p><strong>地点：</strong>{{ project.location }}</p>
	  <p><strong>人均报酬：</strong>{{ project.money_per_person }}</p>
	  <p><strong>人数：</strong>{{ project.person_already }}/{{ project.person_wanted }}</p>
  </div>
</template>

<script>
export default {
  name: 'Project',
  props: {
    project: {
      type: Object,
      required: true
    }
  }
};
</script>

<style scoped>
.project-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #fff;
}
.project-item h3 {
  margin: 0 0 10px;
}
</style>
