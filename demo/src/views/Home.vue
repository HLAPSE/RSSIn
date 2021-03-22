<template>
  <el-container>
    <el-header>
      <el-menu mode="horizontal">
        <el-row type="flex">
          <el-col :span="2"><el-menu-item>RSSIn</el-menu-item></el-col>
          <el-col :span="3" :offset="7">
            <el-menu-item icon="el-icon-reading">
              <i class="el-icon-reading">Reading</i>
            </el-menu-item>
          </el-col>
          <el-col :span="3" :offset="1"
            ><el-menu-item
              ><i class="el-icon-collection">Notebook</i></el-menu-item
            ></el-col
          >
          <el-col :span="2" :offset="6">
            <el-menu-item>
              <!-- <el-avatar icon="el-icon-user-solid"></el-avatar> -->
              Hello! 乌拉乌
            </el-menu-item>
          </el-col>
        </el-row>
      </el-menu>
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
export default {
  name: "Home",
  components: { AsiderForm, Entry },
  setup() {
    const isCollapse = false;
    const selectFeed = reactive({ folder_id: 0, feed_id: 1 });
    const feedInfoFun = (selectInfo) => {
      selectFeed.folder_id = selectInfo.folder_id;
      selectFeed.feed_id = selectInfo.feed_id;
    };
    return { isCollapse, feedInfoFun, selectFeed };
  },
};
</script>
<style scoped>
</style>