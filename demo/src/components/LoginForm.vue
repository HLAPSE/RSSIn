<template>
  <el-form
    ref="LoginForm"
    :model="userInfo"
    :rules="rules"
    label-width="100px"
    class="sign-in-form"
  >
    <el-form-item label="邮箱" prop="email">
      <el-input
        v-model="userInfo.email"
        type="email"
        placeholder="输入邮箱登录···"
      ></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="password">
      <el-input
        v-model="userInfo.password"
        type="password"
        placeholder="输入密码···"
      ></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm">登录</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { getCurrentInstance, ref } from "vue";
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
    const LoginForm = ref();
    const submitForm = () => {
      LoginForm.value.validate((valid) => {
        if (valid) {
          console.log("dgffdsg");
          ctx.$axios
            .post("/api/login", props.userInfo)
            .then((res) => {
              const { access_token } = res.data;
              localStorage.setItem("Token", "Bearer " + access_token);
              ctx.$router.push("/");
            })
            .catch((error) => {
              ElMessage.error(error.response);
            });
        } else {
          return false;
        }
      });
    };
    return { submitForm, LoginForm };
  },
};
</script>

<style scoped>
</style>