<template>
  <el-scrollbar>
    <el-container>
      <el-header height="40px">
        <Menu />
      </el-header>
      <el-container>
        <el-aside>
          <!-- 这里是订阅文件夹 -->
          <el-scrollbar>
            <el-menu>
              <template
                v-for="folder in state.notefolders"
                :key="folder.folder_id"
              >
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
                  <el-row :gutter="20">
                    <el-col :span="20">{{ folder.folder }}</el-col>
                    <el-col :span="4">{{ folder.folder_list.length }}</el-col>
                  </el-row>
                </el-menu-item>
              </template>
              <el-affix position="bottom" :offset="20">
                <el-button
                  type="primary"
                  icon="el-icon-s-tools"
                  circle
                  @click="
                    state.centerDialogVisible = !state.centerDialogVisible
                  "
                ></el-button>
              </el-affix>
              <!-- 笔记管理 -->
              <el-dialog
                title="管理笔记文件夹"
                v-model="state.centerDialogVisible"
                width="50%"
                center
              >
                <div>
                  <el-table
                    :data="
                      state.notefolder.filter(
                        (data) =>
                          !state.search ||
                          data.name
                            .toLowerCase()
                            .includes(state.search.toLowerCase())
                      )
                    "
                    style="width: 100%"
                  >
                    <el-table-column label="Name" prop="name">
                    </el-table-column>
                    <el-table-column label="Conut" prop="note_count">
                    </el-table-column>
                    <el-table-column align="right">
                      <template #header>
                        <el-row>
                          <el-col :span="18" :offset="0"
                            ><el-input
                              v-model="state.search"
                              size="mini"
                              placeholder="输入关键字搜索"
                            />
                          </el-col>
                          <el-col :span="6" :offset="0"
                            ><el-button
                              size="mini"
                              round
                              type="primary"
                              icon="el-icon-folder-add"
                              @click="addfolderopen"
                            ></el-button
                          ></el-col>
                        </el-row>
                      </template>
                      <template #default="scope">
                        <el-button
                          size="mini"
                          @click="handleEdit(scope.$index, scope.row)"
                          >Edit</el-button
                        >
                        <el-button
                          size="mini"
                          type="danger"
                          @click="handleDelete(scope.$index, scope.row)"
                          >Delete</el-button
                        >
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
                <template #footer>
                  <span class="dialog-footer">
                    <el-button @click="state.centerDialogVisible = false"
                      >取 消</el-button
                    >
                    <el-button
                      type="primary"
                      @click="state.centerDialogVisible = false"
                      >确 定</el-button
                    >
                  </span>
                </template>
              </el-dialog>
            </el-menu></el-scrollbar
          >
        </el-aside>
        <el-main>
          <!-- 这里是笔记 -->
          <el-row>
            <el-col :span="12" :offset="2"
              ><h1>{{ state.currentfoldername }}</h1></el-col
            >
          </el-row>
          <template v-for="item in state.currentlist" :key="item.note_id">
            <el-card class="box-card">
              <template #header>
                <div class="card-header">
                  <el-row :gutter="20">
                    <el-col :span="18" :offset="0"
                      ><el-link
                        type="primary"
                        :href="item.entry_info.link"
                        target="_blank"
                        :underline="false"
                        >{{ item.entry_info.title }}</el-link
                      ></el-col
                    >
                    <el-col :span="6" :offset="0"
                      ><el-dropdown trigger="click" @command="handleCommand">
                        <span class="el-dropdown-link">
                          更改文件夹<i
                            class="el-icon-arrow-down el-icon--right"
                          ></i>
                        </span>
                        <template #dropdown>
                          <el-dropdown-menu
                            v-for="folder in state.notefolder"
                            :key="folder.id"
                          >
                            <el-dropdown-item
                              v-if="folder.id != state.currentfolder"
                              :command="String(folder.id + ' ' + item.note_id)"
                            >
                              {{ folder.name }}
                            </el-dropdown-item>
                            <el-dropdown-item
                              v-else
                              disabled
                              :command="String(folder.id + ' ' + item.note_id)"
                            >
                              {{ folder.name }}
                            </el-dropdown-item>
                          </el-dropdown-menu>
                        </template>
                      </el-dropdown>
                      <el-button-group class="btngroup"
                        ><el-button
                          type="primary"
                          icon="el-icon-edit"
                          @click="opendialog(item.content, item)"
                          size="small"
                        ></el-button>
                        <el-button
                          type="danger"
                          icon="el-icon-delete"
                          @click="deletenote(item.note_id)"
                          size="small"
                        ></el-button></el-button-group
                    ></el-col>
                  </el-row>
                </div>
              </template>
              {{ item.content }}
            </el-card>
          </template>
          <el-empty
            description="RSSIn"
            v-if="state.currentlist.length == 0"
          ></el-empty>
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
  </el-scrollbar>
