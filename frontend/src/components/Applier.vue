<template>
  <div class="applier-item">
    <h3>{{ applier.user.username }}</h3>
    <p>{{ applier.user.userprofile.introduction }}</p>
    <p><strong>联系方式：</strong>{{ applier.user.email }}</p>
    <p><strong>审核状态：</strong>{{ status_text }}</p>
    <div v-if="applier.status=='finish'">
      <button class="finish">{{ button_text_qualify }}</button>
    </div>
    <div v-else>
      <button @click="qualified(applier)">{{ button_text_qualify }}</button>
    </div>
  </div>
</template>

<script>
import { postQualify } from './api/api';
export default {
  name: 'Applier',
  props: {
    applier: {
      type: Object,
      required: true
    },
    id : ''
  },
  data() {
    return {
      status_text:'',
    }
  },
  created() {
    if(this.applier.status=='finish') {
      this.status_text='已完成';
      this.button_text_qualify='已完成';
    }

    if(this.applier.status=='to-qualify-user') {
      this.status_text='待审核';
      this.button_text_qualify='资质审核通过';
    }

    if(this.applier.status=='to-check-result') {
      this.status_text='待完成';
      this.button_text_qualify='成果审核通过';
    }

  },
  methods: {
    qualified(applier)
    {
      const access=JSON.parse(localStorage.getItem('access'));
      postQualify(access, this.id, applier.user.username)
        .catch(error => {
          console.error('Error qualify', error.response.data.detail);
        });
        location.reload();
    }
  }
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
button {
  padding: 10px 20px;
  background-color: #94070a;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button.finish {
  cursor: default;
}
</style>
