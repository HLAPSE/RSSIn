<template>
  <el-scrollbar
    ><el-image :src="require('@/assets/404.png')" fit="scale-down"></el-image
  ></el-scrollbar>
</template>

<script>
export default {
  name: "404",
  components: {},
};
</script>

<style scoped>
.el-image {
  height: 50%;
}
html {
  height: 100vh;
}
</style>