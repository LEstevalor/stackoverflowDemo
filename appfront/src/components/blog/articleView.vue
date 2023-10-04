<template>
  <bk-container class="me-view-container">
    <div class="flex-container">
    <bk-main class="custom-main">
      <div class="me-view-card">
        <h1 class="me-view-title">{{ article.title }}</h1>
        <div class="me-view-author">
          <a class="">
            <img class="me-view-picture" :src="avatar"></img>
          </a>
          <div class="me-view-info">
            <bk-button
              v-if="this.article.username == this.username"
              @click="editArticle()"
              style="position: absolute;right: 80%;"
              round
              icon="bk-icon-edit"> 编辑
            </bk-button>
            <span>{{ article.username }}</span>
            <div class="me-view-meta">
              <span>赞同   {{ article.upvotes }}</span>
              <span>不赞同   {{ article.downvotes }}</span>
            </div>
          </div>
        </div>

        <div class="me-view-end">
          <bk-alert
            title="文章 Begin"
            type="success"
            center
            :closable="false">
          </bk-alert>
        </div>


        <div class="me-view-content">
          <div class="article-container">
            <div class="author-info">
              作者：{{ article.username }} | 发布时间：{{ formatDate(article.create_time) }}
            </div>

<!--            <div v-if="this.article.username == this.username">-->
<!--              <markdown-editor :editor=article.editor></markdown-editor>-->
<!--            </div>-->
            <div class="content-container">
              <!-- 内容显示给非文章作者 -->
              <div v-html="article.content"></div>
            </div>
          </div>
        </div>

        <div class="me-view-end">
          <bk-alert
            title="文章 End"
            type="success"
            center
            :closable="false">
          </bk-alert>
        </div>

        <div class="me-view-tag">
          标签：
          <!--<el-tag v-for="t in article.tags" :key="t.id" class="me-view-tag-item" size="mini" type="success">{{t.tagName}}</el-tag>-->
          <!--            <bk-button @click="tagOrCategory('tag', t.id)" size="mini" type="primary" v-for="t in article.tags"-->
          <!--                       :key="t.id" round plain>{{ t.tag }}-->
          <!--            </bk-button>-->
          <bk-button @click="tagOrCategory('tag', article.tag_id)" type="primary">
            {{ article.tag }}
          </bk-button>
        </div>

        <div class="me-view-comment">
          <div class="me-view-comment-write">
            <bk-row :gutter="20">
              <bk-col :span="2">
                <a class="">
                  <img class="me-view-picture" :src="avatar"/>
                </a>
              </bk-col>
              <bk-col :span="22">
                <bk-input
                  type="textarea"
                  :autosize="{ minRows: 2}"
                  placeholder="你的评论..."
                  class="me-view-comment-text"
                  v-model="comment.content"
                  resize="none">
                </bk-input>
              </bk-col>
            </bk-row>

            <bk-row :gutter="20">
              <bk-col :span="2" :offset="22">
                <bk-button type="text" @click="publishComment()">回帖</bk-button>
              </bk-col>
            </bk-row>
          </div>

          <div class="me-view-comment-title">
            <span>{{ this.article.commentCounts }} 条回帖</span>
          </div>

          <commmentz-item
            v-for="(c,index) in comments"
            :comment="c"
            :articleId="article.id"
            :index="comments.length - index - 1"
            :rootCommentCounts="comments.length"
            :key="c.id">
            <!--            @commentCountsIncrement="commentCountsIncrement"-->
          </commmentz-item>

        </div>

      </div>
    </bk-main>
    <bk-aside class="custom-aside">
      <card-relation class="me-area"></card-relation>
      <article-scroll-page v-bind="article1"></article-scroll-page>
    </bk-aside>
</div>
  </bk-container>
</template>

<script>
import CardRelation from '../card/CardRelation'
import {bkContainer, bkMain, bkButton, bkCol, bkRow, bkInput, bkAside} from 'bk-magic-vue'
import ArticleScrollPage from '../ArticleScrollPage'
import MarkdownEditor from './MarkdownEditor'
import CommmentItem from './CommentItem'
import {formatDate} from '../../api/time'
import default_avatar from '../../assets/user.png'
import axios from "axios";
import {host} from "../../../static/js/host";

