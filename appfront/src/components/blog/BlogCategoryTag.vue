<template>
  <div class="me-ct-body" :title="title">
    <bk-container class="me-ct-container">
      <bk-main>
        <div class="me-ct-title me-area">
          <img class="me-ct-picture" :src="defaultAvatar"/>
          <h2 class="me-ct-name">标签：{{ ct.tag }}</h2>
        </div>
        <h3 class="me-ct-meta">{{ ct.count }} 文章</h3>
        <div class="me-ct-articles">
          <article-scroll-page v-bind="article"></article-scroll-page>
        </div>
      </bk-main>
    </bk-container>
  </div>
</template>

<script>
import {bkMain, bkContainer} from 'bk-magic-vue'
import ArticleScrollPage from '../ArticleScrollPage'
import defaultAvatar from '../../assets/book.png'
import axios from "axios"
import {host} from "../../../static/js/host";


export default {
  name: 'BlogCategoryTag',
  component: {
    bkMain, bkContainer
  },
  created() {
    this.getCategoryOrTagAndArticles()
  },
  watch: {
    '$route': 'getCategoryOrTagAndArticles'
  },
  data() {
    this.token = localStorage.token || sessionStorage.token
    return {
      defaultAvatar: defaultAvatar,
      ct: {},
      article: {
        query1: {
          tag_id: "",
        }
      },
    }
  },
  computed: {
    title() {
      return `${this.ct.tag} - 标签 - GDUT`
    }
  },
  methods: {
    getCategoryOrTagAndArticles() {
      let id = this.$route.params.id
      this.article.query1.tag_id = id
      // let type = this.$route.params.type  // 路由为 :type/:id可用（丰富类型）
      // if ('tag' === type) {
      //   this.getTagDetail(id)
      //   this.article.query.tagId = id
      // }
      this.getTagDetail(id)
    },
    getTagDetail(id) {
      let that = this
      axios.get(host + `/api/v1/questions/${id}/get_single_tag/`, { // 获取data列表中的数据
        headers: {
          'Authorization': 'Bearer ' + this.token
        },
        responseType: 'json'
      }).then(data => {
        that.ct = data.data
        console.info(data.data.count)
      }).catch(error => {
        if (error !== 'error') {
          that.$message({type: 'error', message: '标签加载失败', showClose: true})
        }
      })
    }
  },
  components: {
    ArticleScrollPage
  }
}
</script>

<style>
.me-ct-body {
  background-image: url("../../assets/star5.gif");
  /*background-repeat: no-repeat;*/
  /*background-size: cover;*/
  background-position: center center;
}

.me-ct-title {
  text-align: center;
  height: 150px;
  padding: 20px;
}

.me-ct-picture {
  width: 60px;
  height: 60px;
}

.me-ct-name {
  font-size: 28px;
  color: #6e86e4;
}

.me-ct-meta {
  font-size: 12px;
  color: #b25e5e;
}

.me-ct-articles {
  width: 640px;
  margin: 30px auto;
}

</style>
