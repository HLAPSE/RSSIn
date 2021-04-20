<template>
  <el-row type="flex" align="middle">
    <el-col :span="2">RSSIn</el-col>
    <el-col :span="3" :offset="7">
      <router-link to="/"><i class="el-icon-reading">Reading</i></router-link>
    </el-col>
    <el-col :span="3" :offset="1">
      <router-link to="/note"
        ><i class="el-icon-collection">Notebook</i></router-link
      >
    </el-col>
    <el-col :span="2" :offset="6">
      <el-button type="text" icon="el-icon-user" @click="openinfo">
        Hello!{{ state.user.name }}
      </el-button>
      <el-dialog
        title="用户信息"
        v-model="state.centerDialogVisible"
        width="30%"
        center
      >
        <el-form
          :model="ruleForm"
          status-icon
          label-width="100px"
          class="demo-ruleForm"
        >
          <el-form-item label="name" prop="name">
            <el-input
              v-model="ruleForm.name"
              :placeholder="state.user.name"
            ></el-input>
          </el-form-item>
          <el-form-item label="email" prop="email">
            <el-input
              type="email"
              v-model="ruleForm.email"
              :placeholder="state.user.email"
              :rules="[
                {
                  required: true,
                  message: '请输入邮箱地址',
                  trigger: 'blur',
                },
                {
                  type: 'email',
                  message: '请输入正确的邮箱地址',
                  trigger: ['blur', 'change'],
                },
              ]"
            ></el-input>
          </el-form-item>
          <!-- 密码输入不做了 -->
          <!-- <el-form-item label="passwd" prop="passwd">
              <el-input
                v-model.number="ruleForm.passwd"
                placeholder="Enter the passwd"
              ></el-input>
            </el-form-item> -->
          <el-form-item>
            <span class="dialog-footer">
              <el-button @click="resetForm">取 消</el-button>
              <el-button type="primary" @click="submitForm">确 定</el-button>
            </span></el-form-item
          >
        </el-form>
      </el-dialog>
    </el-col>
  </el-row>
</template>
<script>
import { reactive, getCurrentInstance } from "vue";
import { ElMessage } from "element-plus";
export default {
  setup() {
    const ruleForm = reactive({
      name: "",
      email: "",
    });
    const state = reactive({
      user: {},
      centerDialogVisible: false,
    });
    const { ctx } = getCurrentInstance();
    // 获取用户信息
    ctx.$axios
      .get("/api/users")
      .then((res) => {
        state.user = res.data;
      })
      .catch((error) => {
        ElMessage.error(error.message);
      });
    const submitForm = () => {
      if ((ruleForm.name == "") | ruleForm.email) {
        ElMessage.warning({
          message: "邮箱或用户名不可为空!",
          type: "warning",
        });
        return;
      }
      ctx.$axios
        .put("/api/users", {
          name: ruleForm.name,
          email: ruleForm.email,
        })
        .then((res) => {
          state.user.name = ruleForm.name;
          state.user.email = ruleForm.email;
          ElMessage.success({
            message: res.data.message,
            type: "success",
          });
        })
        .catch((error) => {
          ElMessage.error(error.message);
        });
      state.centerDialogVisible = false;
    };
    const resetForm = () => {
      state.centerDialogVisible = false;
    };
    const openinfo = () => {
      ruleForm.name = "";
      ruleForm.email = "";
      state.centerDialogVisible = true;
    };
    return { state, ruleForm, submitForm, resetForm, openinfo };
  },
};
</script>
<style scoped>
</style>


