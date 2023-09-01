<template>
  <div class="me-ct-body" v-title :data-title="title">
    <bk-container class="me-ct-container">
      <bk-main>
        <div class="me-ct-title me-area">
          <template v-if="this.$route.params.type === 'tag'">
            <img class="me-ct-picture" :src="defaultAvatar"/>
            <h3 class="me-ct-name">{{ ct.tag }}</h3>
          </template>

          <template v-else>
            <img class="me-ct-picture" :src="defaultAvatar"/>
            <h3 class="me-ct-name">{{ ct.tag }}</h3>
            <p>{{ ct.description }}</p>
          </template>

          <span class="me-ct-meta">{{ ct.tag }} 文章</span>
        </div>

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
// import {getArticlesByCategory, getArticlesByTag} from '@/api/article'
// import {getTagDetail} from '@/api/tag'
// import {getCategoryDetail} from '@/api/category'
import defaultAvatar from '../../assets/book.png'


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
    return {
      defaultAvatar: defaultAvatar,
      ct: {},
      article: {
        query: {
          tagId: '',
          categoryId: ''
        }
      },
    }
  },
  computed: {
    title() {
      if (this.$route.params.type === 'tag') {
        return `${this.ct.tagName} - 标签 - 码神之路`
      }
      return `${this.ct.categoryName} - 文章分类 - 码神之路`
    }
  },
  methods: {
    getCategoryOrTagAndArticles() {
      let id = this.$route.params.id
      let type = this.$route.params.type
      if ('tag' === type) {
        this.getTagDetail(id)
        this.article.query.tagId = id
      } else {
        this.getCategoryDetail(id)
        this.article.query.categoryId = id
      }

    },
    getCategoryDetail(id) {
      let that = this
      getCategoryDetail(id).then(data => {
        that.ct = data.data
      }).catch(error => {
        if (error !== 'error') {
          that.$message({type: 'error', message: '文章分类加载失败', showClose: true})
        }
      })
    },
    getTagDetail(id) {
      let that = this
      getTagDetail(id).then(data => {
        that.ct = data.data
      }).catch(error => {
        if (error !== 'error') {
          that.$message({type: 'error', message: '标签加载失败', showClose: true})
        }
      })
    },
    getArticlesByCategory(id) {
      let that = this
      getArticlesByCategory(id).then(data => {
        that.articles = data.data
      }).catch(error => {
        if (error !== 'error') {
          that.$message({type: 'error', message: '文章加载失败', showClose: true})
        }
      })
    },
    getArticlesByTag(id) {
      let that = this
      getArticlesByTag(id).then(data => {
        that.articles = data.data
      }).catch(error => {
        if (error !== 'error') {
          that.$message({type: 'error', message: '文章加载失败', showClose: true})
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

.bk-main {
  padding: 0;
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
}

.me-ct-meta {
  font-size: 12px;
  color: #969696;
}

.me-ct-articles {
  width: 640px;
  margin: 30px auto;
}

</style>
