<template>
  <div class="launch-project">
		<h1>{{ banner }}</h1>
		<p><strong>当前资产：</strong>{{ point_amount }} 摆币</p>
      <form @submit.prevent="pay">
        <div class="form-group">
          <p><strong>充值金额</strong>(1 元=100 摆币)</p>
          <input type="number" id="number" v-model="pay_amount" required />
        </div>
        <button type="submit">充值</button>
      </form>
    </div>
</template>
  
<script>
export default {
  name: 'Charge',
  data() {
    return {
      point_amount:'0',
      banner:'充值',
			pay_amount:'',
    };
  },
	methods: {
		pay() {

		}
	}
};
</script>
  
<style scoped>
  .launch-project {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
    color: #94070a;
  }
  .form-group {
    margin-bottom: 15px;
  }
  label {
    display: block;
    margin-bottom: 5px;
  }
  input, textarea {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
  }
  button {
  width: 100%;
  padding: 10px;
  background-color: #94070a;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  }
  button:hover {
    background-color: #0056b3;
  }
</style>
  