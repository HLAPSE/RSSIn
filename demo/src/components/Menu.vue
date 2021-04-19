<template>
  <el-menu mode="horizontal">
    <el-row type="flex">
      <el-col :span="2"><el-menu-item>RSSIn</el-menu-item></el-col>
      <el-col :span="3" :offset="7">
        <el-menu-item>
          <router-link to="/"
            ><i class="el-icon-reading">Reading</i></router-link
          >
        </el-menu-item>
      </el-col>
      <el-col :span="3" :offset="1">
        <el-menu-item>
          <router-link to="/note"
            ><i class="el-icon-collection">Notebook</i></router-link
          >
        </el-menu-item>
      </el-col>
      <el-col :span="2" :offset="6">
        <el-menu-item>
          <!-- <el-avatar icon="el-icon-user-solid"></el-avatar> -->
          Hello!{{ state.user.name }}
        </el-menu-item>
      </el-col>
    </el-row>
  </el-menu>
</template>
<script>
import { reactive, getCurrentInstance } from "vue";
export default {
  setup() {
    const state = reactive({
      user: {},
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
    return { state };
  },
};
</script>
<style scoped>
</style>


