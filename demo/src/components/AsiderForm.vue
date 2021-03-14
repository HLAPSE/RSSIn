<template>
  <el-menu>
    <!-- 这里是总的和未读 -->
    <el-submenu index="0">
      <template #title>
        <i class="el-icon-house"></i>
        <span>ALL</span>
      </template>
      <el-menu-item index="1-1">All</el-menu-item>
      <el-menu-item index="1-2">Unread</el-menu-item>
    </el-submenu>
    <!-- 这里开始是各个文件夹 -->
    <template v-for="folder in state.folders" :key="folder.folder_id">
      <el-submenu :index="String(folder.folder_id)">
        <!-- 文件夹标题 -->
        <template #title>
          <i class="el-icon-folder"></i>
          <span>{{ folder.folder }}</span>
        </template>
        <!-- 文件夹订阅 -->
        <template v-for="feed in folder.folder_list" :key="feed.feed_id">
          <el-menu-item :index="feed.feed_id">{{ feed.title }}</el-menu-item>
        </template>
      </el-submenu>
    </template>
    <el-submenu index="-1">
      <template #title>
        <i class="el-icon-s-opportunity"></i>
        <span>推荐</span>
      </template>
      <el-menu-item index="0-1"
        >假装这有个推荐1 <i class="el-icon-circle-plus-outline"></i
      ></el-menu-item>
      <el-menu-item index="0-2"
        >再来一个推荐2<i class="el-icon-circle-plus-outline"></i
      ></el-menu-item>
      <el-menu-item index="0-0"
        >点这里关闭推荐<i class="el-icon-delete-solid"></i
      ></el-menu-item>
    </el-submenu>
  </el-menu>
</template>
<script>
import { getCurrentInstance } from "vue";
import { reactive } from "vue";
import { ElMessage } from "element-plus";
export default {
  props: {},
  setup(props) {
    const state = reactive({
      folders: [],
    });
    const { ctx } = getCurrentInstance();
    ctx.$axios
      .get("/api/subscriptions")
      .then((res) => {
        state.folders = res.data.data;
      })
      .catch((error) => {
        ElMessage.error(error);
      });
    return { state };
  },
};
</script>

<style scoped>
</style>