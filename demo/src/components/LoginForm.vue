<template>
  <el-form
    ref="LoginForm"
    :model="userInfo"
    :rules="rules"
    label-width="100px"
    class="sign-in-form"
  >
    <el-form-item label="Email" prop="email">
      <el-input
        v-model="userInfo.email"
        type="email"
        placeholder="Enter your email"
      ></el-input>
    </el-form-item>
    <el-form-item label="Password" prop="password">
      <el-input
        v-model="userInfo.password"
        type="password"
        placeholder="Enter your passward"
      ></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('LoginForm')"
        >Login</el-button
      >
    </el-form-item>
  </el-form>
</template>

<script>
import { ref, getCurrentInstance } from "vue";

export default {
  props: {
    userInfo: {
      required: true,
    },
    rules: {
      required: true,
    },
  },
  setup() {
    const { ctx } = getCurrentInstance();
    const submitForm = (formName) => {
      ctx.$refs[formName].validate((valid) => {
        if (valid) {
          alert("submit!");
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    };
    return { submitForm };
  },
};
</script>

<style scoped>
</style>