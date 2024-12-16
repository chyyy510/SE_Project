<template>
  <div class="applier-item">
    <h3>{{ applier.username }}</h3>
    <p>{{ applier.description }}</p>
    <p><strong>审核状态：</strong>{{ applier.status }}</p>
  </div>
</template>

<script>
export default {
  name: 'Applier',
  props: {
    applier: {
      type: Object,
      required: true
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
}
.applier-item h3 {
  margin: 0 0 10px;
}
</style>
