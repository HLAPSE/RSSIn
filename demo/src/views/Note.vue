<template>
  <el-container>
    <el-header>
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
    </el-header>
    <el-container>
      <el-aside>
        <!-- 这里是订阅文件夹 -->
        <el-menu>
          <template v-for="folder in state.notefolders" :key="folder.folder_id">
            <el-menu-item
              :index="String(folder.folder_id)"
              @click="
                handleSelect(
                  folder.folder_id,
                  folder.folder_list,
                  folder.folder
                )
              "
            >
              {{ folder.folder }}
            </el-menu-item>
          </template>
        </el-menu>
      </el-aside>
      <el-main>
        <!-- 这里是笔记 -->
        {{ state.currentfoldername }}
        <template v-for="item in state.currentlist" :key="item.note_id">
          <el-divider></el-divider>
          <el-card class="box-card">
            <template #header>
              <div class="card-header">
                <el-link
                  type="primary"
                  :href="item.entry_info.link"
                  target="_blank"
                  :underline="false"
                  >{{ item.entry_info.title }}</el-link
                >
                <div>
                  <el-button
                    type="primary"
                    icon="el-icon-edit"
                    circle
                    @click="opendialog(item.content, item)"
                  ></el-button>
                  <el-button
                    type="danger"
                    icon="el-icon-delete"
                    circle
                    @click="deletenote(item.note_id)"
                  ></el-button>
                </div>
              </div>
            </template>
            {{ item.content }}
          </el-card>
        </template>
      </el-main>
    </el-container>
  </el-container>
  <!-- 用来修改笔记的弹出框 -->
  <el-dialog
    title="修改笔记"
    v-model="state.dialogVisible"
    width="30%"
    :before-close="handleClose"
  >
    <el-input
      type="textarea"
      :rows="2"
      placeholder="state.currentnote"
      v-model="state.currentnote"
    >
    </el-input>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="state.dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="putnote">确 定</el-button>
      </span>
    </template>
  </el-dialog>
</template>
<script>
import { reactive, getCurrentInstance } from "vue";
import { ElMessage } from "element-plus";
export default {
  setup() {
    const state = reactive({
      user: {},
      currentlist: [],
      currentfolder: 0,
      currentfoldername: "",
      dialogVisible: false,
      currentnote: "",
      // 当前选中的笔记
      item: {},
    });
    const { ctx } = getCurrentInstance();
    ctx.$axios
      .get("/api/users")
      .then((res) => {
        state.user = res.data;
      })
      .catch((error) => {
        ElMessage.error(error.message);
      });
    ctx.$axios
      .get("/api/notes")
      .then((res) => {
        state.notefolders = res.data.data;
      })
      .catch((error) => {
        ElMessage.error(error.message);
      });
    const handleSelect = (key, lists, name) => {
      state.currentfolder = parseInt(key);
      state.currentlist = lists;
      state.currentfoldername = name;
      console.log(state.currentfolder, state.currentlist);
    };
    const deletenote = (id) => {
      console.log(id);
      ctx.$axios
        .delete("/api/notes", {
          params: {
            note_id: id,
          },
        })
        .then((res) => {
          ElMessage.success({
            message: res.data.message,
            type: "success",
          });
        })
        .catch((error) => {
          ElMessage.error(error.message);
        });
    };
    const opendialog = (content, item) => {
      state.currentnote = content;
      state.dialogVisible = true;
      state.item = item;
    };
    const handleClose = () => {
      state.dialogVisible = false;
    };
    const putnote = () => {
      state.item.content = state.currentnote;
      state.dialogVisible = false;
      ctx.$axios
        .put("/api/notes", {
          note_id: state.item.note_id,
          content: state.currentnote,
          notefolder_id_dst: -1,
        })
        .then((res) => {
          ElMessage.success({
            message: res.data.message,
            type: "success",
          });
        })
        .catch((error) => {
          ElMessage.error(error.message);
        });
    };
    return {
      state,
      handleSelect,
      deletenote,
      opendialog,
      handleClose,
      putnote,
    };
  },
};
</script>
<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

/* .box-card {
  width: 480px;
} */
</style>