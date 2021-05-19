<template>
  <el-form
    ref="RegisterForm"
    :model="RegisterInfo"
    :rules="rules"
    label-width="100px"
    class="sign-up-form"
  >
    <el-form-item label="用户名" prop="name">
      <el-input
        v-model="RegisterInfo.name"
        placeholder="输入名称···"
      ></el-input>
    </el-form-item>
    <el-form-item label="邮箱" prop="email">
      <el-input
        v-model="RegisterInfo.email"
        type="email"
        placeholder="输入邮箱"
      ></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="password">
      <el-input
        v-model="RegisterInfo.password"
        type="password"
        placeholder="输入密码···"
      ></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitRegisterForm('RegisterForm')"
        >注册</el-button
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
