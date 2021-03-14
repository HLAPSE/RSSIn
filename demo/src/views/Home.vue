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
      <el-aside> <AsiderForm /></el-aside>
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
import AsiderForm from "@/components/AsiderForm";

export default {
  name: "Home",
  components: { AsiderForm },
  data() {
    return { isCollapse: false };
  },
  methods: {},
};
</script>
<style scoped>
</style>