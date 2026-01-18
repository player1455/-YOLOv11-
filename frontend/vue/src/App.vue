<template>
  <div id="app">
    <el-container>
      <el-header>
        <h1>YOLO Drone Obstacle Avoidance System</h1>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.el-header {
  background-color: #409EFF;
  color: white;
  text-align: center;
  line-height: 60px;
  margin-bottom: 20px;
}

.el-header h1 {
  margin: 0;
  font-size: 24px;
}
</style>
