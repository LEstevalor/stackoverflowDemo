<template>
  <div style="background-color: #ddf1e2" class="page-container">
<!--    <img src="../assets/TEGNOLOGY2.jpg" style="float:left;"/>-->
<!--    <img src="../assets/star.gif" style="float:left;"/>&ndash;&gt;-->
    <bk-swiper :pics="pics" :loop-time="4000" class="swiper" style="float:right;"></bk-swiper>
    <h1 class="artistic-title">KEY: 数据库  存储  OS  NOSQL  MYSQL  REDIS  网络  并发  缓存  内存  服务  集群 DOCKER K8S</h1>
  </div>
</template>

<script>
import { bkSwiper } from 'bk-magic-vue'
import firstSwiper from '../assets/2023label.jpg'
import secondSwiper from '../assets/gdut_label.jpg'
import thirdSwiper from '../assets/db.jpg'
import fourthSwiper from '../assets/nosql.jpg'
import fifthSwiper from '../assets/machine.jpg'
import sixthSwiper from '../assets/dragonCenter.jpg'


export default {
  name: 'top',
  components: {
    bkSwiper // 轮播图
  },
  data () {
    return {
      pics: [
        // { url: firstSwiper, link: 'https://www.npmjs.com/package/bk-magic-vue' },
        {url: firstSwiper},
        {url: secondSwiper},
        {url: thirdSwiper},
        {url: fourthSwiper},
        {url: fifthSwiper},
        {url: sixthSwiper}
      ]
    }
  },
  mounted () {
    // 未登录跳转回登录页面逻辑
    var username = sessionStorage.username || localStorage.username // 注意取的是Storage的信息
    if (username && (sessionStorage.token || localStorage.token)) {
      console.log('登录了')
    } else {
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.swiper {
  width: 50%;
  height: 75%; /* 600px; */
}

.page-container {
  /*background-image: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);*/
  /* 其他样式 */
  /*opacity: 0.9; !* 设置透明度为 80% *!*/
  background-image: url("../assets/star2.gif");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center center;
}

/* 为文本添加动画效果 */
@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

/* 艺术字与变色 */
.artistic-title {
  color: #ffffff;
  font-family: "Pacifico", cursive; /* 使用艺术字体 */
  font-size: 1.5rem;
  text-align: center;
}

</style>