export default {
  name: 'articleView',
  component: {
    bkContainer, bkMain, bkButton, bkCol, bkRow, bkInput, bkAside,
  },
  created() {
    this.article1.query1.article_id = this.$route.params.id
    this.getArticle()
  },
  watch: {
    '$route': 'getArticle'
  },
  data() {
    this.token = localStorage.token || sessionStorage.token
    this.username = localStorage.username || sessionStorage.username
    return {
      article: {
        id: '',
        title: '',
        upvotes: 0,
        downvotes: 0,
        content: '',
        username: '',
        tag: '',
        tag_id: 0,
        category: {},
        createDate: '',
        commentCounts: 0,
        editor: {
          value: '',
          toolbarsFlag: false,
          subfield: false,
          defaultOpen: 'preview'
        }
      },
      comments: [],
      comment: {
        article: {},
        content: ''
      },
      article1: {
        query1: {
          article_id: "",
        }
      },
    }
  },
  computed: {
    avatar() {
      return default_avatar
    },
    title() {
      return `${this.article.title} - 文章`
    }
  },
  methods: {
    successInfoBox(msg) {
      const h = this.$createElement
      const a = this.$bkInfo({
        type: 'success',
        title: msg,
        showFooter: false,
        subHeader: h('a', {
          style: {
            color: '#3a84ff',
            textDecoration: 'none',
            cursor: 'pointer'
          }
        })
      })
      let num = 1
      let t = setInterval(() => {
        if (--num === 0) {
          clearInterval(t)
          a.close()
        }
      }, 1000)
    },
    errorInfoBox(msg) {
      const a = this.$bkInfo({
        type: 'error',
        title: 'Fail:' + msg,
        subTitle: '窗口2秒后关闭',
        showFooter: false
      })
      let num = 2
      let t = setInterval(() => {
        a.subTitle = `此窗口${--num}秒后关闭`
        if (num === 0) {
          clearInterval(t)
          a.close()
        }
      }, 1000)
    },
    formatDate(time) {
      return formatDate(time)
    },
    tagOrCategory(type, id) {
      this.$router.push({path: `/${type}/${id}`})
    },
    editArticle() {
      this.$router.push({path: `/write/${this.article.id}/`})
    },
    getArticle() {
      let that = this
      axios.get(host + '/api/v1/questions/get_question/', { // 获取data列表中的数据
        headers: {
          'Authorization': 'Bearer ' + this.token
        },
        responseType: 'json',
        params: {question_id: that.$route.params.id}
      }).then(data => {
        that.article = data.data
        console.log(that.article.content)
        that.article.editor = {}
        that.article.editor.value = data.data.content
        console.log(that.article.editor.value)
        that.getCommentsByArticle()
      }).catch(error => {
        alert(error)
      })
    },
    publishComment() {
      let that = this
      if (!that.comment.content) {
        return;
      }
      that.comment.article.id = that.article.id
      let params = {question_id: that.article.id, content: that.comment.content, username: that.username}
      axios.post(host + '/api/v1/back_questions/', params, {
        responseType: 'json',
        withCredentials: true // 跨域情况可以携带cookie
      }).then(data => {
        that.comment.content = ''
        that.comments.push(data.data)
        that.commentCountsIncrement()
        that.successInfoBox("评论成功")
      }).catch(error => {
        that.errorInfoBox("评论失败")
      })
    },
    commentCountsIncrement() {
      this.article.commentCounts += 1
    },
    getCommentsByArticle() {
      let that = this
      axios.get(host + `/api/v1/back_questions/${that.article.id}/get_back_by_question`, {
        responseType: 'json',
        withCredentials: true // 跨域情况可以携带cookie
      }).then(data => {
        that.comments = data.data.results
        that.article.commentCounts = data.data.results.length
      }).catch(error => {
        this.errorInfoBox("回帖加载失败")
      })
    }
  },
  components: {
    'commmentz-item': CommmentItem,
    'markdown-editor': MarkdownEditor,
    ArticleScrollPage,
    'card-relation': CardRelation,
  },
  //组件内的守卫 调整body的背景色
  beforeRouteEnter(to, from, next) {
    window.document.body.style.backgroundColor = '#fff';
    next();
  },
  beforeRouteLeave(to, from, next) {
    window.document.body.style.backgroundColor = '#f5f5f5';
    next();
  },
}
</script>

<style>
.custom-main {
  width: 60%; /* 设置宽度为 50% */
  border-radius: 8px; /* 添加圆角 */
  box-shadow: 0 4px 6px rgba(9, 9, 9, 0.1); /* 添加阴影 */
  transition: all 0.3s; /* 添加过渡效果 */
  margin: 16px; /* 添加一致的边距 */
}

.custom-aside {
  width: 40%; /* 设置宽度为 50% */
  border-radius: 8px; /* 添加圆角 */
  box-shadow: 0 4px 6px rgba(9, 9, 9, 0.1); /* 添加阴影 */
  transition: all 0.3s; /* 添加过渡效果 */
  margin: 16px; /* 添加一致的边距 */
}

.flex-container {
  display: flex;
}

/*非作者文本显示*/
.article-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  line-height: 1;
  color: #333;
}

.article-title {
  font-size: 2em;
  margin-bottom: 20px;
}

.author-info {
  font-size: 0.9em;
  color: #666;
  margin-bottom: 30px;
}

.content-container {
  background-color: #fff;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}


.me-view-container {
  width: 1600px;
}

.me-view-title {
  font-size: 34px;
  font-weight: 800;
  line-height: 1.3;
}

.me-view-author {
  /*margin: 30px 0;*/
  margin-top: 20px;
  vertical-align: middle;
}

.me-view-picture {
  width: 40px;
  height: 40px;
  border: 1px solid #ddd;
  border-radius: 50%;
  vertical-align: middle;
  background-color: #5fb878;
}

.me-view-info {
  display: inline-block;
  vertical-align: middle;
  margin-left: 8px;
}

.me-view-meta {
  font-size: 12px;
  color: #969696;
}

.me-view-end {
  margin-top: 10px;
}

.me-view-tag {
  margin-top: 10px;
  padding-left: 6px;
  border-left: 4px solid #c5cac3;
}

.me-view-comment {
  margin-top: 40px;
}

.me-view-comment-title {
  font-weight: 600;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 20px;
}

.me-view-comment-write {
  margin-top: 20px;
}

.me-view-comment-text {
  font-size: 16px;
}

.v-show-content {
  padding: 8px 25px 15px 30px !important;
}

.v-note-wrapper .v-note-panel {
  box-shadow: none !important;
}

.v-note-wrapper .v-note-panel .v-note-show .v-show-content, .v-note-wrapper .v-note-panel .v-note-show .v-show-content-html {
  background: #fff !important;
}

</style>
