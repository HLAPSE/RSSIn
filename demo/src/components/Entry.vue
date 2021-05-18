<template>
  <el-row>
    <el-col :span="12" :offset="1">
      <el-link :underline="false" :href="state.feed_info.link" target="_blank">
        <h1 id="feed-title">{{ state.feed_info.title }}</h1>
      </el-link>
      <el-popover
        placement="top"
        :width="160"
        v-model:visible="state.visible"
        v-if="selectFeed.folder_id > 0"
      >
        <el-input
          size="mini"
          placeholder="输入别名"
          v-model="state.alias"
          clearable
        >
        </el-input>
        <div style="text-align: right; margin: 0">
          <el-button size="mini" type="text" @click="state.visible = false"
            >取消</el-button
          >
          <el-button type="primary" size="mini" @click="changeAlias"
            >确定</el-button
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
    <el-col :span="4" :offset="1" class="option">
      <el-select
        v-model="state.value"
        :placeholder="state.placeholder"
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
    </el-col>
    <el-col :span="4" :offset="0" class="option"
      ><el-input
        v-model="state.search"
        size="mini"
        placeholder="输入关键字搜索"
        v-if="selectFeed.folder_id"
    /></el-col>
  </el-row>
  <template
    v-for="(entry, index) in state.lists.filter(
      (data) =>
        !state.search ||
        data.title.toLowerCase().includes(state.search.toLowerCase())
    )"
    :key="entry.id"
  >
    <el-card
      class="box-card"
      shadow="hover"
      :class="{
        bilibili: entry.type == 'space.bilibili.com',
        zhihu: entry.type == 'www.zhihu.com',
        bing: entry.type == 'cn.bing.com',
        epic: entry.type == 'www.epicgames.com',
        weibo: entry.type == 'weibo.com',
      }"
    >
      <template #header>
        <el-row :gutter="12">
          <el-col :span="20">
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
          <el-col :span="4" class="btngroup">
            <el-button-group>
              <el-button
                class="edit"
                icon="el-icon-edit"
                @click="state.noteinput[index] = !state.noteinput[index]"
                size="small"
              ></el-button>
              <el-button
                class="goon"
                @click="readEntry(index, entry.read, entry.id, entry)"
                size="small"
                >{{ state.display[index] ? "收起" : "展开" }}</el-button
              >
            </el-button-group>
          </el-col>
        </el-row>
        <div v-show="state.noteinput[index]" class="edit-area">
          <el-row :gutter="20">
            <el-col :span="12" :offset="2">
              <el-input
                type="textarea"
                placeholder="记点东西吧！"
                :autosize="{ minRows: 1, maxRows: 3 }"
                v-model="state.note[index]"
              ></el-input>
            </el-col>
            <el-col :span="9" :offset="1" class="btngroup">
              <el-col :span="15" :offset="0">
                <el-select
                  v-model="state.notefoldid"
                  placeholder="选择笔记分类"
                  size="small"
                >
                  <el-option
                    v-for="item in state.notefolders"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                  >
                  </el-option> </el-select
              ></el-col>
              <el-col :span="9" :offset="0"
                ><el-button
                  type="primary"
                  @click="addNote(entry.id, index)"
                  size="small"
                  >确定</el-button
                ></el-col
              >
            </el-col>
          </el-row>
        </div>
      </template>
      <div
        class="entry-content"
        v-if="state.display[index]"
        @mouseup="handleMouseSelect"
        v-html="entry.content"
      ></div>
    </el-card>
  </template>
  <!-- 回到顶部 -->
  <el-empty
    description="RSSIn"
    v-if="selectFeed.folder_id < 1"
    :image-size="240"
  ></el-empty>
  <el-backtop></el-backtop>
</template>

<script>
// import {} from "@vue/composition-api";
import { getCurrentInstance, watch, reactive, defineComponent } from "vue";
import { ElMessage } from "element-plus";

export default defineComponent({
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
      notefoldid: "",
      search: "",
      placeholder: "",
    });
    watch(
      () => props.selectFeed.feed_id,
      (newFeedId) => {
        getEntries(newFeedId, props.selectFeed.folder_id);
        if (props.selectFeed.folder_id > 0) {
          state.placeholder = "移动到···";
        } else {
          state.placeholder = "订阅到···";
        }
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
    // 调用父组件方法实现侧栏刷新
    const freshfolder = () => {
      context.emit("freshAside");
    };
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
          freshfolder();
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
          .then((res) => {
            info.entry.read = true;
          })
          .catch((error) => {
            ElMessage.error(error.message);
          });
      }
    };
    const readEntry = (index, read, id, entry) => {
      state.display[index] = !state.display[index];
      if (state.display[index] && !read) {
        setTimeout(addrecord, 3000, { index: index, id: id, entry: entry });
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
});
</script>
<style scoped>
#feed-title {
  color: #cc6666;
}
#feed-subtitle {
  color: #909399;
}
.option {
  margin-top: 30px;
}
.box-card {
  margin: 20px auto;
  width: 75%;
}
.box-card /deep/ .el-card__header {
  background-color: #f6f7f899;
}
.bilibili /deep/ .el-card__header {
  background-color: #f1729d10;
}
.zhihu /deep/ .el-card__header {
  background-color: #0064fa10;
}
.weibo /deep/ .el-card__header {
  background-color: #eb735010;
}
.bing /deep/ .el-card__header {
  background-color: #ffc20e10;
}
.epic /deep/ .el-card__header {
  background-color: #00000010;
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
.btngroup {
  margin: auto;
}
.entry-content /deep/ img {
  max-width: 100%;
}
.edit.is-active,
.edit:active {
  background: #ff9966;
  border-color: #ff9966;
  color: #fff;
}

.edit:focus,
.edit:hover {
  background: #ffcccc;
  border-color: #ffcccc;
  color: #fff;
}

.edit {
  color: #fff;
  background-color: #ff9966;
  border-color: #ff9966;
}
.goon.is-active,
.goon:active {
  background: #20b2aa;
  border-color: #20b2aa;
  color: #fff;
}

.goon:focus,
.goon:hover {
  background: #48d1cc;
  border-color: #48d1cc;
  color: #fff;
}

.goon {
  color: #fff;
  background-color: #20b2aa;
  border-color: #20b2aa;
}
.edit-area {
  margin: 2em auto 1em;
}
</style>