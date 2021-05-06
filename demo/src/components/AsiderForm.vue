<template>
  <el-scrollbar
    ><el-menu @select="handleSelect">
      <!-- 这里是总的和未读 -->
      <el-submenu index="0">
        <template #title>
          <span>🏠 ALL</span>
        </template>
        <el-menu-item index="0-1">All</el-menu-item>
        <el-menu-item index="0-2">Unread</el-menu-item>
      </el-submenu>
      <!-- 这里开始是各个文件夹 -->
      <template v-for="folder in state.folders" :key="folder.folder_id">
        <el-submenu :index="String(folder.folder_id)">
          <!-- 文件夹标题 -->
          <template #title>
            <span>{{ folder.folder }}</span>
          </template>
          <!-- 文件夹订阅 -->
          <template v-for="feed in folder.folder_list" :key="feed.feed_id">
            <el-menu-item
              :index="String(folder.folder_id) + String(feed.feed_id)"
            >
              <el-row :gutter="20">
                <el-col :span="20">{{ feed.title }}</el-col>
                <!-- 这里用于获取未读文章的个数 -->
                <el-col :span="2">{{ feed.conut }}</el-col>
              </el-row></el-menu-item
            >
          </template>
        </el-submenu>
      </template>
      <el-submenu index="-3">
        <template #title>
          <span>🎁 推荐</span>
        </template>
        <template v-for="feed in state.recommendations" :key="feed.feed_id">
          <el-menu-item :index="'-3' + String(feed.feed_id)">
            <el-row :gutter="20">
              <el-col :span="20">{{ feed.title }}</el-col>
              <!-- 这里用于获取未读文章的个数 -->
              <el-col :span="2">{{ feed.conut }}</el-col>
            </el-row></el-menu-item
          >
        </template>
      </el-submenu>
      <!-- 管理页面按钮 -->
    </el-menu>
    <el-affix position="bottom" :offset="20">
      <el-button
        type="primary"
        icon="el-icon-folder"
        circle
        @click="state.centerDialogVisible = !state.centerDialogVisible"
      ></el-button>
    </el-affix>
    <el-dialog
      title="管理订阅分组"
      v-model="state.centerDialogVisible"
      width="50%"
      center
    >
      <div>
        <el-table
          :data="
            state.folders.filter(
              (data) =>
                !state.search ||
                data.folder.toLowerCase().includes(state.search.toLowerCase())
            )
          "
          style="width: 100%"
        >
          <el-table-column label="分组" prop="folder"> </el-table-column>
          <el-table-column label="数量" prop="folder_list.length">
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
                >编辑</el-button
              >
              <el-button
                size="mini"
                type="danger"
                @click="handleDelete(scope.$index, scope.row)"
                >删除</el-button
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
          <el-button type="primary" @click="state.centerDialogVisible = false"
            >确 定</el-button
          >
        </span>
      </template>
    </el-dialog></el-scrollbar
  >
</template>
<script>
import { getCurrentInstance, defineComponent } from "vue";
import { reactive, onBeforeMount } from "vue";
import { ElMessage, ElLoading } from "element-plus";
export default defineComponent({
  name: "AsiderForm",
  props: {},
  setup(props, context) {
    const state = reactive({
      folders: [],
      options: [],
      centerDialogVisible: false,
      search: "",
      recommendations: [],
    });
    const { ctx } = getCurrentInstance();
    const handleSelect = (keyPath, key) => {
      context.emit("feedInfo", {
        folder_id: parseInt(key[0]),
        // 这里将子菜单index做分割，获取订阅的id
        feed_id: parseInt(keyPath.substring(key[0].length)),
      });
    };
    let loading;
    const startLoading = () => {
      const options = {
        lock: true,
        text: "loading...",
        background: "rgba(0,0,0,0.7)",
      };
      loading = ElLoading.service(options);
    };
    const endLoading = () => {
      loading.close();
    };
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
    const addnotefold = (name) => {
      ctx.$axios
        .post("/api/folders", {
          folder_name: name,
        })
        .then((res) => {
          // 成功之后刷新文件夹
          freshfolder();
          ElMessage.success({
            message: res.data.message,
            type: "success",
          });
        })
        .catch((error) => {
          ElMessage.error(error.message);
        });
    };
    const freshfolder = () => {
      ctx.$axios
        .get("/api/subscriptions")
        .then((res) => {
          state.folders = res.data.data;
          endLoading();
        })
        .catch((error) => {
          ElMessage.error(error.message);
        });
      getrecommendations();
    };
    const handleDelete = (index, row) => {
      if (row.folder_list.length) {
        ElMessage.error("文件夹不为空");
      } else {
        ctx.$axios
          .delete("/api/folders", {
            params: {
              folder_id: row.folder_id,
            },
          })
          .then((res) => {
            ElMessage.success({
              message: res.data.message,
              type: "success",
            });
            freshfolder();
          })
          .catch((error) => {
            ElMessage.error(error.message);
          });
      }
    };
    const handleEdit = (index, row) => {
      ctx
        .$prompt("请输入名称", "", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
        })
        .then(({ value }) => {
          if (value) {
            editfoldname(row, value);
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
    const editfoldname = (row, name) => {
      ctx.$axios
        .put("/api/folders", {
          folder_id: row.folder_id,
          folder_name: name,
        })
        .then((res) => {
          row.folder = name;
          ElMessage.success({
            message: res.data.message,
            type: "success",
          });
        })
        .catch((error) => {
          ElMessage.error(error.message);
        });
    };
    const getrecommendations = () => {
      ctx.$axios
        .get("/api/recommendations")
        .then((res) => {
          state.recommendations = res.data;
        })
        .catch((error) => {
          ElMessage.error(error.message);
        });
    };
    startLoading();
    freshfolder();
    return {
      state,
      handleSelect,
      addfolderopen,
      handleDelete,
      handleEdit,
      freshfolder,
    };
  },
});
</script>

<style scoped>
.el-menu {
  background-color: #f6f7f8;
  height: 95vh;
}
.el-menu-item {
  background-color: #f6f7f8;
}
.el-affix {
  background-color: #f6f7f8;
}
</style>