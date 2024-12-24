<template>
  <div class="project">
    <div class="project-header">
      <h3>{{ project.title }}</h3>
      <span class="project-tag">{{ project.tag }}</span> <!-- 在这里展示 tag -->
    </div>
    <p>{{ project.description }}</p>
    <p><strong>日期：</strong>{{ project.date }}</p>
    <p><strong>地点：</strong>{{ project.location }}</p>
    <p><strong>人均报酬：</strong>{{ project.money_per_person }}</p>
    <p><strong>人数：</strong>{{ project.person_applied }}/{{ project.person_wanted }}</p>
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
.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.project-tag {
  background-color: #94070a;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}
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
