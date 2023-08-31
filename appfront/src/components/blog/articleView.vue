<template>
  <bk-container class="me-view-container">
    <bk-main>
      <div class="me-view-card">
        <h1 class="me-view-title">{{ article.title }}</h1>
        <div class="me-view-author">
          <a class="">
            <img class="me-view-picture" :src="avatar"></img>
          </a>
          <div class="me-view-info">
            <span>{{ article.username }}</span>
            <div class="me-view-meta">
              <span>{{ formatDate(article.create_time) }}</span>
              <span>赞同   {{ article.upvotes }}</span>
              <span>不赞同   {{ article.downvotes }}</span>
            </div>

          </div>
          <bk-button
            @click="editArticle()"
            style="position: absolute;left: 60%;"
            round
            icon="bk-icon-edit">编辑
          </bk-button>
        </div>
        <div class="me-view-content">
          <markdown-editor :editor=article.editor></markdown-editor>
        </div>

        <div class="me-view-end">
          <bk-alert
            title="文章End..."
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
          <bk-button @click="tagOrCategory('tag', article.id)" type="primary">
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
                <bk-button type="text" @click="publishComment()">评论</bk-button>
              </bk-col>
            </bk-row>
          </div>

          <div class="me-view-comment-title">
            <span>{{ article.commentCounts }} 条评论</span>
          </div>

          <commment-item
            v-for="(c,index) in comments"
            :comment="c"
            :articleId="article.id"
            :index="index"
            :rootCommentCounts="comments.length"
            @commentCountsIncrement="commentCountsIncrement"
            :key="c.id">
          </commment-item>

        </div>

      </div>
    </bk-main>

  </bk-container>
</template>

<script>
import {bkContainer, bkMain, bkButton, bkCol, bkRow, bkInput, bkAside} from 'bk-magic-vue'
import MarkdownEditor from './MarkdownEditor'
import CommmentItem from './CommentItem'
import {formatDate} from '../../api/time'
// import {viewArticle} from '@/api/article'
// import {getCommentsByArticle, publishComment} from '@/api/comment'
import default_avatar from '../../assets/user.png'
import axios from "axios";
import {host} from "../../../static/js/host";

export default {
  name: 'articleView',
  component: {
    bkContainer, bkMain, bkButton, bkCol, bkRow, bkInput, bkAside
  },
  created() {
    this.getArticle()
  },
  watch: {
    '$route': 'getArticle'
  },
  data() {
    this.token = localStorage.token || sessionStorage.token
    return {
      article: {
        id: '',
        title: '',
        upvotes: 0,
        downvotes: 0,
        content: '',
        username: '',
        tags: [],
        category: {},
        createDate: '',
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
      }
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
    formatDate(time) {
      return formatDate(time)
    },
    tagOrCategory(type, id) {
      this.$router.push({path: `/${type}/${id}`})
    },
    editArticle() {
      this.$router.push({path: `/write/${this.article.id}`})
    },
    getArticle() {
      let that = this
      console.log("aaa")
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
        // that.getCommentsByArticle()
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
      let parms = {articleId: that.article.id, content: that.comment.content}
      publishComment(parms, this.$store.state.token).then(data => {
        if (data.success) {
          that.$message({type: 'success', message: '评论成功', showClose: true})
          that.comment.content = ''
          that.comments.unshift(data.data)
          that.commentCountsIncrement()

        } else {
          that.$message({type: 'error', message: data.msg, showClose: true})
        }

      }).catch(error => {
        if (error !== 'error') {
          that.$message({type: 'error', message: '评论失败', showClose: true})
        }
      })
    },

    getCommentsByArticle() {
      let that = this
      getCommentsByArticle(that.article.id).then(data => {
        if (data.success) {
          that.comments = data.data
        } else {
          that.$message({type: 'error', message: '评论加载失败', showClose: true})
        }
      }).catch(error => {
        if (error !== 'error') {
          that.$message({type: 'error', message: '评论加载失败', showClose: true})
        }
      })
    }
  },
  components: {
    'markdown-editor': MarkdownEditor,
    CommmentItem
  },
  //组件内的守卫 调整body的背景色
  beforeRouteEnter(to, from, next) {
    window.document.body.style.backgroundColor = '#fff';
    next();
  },
  beforeRouteLeave(to, from, next) {
    window.document.body.style.backgroundColor = '#f5f5f5';
    next();
  }
}
</script>

<style>
.me-view-container {
  width: 1600px;
}

.bk-main {
  overflow: hidden;
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
