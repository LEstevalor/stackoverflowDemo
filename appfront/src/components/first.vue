<template>
  <div class="page-container">
    <bk-container class="custom-container">
      <div class="flex-container">
        <bk-aside class="custom-aside">
          <article-scroll-page></article-scroll-page>
        </bk-aside>
        <bk-main class="custom-main">
          <card-me class="me-area"></card-me>
          <card-tag :tags="hotTags"></card-tag>
          <card-article cardHeader="最热文章" :articles="hotArticles"></card-article>
          <card-article cardHeader="最新文章" :articles="newArticles"></card-article>
        </bk-main>
      </div>
      <!--      <bk-row justify="space-between">-->

    </bk-container>
  </div>
</template>

<script>
import CardMe from './card/CardMe'
import CardArticle from './card/CardArticle'
import CardArchive from './card/CardArchive'
import CardTag from './card/CardTag'

import {bkContainer, bkAside, bkMain, bkRow, bkCol} from 'bk-magic-vue'
import ArticleScrollPage from './ArticleScrollPage'
import axios from "axios";
import {host} from "../../static/js/host";

// import {getArticles, getHotArtices, getNewArtices} from '@/api/article'

export default {
  name: 'first',
  component: {
    bkContainer,
    bkAside,
    bkMain,
    bkRow,
    bkCol,
  },
  created() {
    // this.getHotArtices()
    // this.getNewArtices()
    this.getHotTags()
  },
  data() {
    this.token = localStorage.token || sessionStorage.token
    return {
      hotTags: [],
      hotArticles: [],
      newArticles: [],
      archives: []
    }
  },
  methods: {
    getHotArtices() {
      let that = this
      getHotArtices().then(data => {
        that.hotArticles = data.data
      }).catch(error => {
        if (error !== 'error') {
          that.$message({type: 'error', message: '最热文章加载失败!', showClose: true})
        }

      })

    },
    getNewArtices() {
      let that = this
      getNewArtices().then(data => {
        that.newArticles = data.data
      }).catch(error => {
        if (error !== 'error') {
          that.$message({type: 'error', message: '最新文章加载失败!', showClose: true})
        }

      })

    },
    getHotTags() {
      axios.get(host + '/api/v1/questions/list_hot_tag/', {
        headers: {
          'Authorization': 'Bearer ' + this.token
        },
        responseType: 'json'
      }).then(data => {
        this.hotTags = data.data.results
        console.log(this.hotTags)
      }).catch(error => {
        if (error !== 'error') {
          this.$message({type: 'error', message: '最热标签加载失败!', showClose: true})
        }
      })
    }

  },
  components: {
    'card-me': CardMe,
    'card-article': CardArticle,
    'card-tag': CardTag,
    ArticleScrollPage,
    CardArchive
  }
}
</script>

<style scoped>
/*背景*/
.page-container {
  background-image: url("../assets/star4.gif");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center center;
}

.custom-container {
  font-family: "Roboto", sans-serif; /* 使用现代化字体 */
}

.flex-container {
  display: flex;
}

.custom-aside,
.custom-main {
  width: 50%; /* 设置宽度为 50% */
  border-radius: 8px; /* 添加圆角 */
  box-shadow: 0 4px 6px rgba(9, 9, 9, 0.1); /* 添加阴影 */
  transition: all 0.3s; /* 添加过渡效果 */
  margin: 16px; /* 添加一致的边距 */
}

.custom-aside:hover,
.custom-main:hover {
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15); /* 鼠标悬停时增加阴影 */
  transform: translateY(-2px); /* 鼠标悬停时向上移动 */
}

.box {
  background-color: #f0f0f0;
  padding: 16px;
  text-align: center;
  height: 100%;
}

.bk-container {
  width: 960px;
}

.bk-aside {
  margin-left: 20px;
  width: 260px;
}

.bk-main {
  padding: 0px;
  line-height: 16px;
}

.bk-card {
  border-radius: 0;
}

.bk-card:not(:first-child) {
  margin-top: 20px;
}
</style>
