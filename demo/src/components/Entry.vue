<template>
  <el-row>
    <el-col :span="12" :offset="0"><h3>标题</h3></el-col>
  </el-row>
  <el-row :gutter="20">
    <el-col :span="12" :offset="0"
      ><el-button icon="el-icon-search" circle></el-button
    ></el-col>
    <el-col :span="12" :offset="0"></el-col>
  </el-row>
  <template v-for="(entry, index) in state.lists" :key="entry.id">
    <el-card class="box-card">
      <div class="card-header">
        <el-link
          type="info"
          :href="entry.link"
          target="_blank"
          :underline="false"
          ><h3>{{ entry.title }}</h3></el-link
        >
        <el-row>
          <el-col :span="6" :offset="18">
            <el-button type="primary" icon="el-icon-edit" circle></el-button>
            <el-button type="success" icon="el-icon-check" circle></el-button>
            <el-button
              type="warning"
              icon="el-icon-star-off"
              circle
            ></el-button>
            <el-button @click="state.display[index] = !state.display[index]">{{
              state.display[index] ? "关闭" : "展开"
            }}</el-button>
          </el-col>
        </el-row>
      </div>
      <div class="text item">
        <li>{{ entry.updateddate }}</li>
      </div>
      <div v-if="state.display[index]">
        <span v-html="entry.content"></span>
      </div>
    </el-card>
  </template>
  <!-- 回到顶部 -->
  <el-empty description="正在加载"></el-empty>
  <el-backtop></el-backtop>
</template>

<script>
// import {} from "@vue/composition-api";
import { getCurrentInstance, watch, reactive } from "vue";
import { ElMessage } from "element-plus";

export default {
  props: {
    selectFeed: {
      required: true,
    },
  },
  setup(props, context) {
    const { ctx } = getCurrentInstance();
    let state = reactive({});
    watch(
      () => props.selectFeed.feed_id,
      (newFeedId) => {
        getEntries(newFeedId, props.selectFeed.folder_id);
      }
    );
    const getEntries = (newFeedId, foldId) => {
      ctx.$axios
        .get("/api/entries", {
          params: { feed_id: newFeedId, folder_id: foldId },
        })
        .then((res) => {
          state.lists = res.data.data;
          // 创建数组用于展示与隐藏
          state.display = Array.apply(null, Array(state.lists.length)).map(
            () => false
          );
        })
        .catch((error) => {
          ElMessage.error(error);
        });
    };
    return { state };
  },
};
</script>
<style scoped>
</style>