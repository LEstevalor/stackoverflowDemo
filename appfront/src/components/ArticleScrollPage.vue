<template>
  <div class="background">
<!--    <div class="search-container">-->
<!--      <input class="search-input" v-model="title" type="search" placeholder="搜索...">-->
<!--      <button class="search-button" @click="getArticles">搜索</button>-->
<!--    </div>-->
    <scroll-page :loading="loading" :offset="offset" :no-data="noData" v-on:load="load">
      <article-item v-for="a in articles" :key="a.id" v-bind="a"></article-item>
    </scroll-page>
  </div>
</template>

<script>
import ArticleItem from '../components/scrollpage/ArticleItem'
import ScrollPage from '../components/scrollpage'
import axios from "axios"
import {host} from "../../static/js/host"

export default {
  name: "ArticleScrollPage",
  props: {
    offset: {
      type: Number,
      default: 100
    },
    page: {
      type: Object,
      default() {
        return {}
      }
    },
    query: {
      type: Object,
      default() {
        return {}
      }
    },
    query1: {
      type: Object,
      default() {
        return {}
      }
    }
  },
  watch: {
    'query1': {
      handler() {
        this.innerPage.pageNumber = 1
        this.articles = []
        this.noData = false
        this.getArticles()
      },
      deep: true
    },
    'query': {
      handler() {
        this.noData = false
        this.articles = []
        this.innerPage.pageNumber = 1
        this.getArticles()
      },
      deep: true
    },
    'page': {
      handler() {
        this.noData = false
        this.articles = []
        this.innerPage = this.page
        this.getArticles()
      },
      deep: true
    }
  },
  created() {
    this.getArticles()
  },
  data() {
    this.token = localStorage.token || sessionStorage.token
    return {
      title: '',
      loading: false,
      noData: false,
      innerPage: {
        pageSize: 5,
        pageNumber: 1,
        name: 'a.createDate',
        sort: 'desc'
      },
      articles: []
    }
  },
  methods: {
    load() {
      this.getArticles()
    },
    view(id) {
      this.$router.push({path: `/view/${id}`})
    },
    getArticles() {
      let path = '/api/v1/questions/'
      if (this.query1.tag_id)
        path = `/api/v1/questions/${this.query1.tag_id}/get_question_by_tag/`
      if (this.query1.article_id)
        path = `/api/v1/questions/${this.query1.article_id}/get_related_questions/`
      // 支持模糊搜索
      let params = {}
      if (this.title !== '') {
        params = {"title": this.title}
      }
      this.loading = true
      axios.get(host + path, { // 获取data列表中的数据
        headers: {
          'Authorization': 'Bearer ' + this.token
        },
        responseType: 'json',
        params: params
      }).then(data => {
        let newArticles = data.data.results
        if (newArticles && newArticles.length > 0) {
          this.innerPage.pageNumber += 1
          this.articles = this.articles.concat(newArticles)
        } else {
          this.noData = true
        }
      }).catch(error => {
        if (error !== 'error') {
          this.$message({type: 'error', message: '文章加载失败!', showClose: true})
        }
      }).finally(() => {
        this.loading = false
      })
    },
    view(id) {
      this.$router.push(`/articleView/${id}`)
      /*反携号可以代入外部值*/
    },
  },
  components: {
    'article-item': ArticleItem,
    'scroll-page': ScrollPage
  }

}
</script>

<style scoped>
.background {
  background-image: url("../assets/star6.gif");
}

/* 搜索容器样式 */
.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  /*background-color: #f5f5f5;*/
}

/* 搜索输入框样式 */
.search-input {
  width: 100%;
  max-width: 600px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px 0 0 5px;
  font-size: 16px;
  outline: none;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 搜索按钮样式 */
.search-button {
  padding: 10px 20px;
  border: none;
  border-radius: 0 5px 5px 0;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease;
}

/* 搜索按钮悬停效果 */
.search-button:hover {
  background-color: #0056b3;
}
</style>
