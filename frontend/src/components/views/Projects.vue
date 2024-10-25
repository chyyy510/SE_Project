<template>
    <div class="projects">
      <h3>{{ activity.title }}</h3>
      <p>{{ activity.description }}</p>
      <p><strong>日期:</strong> {{ activity.date }}</p>
      <p><strong>地点:</strong> {{ activity.location }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'prijects',
    props: {
      activity: Object
    }
  }
  </script>
  
  <style scoped>
  .projects {
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
  }
  </style>
  