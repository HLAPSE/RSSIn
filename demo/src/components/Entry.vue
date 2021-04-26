<template>
  <el-row>
    <el-col :span="16" :offset="0">
      <el-link :underline="false" :href="state.feed_info.link" target="_blank">
        <h1 id="feed-title">{{ state.feed_info.title }}</h1>
      </el-link>
      <el-popover
        placement="top"
        :width="160"
        v-model:visible="state.visible"
        v-if="state.feed_id"
      >
        <el-input
          size="mini"
          placeholder="Enter another alias"
          v-model="state.alias"
          clearable
        >
        </el-input>
        <div style="text-align: right; margin: 0">
          <el-button size="mini" type="text" @click="state.visible = false"
            >cancel</el-button
          >
          <el-button type="primary" size="mini" @click="changeAlias"
            >confirm</el-button
          >
        </div>
        <template #reference>
          <el-button
            type="text"
            icon="el-icon-edit"
            circle
            @click="
              state.visible = true;
              state.alias = '';
            "
          ></el-button>
        </template>
      </el-popover>
      <h6 id="feed-subtitle">{{ state.feed_info.sub_title }}</h6>
    </el-col>
    <el-col :span="8" :offset="0" class="option">
      <el-select
        v-model="state.value"
        placeholder="Move To ..."
        @change="changeFold"
        v-show="state.feed_info.id > 0"
        size="mini"
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
      <el-col :span="18" :offset="0"
        ><el-input
          v-model="state.search"
          size="mini"
          placeholder="输入关键字搜索"
          v-if="selectFeed.folder_id"
        />
      </el-col>
    </el-col>
  </el-row>
  <br />
  <template
    v-for="(entry, index) in state.lists.filter(
      (data) =>
        !state.search ||
        data.title.toLowerCase().includes(state.search.toLowerCase())
    )"
    :key="entry.id"
  >
    <el-card class="box-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-row>
            <el-col :span="15">
              <el-link
                type="info"
                :href="entry.link"
                target="_blank"
                :underline="false"
                ><h3 class="entry-title" :class="{ read: entry.read }">
                  {{ entry.title }}
                </h3>
              </el-link>
              <div>
                <span class="updateddate">{{ entry.updateddate }}</span>
              </div>
            </el-col>
            <el-col :span="9" :offset="15">
              <el-button
                type="primary"
                icon="el-icon-edit"
                circle
                @click="state.noteinput[index] = !state.noteinput[index]"
              ></el-button>
              <el-button
                type="warning"
                icon="el-icon-star-off"
                circle
              ></el-button>
              <el-button @click="readEntry(index, entry.read, entry.id)">{{
                state.display[index] ? "收起" : "展开"
              }}</el-button>
            </el-col>
          </el-row>
        </div>
        <div v-if="state.noteinput[index]">
          <el-row>
            <el-col :span="15">
              <el-input
                type="textarea"
                placeholder="Enter something"
                :autosize="{ minRows: 2, maxRows: 4 }"
                v-model="state.note[index]"
              ></el-input>
            </el-col>
          </el-row>
          <el-row>
            <el-col :offset="9">
              <el-select v-model="state.notefoldid" placeholder="请选择">
                <el-option
                  v-for="item in state.notefolders"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                >
                </el-option>
              </el-select>
              <el-button type="primary" @click="addNote(entry.id, index)"
                >确定</el-button
              >
            </el-col>
          </el-row>
        </div>
      </template>
      <div
        v-if="state.display[index]"
        @mouseup="handleMouseSelect"
        v-html="entry.content"
      ></div>
    </el-card>
    <br />
  </template>
  <!-- 回到顶部 -->
  <el-empty description="RSSIn" v-if="selectFeed.folder_id < 1"></el-empty>
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
      // 编辑订阅名称
      visible: false,
      alias: "",
      note_fold: [],
      notefoldid: "",
      search: "",
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
        ctx.$axios
          .get("/api/notefolders")
          .then((res) => {
            state.notefolders = res.data.data;
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
          state.note = Array.apply(null, Array(state.lists.length)).map(
            () => ""
          );
          state.noteinput = Array.apply(null, Array(state.lists.length)).map(
            () => false
          );
        })
        .catch((error) => {
          ElMessage.error(error.message);
        });
      ctx.$axios
        .get("/api/infos", {
          params: {
            type: "feed",
            id: props.selectFeed.feed_id,
            folder_id: props.selectFeed.folder_id,
          },
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
      ctx.$axios
        .put("/api/subscriptions", {
          folder_id: props.selectFeed.folder_id,
          folder_id_dst: state.value,
          feed_id: props.selectFeed.feed_id,
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
    const changeAlias = () => {
      state.visible = false;
      ctx.$axios
        .put("/api/subscriptions", {
          folder_id: props.selectFeed.folder_id,
          feed_alias: state.alias,
          feed_id: props.selectFeed.feed_id,
        })
        .then((res) => {
          state.feed_info.title = state.alias;
          ElMessage.success({
            message: res.data.message,
            type: "success",
          });
        })
        .catch((error) => {
          ElMessage.error(error.message);
        });
    };
    const addrecord = (info) => {
      if (state.display[info.index]) {
        ctx.$axios
          .post("/api/entries", {
            entry_id: info.id,
          })
          .catch((error) => {
            ElMessage.error(error.message);
          });
      }
    };
    const readEntry = (index, read, id) => {
      state.display[index] = !state.display[index];
      if (state.display[index] && !read) {
        setTimeout(addrecord, 3000, { index: index, id: id });
      }
    };
    // 这里获取选中文本，以后可能就不用这个功能了
    const handleMouseSelect = () => {
      let text = window.getSelection().toString();
      if (text != "") {
        console.log(text);
      }
    };
    const addNote = (entry_id, index) => {
      ctx.$axios
        .post("/api/notes", {
          content: state.note[index],
          notefolder_id: state.notefoldid,
          entry_id: entry_id,
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
      changeFold,
      changeAlias,
      readEntry,
      handleMouseSelect,
      addNote,
    };
  },
};
</script>
<style scoped>
#feed-title {
  color: #66b1ff;
}
#feed-subtitle {
  color: #909399;
}
.option {
  margin-top: 30px;
}
.box-card {
  margin-left: 20px;
  width: 70%;
}
.card-header {
  background-color: #fff;
}
.entry-title {
  color: black;
}
.read {
  color: #888;
}
.updateddate {
  color: #909399;
  font-size: Small;
}
</style>