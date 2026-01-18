<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>YOLO无人机障碍规避系统</h1>
          <el-menu
            :default-active="activeIndex"
            class="el-menu-demo"
            mode="horizontal"
            @select="handleSelect"
          >
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/flying">实时监控</el-menu-item>
            <el-menu-item index="/map">GPS地图</el-menu-item>
            <el-menu-item index="/analyze">数据分析</el-menu-item>
            <el-sub-menu index="control">
              <template #title>
                <span>控制面板</span>
              </template>
              <el-menu-item index="/control/drone">无人机控制</el-menu-item>
              <el-menu-item index="/control/user">用户管理</el-menu-item>
            </el-sub-menu>
          </el-menu>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      activeIndex: this.$route.path
    }
  },
  watch: {
    '$route'(to) {
      this.activeIndex = to.path
    }
  },
  methods: {
    handleSelect(key, keyPath) {
      this.$router.push(key)
    }
  }
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
  line-height: 60px;
  margin-bottom: 20px;
  padding: 0 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.el-header h1 {
  margin: 0;
  font-size: 24px;
  color: white;
}

.el-menu-demo {
  background-color: transparent;
  border-bottom: none;
}

.el-menu-demo .el-menu-item,
.el-menu-demo .el-sub-menu__title {
  color: white;
}

.el-menu-demo .el-menu-item:hover,
.el-menu-demo .el-sub-menu__title:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.el-menu-demo .el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.el-main {
  padding: 0 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
</style>
