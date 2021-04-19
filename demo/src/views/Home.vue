<template>
  <el-container>
    <el-header>
      <Menu />
    </el-header>
    <el-container>
      <el-aside>
        <!-- 这里是订阅文件夹 -->
        <AsiderForm @feedInfo="feedInfoFun" />
      </el-aside>
      <el-main>
        <Entry :selectFeed="selectFeed" />
      </el-main>
    </el-container>
  </el-container>
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
</style>