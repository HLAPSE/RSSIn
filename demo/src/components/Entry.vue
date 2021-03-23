<template>
  <el-row>
    <el-col :span="16" :offset="0">
      <el-link :underline="false" :href="state.feed_info.link" target="_blank">
        <h2>{{ state.feed_info.title }}</h2>
      </el-link>
      <h5>{{ state.feed_info.sub_title }}</h5>
    </el-col>
    <el-col :span="8" :offset="0">
      <el-select
        v-model="state.value"
        placeholder="Move To ..."
        @change="changeFold"
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
      <el-button icon="el-icon-search" circle></el-button>
    </el-col>
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
              state.display[index] ? "收起" : "展开"
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
import { getCurrentInstance, watch, reactive, h } from "vue";
import { ElMessage } from "element-plus";

export default {
  props: {
    selectFeed: {
      required: true,
    },
  },
  setup(props, context) {
    const { ctx } = getCurrentInstance();
    const state = reactive({
      feed_info: {},
      lists: [],
      options: [],
      // 获取文件夹选项
      value: "",
    });
    watch(
      () => props.selectFeed.feed_id,
      (newFeedId) => {
        getEntries(newFeedId, props.selectFeed.folder_id);
      }
    );
    // 渲染选择文件夹
    watch(
      () => props.selectFeed.folder_id,
      (folder_id) => {
        state.options = [];
        ctx.$axios
          .get("/api/subscriptions")
          .then((res) => {
            for (let folder of res.data.data) {
              let option = { value: folder.folder_id, label: folder.folder };
              if (folder.folder_id == folder_id) {
                option = {
                  value: folder.folder_id,
                  label: folder.folder,
                  disabled: true,
                };
              }
              state.options.push(option);
            }
          })
          .catch((error) => {
            ElMessage.error(error.message);
          });
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
          ElMessage.error(error.message);
        });
      ctx.$axios
        .get("/api/infos", {
          params: { type: "feed", id: props.selectFeed.feed_id },
        })
        .then((res) => {
          state.feed_info = res.data;
        })
        .catch((error) => {
          ElMessage.error(error.message);
          // ctx.$notify({
          //   title: "Failed to get data",
          //   message: h("i", { style: "color: teal" }, error.message),
          // });
        });
    };
    const changeFold = () => {
      console.log("folder_id", state.value, "id", props.selectFeed.feed_id);
    };
    return { state, changeFold };
  },
};
</script>
<style scoped>
</style>