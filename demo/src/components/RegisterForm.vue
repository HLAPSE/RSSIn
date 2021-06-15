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
import { getCurrentInstance, reactive } from "vue";
import { ElMessage } from "element-plus";
export default {
  props: {
    rules: {
      required: true,
    },
  },
  setup() {
    const { ctx } = getCurrentInstance();
    const RegisterInfo = reactive({
      name: "",
      email: "",
      password: "",
    });
    const register = (name, email, password) => {
      ctx.$axios
        .post("/api/users", {
          name: name,
          email: email,
          password: password,
        })
        .then((res) => {
          const { access_token, message } = res.data;
          ElMessage.success({
            message: message,
            type: "success",
          });
          localStorage.setItem("Token", "Bearer " + access_token);
          ctx.$router.push("/");
        })
        .catch((error) => {
          ElMessage.error(error.response.data.message);
        });
    };
    const submitRegisterForm = (formName) => {
      ctx.$refs[formName].validate((valid) => {
        if (valid) {
          register(
            RegisterInfo.name,
            RegisterInfo.email,
            RegisterInfo.password
          );
        } else {
          console.log("提交错误!!");
          return false;
        }
      });
    };
    return { submitRegisterForm, RegisterInfo };
  },
};
</script>
