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
              <el-avatar icon="el-icon-user-solid"></el-avatar>
            </el-menu-item>
          </el-col>
        </el-row>
      </el-menu>
    </el-header>
    <el-container>
      <el-aside
        ><el-menu>
          <el-submenu index="1">
            <template #title>
              <i class="el-icon-location"></i>
              <span>导航一</span>
            </template>
            <el-menu-item-group>
              <template #title>分组一</template>
              <el-menu-item index="1-1">选项1</el-menu-item>
              <el-menu-item index="1-2">选项2</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="分组2">
              <el-menu-item index="1-3">选项3</el-menu-item>
            </el-menu-item-group>
            <el-submenu index="1-4">
              <template #title>选项4</template>
              <el-menu-item index="1-4-1">选项1</el-menu-item>
            </el-submenu>
          </el-submenu>
          <el-menu-item index="2">
            <i class="el-icon-menu"></i>
            <template #title>导航二</template>
          </el-menu-item>
          <el-menu-item index="3" disabled>
            <i class="el-icon-document"></i>
            <template #title>导航三</template>
          </el-menu-item>
          <el-menu-item index="4">
            <i class="el-icon-setting"></i>
            <template #title>导航四</template>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <el-card class="box-card">
          <div class="card-header">
            <span>这是一篇文章</span>
            <el-button class="button" type="text">展开</el-button>
          </div>
          <div class="text item">
            <ul>
              <li>标题</li>
              <li>概要</li>
            </ul>
          </div>
        </el-card>
        <!-- 回到顶部 -->
        <el-backtop></el-backtop>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
// @ is an alias to /src

export default {
  name: "Home",
  components: {},
  data() {
    return { isCollapse: false };
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
  },
};
</script>
<style scoped>
</style>