<template>
  <el-scrollbar
    ><el-container>
      <el-header height="5vh">
        <Menu />
      </el-header>
      <el-container>
        <el-aside class="asi">
          <!-- 这里是订阅文件夹 -->
          <AsiderForm ref="RefChilde" @feedInfo="feedInfoFun" />
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
import { reactive, ref, defineComponent } from "vue";
import Menu from "@/components/Menu";
export default defineComponent({
  name: "Home",
  components: { AsiderForm, Entry, Menu },
  setup() {
    const RefChilde = ref();
    const isCollapse = false;
    const selectFeed = reactive({ folder_id: 0, feed_id: -10 });
    // 获取所选的文件夹
    const feedInfoFun = (selectInfo) => {
      selectFeed.folder_id = selectInfo.folder_id;
      selectFeed.feed_id = selectInfo.feed_id;
    };
    const freshAsideFun = () => {
      RefChilde.value.freshfolder();
    };
    return {
      isCollapse,
      feedInfoFun,
      selectFeed,
      RefChilde,
      freshAsideFun,
    };
  },
});
</script>
<style scoped>
.el-container > .el-container {
  height: 94vh;
}
</style>