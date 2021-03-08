<template>
  <el-form
    ref="RegisterForm"
    :model="RegisterInfo"
    :rules="rules"
    label-width="100px"
    class="sign-up-form"
  >
    <el-form-item label="name" prop="name">
      <el-input
        v-model="RegisterInfo.name"
        placeholder="Enter your name"
      ></el-input>
    </el-form-item>
    <el-form-item label="Email" prop="email">
      <el-input
        v-model="RegisterInfo.email"
        type="email"
        placeholder="Enter your email"
      ></el-input>
    </el-form-item>
    <el-form-item label="Password" prop="password">
      <el-input
        v-model="RegisterInfo.password"
        type="password"
        placeholder="Enter your passward"
      ></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitRegisterForm('RegisterForm')"
        >SignUp</el-button
      >
    </el-form-item>
  </el-form>
</template>
<script>
import { getCurrentInstance } from "vue";

export default {
  props: {
    RegisterInfo: {
      required: true,
    },
    rules: {
      required: true,
    },
  },
  setup() {
    const { ctx } = getCurrentInstance();
    const submitRegisterForm = (formName) => {
      ctx.$refs[formName].validate((valid) => {
        if (valid) {
          alert("submit!");
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    };
    return { submitRegisterForm };
  },
};
</script>
