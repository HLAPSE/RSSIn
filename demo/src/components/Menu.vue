<template>
  <el-row type="flex" align="middle">
    <el-col :span="2">RSSIn</el-col>
    <el-col :span="3" :offset="7">
      <router-link to="/"><i class="el-icon-reading">Reading</i></router-link>
    </el-col>
    <el-col :span="3" :offset="2">
      <router-link to="/note"
        ><i class="el-icon-collection">Notebook</i></router-link
      >
    </el-col>
    <el-col :span="1" :offset="4">
      <el-button
        type="success"
        size="mini"
        icon="el-icon-plus"
        @click="state.dialog = true"
      ></el-button>
      <el-drawer
        title="添加订阅"
        v-model="state.dialog"
        direction="rtl"
        ref="drawer"
        size="50%"
      >
        <div>
          <el-row :gutter="2">
            <el-col :span="16" :offset="1"
              ><el-input
                placeholder="请输入订阅链接···"
                v-model="feedurl"
                clearable
                size="small"
              >
              </el-input
            ></el-col>
            <el-col :span="4" :offset="1">
              <el-button
                type="success"
                @click="getfeed"
                :loading="state.loading"
                round
                size="small"
              >
                {{ state.loading ? "提交中 ..." : "确 定" }}
              </el-button>
            </el-col>
          </el-row>
          <div>
            <el-button @click="cancelForm" size="small">取 消</el-button>
            <el-select
              v-model="state.value"
              placeholder="订阅到···"
              @change="feedadd"
              size="small"
              style="width: 100px"
            >
              <el-option
                v-for="item in state.options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                :disabled="item.disabled"
              >
              </el-option>
            </el-select>
          </div>
        </div>
      </el-drawer>
    </el-col>
    <el-col :span="2" :offset="0">
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
import { reactive, getCurrentInstance, ref } from "vue";
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
      dialog: false,
      loading: false,
      // 用于获取所选择的订阅文件夹以及所选择的值
      options: [],
      value: "",
    });
    const feedurl = ref("");
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
    // 获取订阅文件夹
    ctx.$axios
      .get("/api/subscriptions")
      .then((res) => {
        for (let folder of res.data.data) {
          let option = { value: folder.folder_id, label: folder.folder };
          // if (folder.folder_id == folder_id) {
          //   option = {
          //     value: folder.folder_id,
          //     label: folder.folder,
          //     disabled: true,
          //   };
          // }
          state.options.push(option);
        }
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
    const cancelForm = () => {
      state.loading = false;
      state.dialog = false;
    };
    // 获取订阅信息及文章
    const getfeed = () => {
      if (feedurl.value != "") {
        console.log(feedurl.value);
      } else {
        ElMessage.warning({
          message: "订阅链接不可为空!",
          type: "warning",
        });
      }
    };
    // 点击订阅按钮添加订阅
    const feedadd = () => {
      state.loading = false;
      state.dialog = false;
      console.log(state.value, feedurl.value);
    };
    return {
      state,
      ruleForm,
      submitForm,
      resetForm,
      openinfo,
      cancelForm,
      feedurl,
      getfeed,
      feedadd,
    };
  },
};
</script>
<style scoped>
</style>


