<template>
  <div class="project">
    <div class="project-header">
      <h3>{{ project.title }}</h3>
    </div>
    <p>{{ project.description }}</p>
    <p><strong>日期：</strong>{{ project.activity_time }}</p>
    <p><strong>地点：</strong>{{ project.activity_location }}</p>
    <p><strong>人均报酬：</strong>{{ project.money_per_person }}</p>
    <p><strong>人数：</strong>{{ project.person_already }}/{{ project.person_wanted }}</p>
    <div class="tag-box">
      <div v-for="tag in tags">
        <span>{{ tag.name }}</span>
      </div>
    </div>
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
.tag-box {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 20px;
}
.tag-box span {
  display: inline-block;
  padding: 5px 10px;
  margin: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
}
</style>
