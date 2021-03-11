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
import { getCurrentInstance } from "vue";
import { ElMessage } from "element-plus";

export default {
  props: {
    userInfo: {
      required: true,
    },
    rules: {
      required: true,
    },
  },
  setup(props) {
    const { ctx } = getCurrentInstance();
    const submitForm = (formName) => {
      ctx.$refs[formName].validate((valid) => {
        if (valid) {
          ctx.$axios
            .post("/api/login", props.userInfo)
            .then((res) => {
              const { access_token } = res.data;
              localStorage.setItem("Token", "Bearer " + access_token);
              ctx.$router.push("/");
            })
            .catch((error) => {
              ElMessage.error(error.response.data);
            });
        } else {
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