<template>
  <scroll-page :loading="loading" :offset="offset" :no-data="noData" v-on:load="load">
    <article-item v-for="a in articles" :key="a.id" v-bind="a"></article-item>
  </scroll-page>
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
      console.log(this.query1.tag_id)
      if (this.query1.tag_id)
        path = `/api/v1/questions/${this.query1.tag_id}/get_question_by_tag/`

      this.loading = true
      // getArticles(this.query, this.innerPage)
      axios.get(host + path, { // 获取data列表中的数据
        headers: {
          'Authorization': 'Bearer ' + this.token
        },
        responseType: 'json'
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
.bk-card {
  border-radius: 0;
}

.bk-card:not(:first-child) {
  margin-top: 10px;

}
</style>