</template>
<script>
import { reactive, getCurrentInstance } from "vue";
import { ElMessage } from "element-plus";
import Menu from "@/components/Menu";
export default {
  components: { Menu },
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
      // 这里放笔记文件夹
      notefolder: [],
      // 笔记管理显示
      centerDialogVisible: false,
      search: "",
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
    // 用来获取笔记
    ctx.$axios
      .get("/api/notes")
      .then((res) => {
        state.notefolders = res.data.data;
      })
      .catch((error) => {
        ElMessage.error(error.message);
      });
    // 用来获取笔记文件夹
    const handleSelect = (key, lists, name) => {
      state.currentfolder = parseInt(key);
      state.currentlist = lists;
      state.currentfoldername = name;
    };
    const freshnotefolder = () => {
      ctx.$axios
        .get("/api/notefolders")
        .then((res) => {
          state.notefolder = res.data.data;
        })
        .catch((error) => {
          ElMessage.error(error.message);
        });
    };
    freshnotefolder();
    const deletenote = (id) => {
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
    const handleCommand = (command) => {
      let folder_id = parseInt(command.split(" ")[0]);
      let note_id = parseInt(command.split(" ")[1]);
      ctx.$axios
        .put("/api/notes", {
          note_id: note_id,
          content: state.currentnote,
          notefolder_id_dst: folder_id,
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
    // 用来删除与编辑文件夹
    const handleEdit = (index, row) => {
      ctx
        .$prompt("请输入名称", "", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
        })
        .then(({ value }) => {
          if (value) {
            editnotefoldname(row, value);
          } else {
            ctx.$message({
              type: "info",
              message: "不能为空",
            });
          }
        })
        .catch(() => {
          ctx.$message({
            type: "info",
            message: "取消输入",
          });
        });
    };
    const handleDelete = (index, row) => {
      if (row.note_count) {
        ElMessage.error("文件夹不为空");
      } else {
        ctx.$axios
          .delete("/api/notefolders", {
            params: {
              notefolder_id: row.id,
            },
          })
          .then((res) => {
            delete state.notefolder[index];
            ElMessage.success({
              message: res.data.message,
              type: "success",
            });
          })
          .catch((error) => {
            ElMessage.error(error.message);
          });
      }
    };
    // 提交修改笔记文件夹
    const editnotefoldname = (row, name) => {
      ctx.$axios
        .put("/api/notefolders", {
          notefolder_id: row.id,
          notefolder_name: name,
        })
        .then((res) => {
          row.name = name;
          ElMessage.success({
            message: res.data.message,
            type: "success",
          });
        })
        .catch((error) => {
          ElMessage.error(error.message);
        });
    };
    // 这里是添加文件夹的两个方法，和上两个一样
    // 打开添加文件夹提示框
    const addfolderopen = () => {
      ctx
        .$prompt("请输入名称", "", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
        })
        .then(({ value }) => {
          if (value) {
            addnotefold(value);
          } else {
            ctx.$message({
              type: "info",
              message: "不能为空",
            });
          }
        })
        .catch(() => {
          ctx.$message({
            type: "info",
            message: "取消输入",
          });
        });
    };
    // 提交添加笔记文件夹
    const addnotefold = (name) => {
      ctx.$axios
        .post("/api/notefolders", {
          notefolder_name: name,
        })
        .then((res) => {
          // 成功之后刷新文件夹
          freshnotefolder();
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
      handleCommand,
      handleEdit,
      handleDelete,
      open,
      addfolderopen,
    };
  },
};
</script>
<style scoped>
.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.box-card {
  margin: 20px auto;
  width: 75%;
}
/* 下拉菜单样式 */
.el-dropdown-link {
  cursor: pointer;
  color: #409eff;
}
.el-icon-arrow-down {
  font-size: 12px;
}
.demonstration {
  display: block;
  color: #8492a6;
  font-size: 14px;
  margin-bottom: 20px;
}
.el-header {
  background-color: #f6f7f8;
}
.el-menu {
  height: 100vh;
  background-color: #f6f7f8;
}
.el-menu-item {
  background-color: #f6f7f8;
}
.btngroup {
  margin: auto;
}
</style>