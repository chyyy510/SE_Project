<template>
  <div class="activity-item">
    <h3>{{ activity.title }}</h3>
    <p>{{ activity.description }}</p>
    <p><strong>日期：</strong>{{ activity.date }}</p>
    <p><strong>地点：</strong>{{ activity.location }}</p>
  </div>
</template>

<script>
export default {
  name: 'Project',
  props: {
    activity: {
      type: Object,
      required: true
    }
  }
};
</script>

<style scoped>
.activity-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #fff;
}
.activity-item h3 {
  margin: 0 0 10px;
}
</style>
