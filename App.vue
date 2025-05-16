<template>
  <div id="app">
    <Header></Header>
    <main class="container">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import Header from './components/Header.vue'

export default {
  name: 'App',
  components: {
    Header
  }
}
</script>

<style>
/* Add global styles here */
body {
  background-image: url('/public/house.jpg'); /* 背景图片路径 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 创建一个半透明的覆盖层 */
#app::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(210, 236, 209, 0.42); /* 白色半透明 */
  z-index: -1; /* 置于内容下方 */
}

.container {
  padding-top: 70px; /* 为固定导航栏留出空间 */
}
</style>  