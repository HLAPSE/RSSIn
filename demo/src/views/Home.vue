<template>
  <el-scrollbar
    ><el-container>
      <el-header height="40px">
        <Menu />
      </el-header>
      <el-container>
        <el-aside class="asi">
          <!-- 这里是订阅文件夹 -->
          <el-scrollbar><AsiderForm @feedInfo="feedInfoFun" /></el-scrollbar>
        </el-aside>
        <el-main>
          <el-scrollbar><Entry :selectFeed="selectFeed" /></el-scrollbar>
        </el-main>
      </el-container> </el-container
  ></el-scrollbar>
</template>

<script>
// @ is an alias to /src
import AsiderForm from "@/components/AsiderForm";
import Entry from "@/components/Entry";
import { reactive } from "vue";
import Menu from "@/components/Menu";
export default {
  name: "Home",
  components: { AsiderForm, Entry, Menu },
  setup() {
    const state = reactive({});
    const isCollapse = false;
    const selectFeed = reactive({ folder_id: 0, feed_id: -10 });
    // 获取所选的文件夹
    const feedInfoFun = (selectInfo) => {
      selectFeed.folder_id = selectInfo.folder_id;
      selectFeed.feed_id = selectInfo.feed_id;
    };
    return { isCollapse, feedInfoFun, selectFeed, state };
  },
};
</script>
<style scoped>
.el-container > .el-container {
  height: 100vh;
}
.el-header {
  background-color: #f6f7f8;
}
.el-aside {
  height: 100vh;
  background-color: #f6f7f8;
}
</style>