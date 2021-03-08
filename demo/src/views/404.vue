<template>
  <div class="demo-image">
    <el-image :src="require('@/assets/404.png')" fit="scale-down"></el-image>
  </div>
</template>

<script>
export default {
  name: "404",
  components: {},
};
</script>

<style scoped>
el-image {
  width: 100%;
}
</style>