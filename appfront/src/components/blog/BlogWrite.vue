<template>
  <div id="write" v-title :data-title="title" class="background">
    <bk-container>
      <div class="me-write-info">写文章</div>
      <div class="me-write-btn">
        <bk-button class="publish-btn" @click="publishShow">发布</bk-button>
        <bk-button theme="warning" class="cancel-btn" @click="cancel">取消</bk-button>
      </div>

      <div>
        <div class="me-write-info-left">文章标签</div>
        <bk-select v-model="tag_value" style="width: 250px;" class="select-use">
          <bk-option class="custom-option"
                     v-for="option in tags"
                     :key="option.tag"
                     :id="option.tag"
                     :name="option.tag">
            <span>{{ option.tag }}</span>
            <i class="bk-icon icon-close"></i>
          </bk-option>
        </bk-select>
      </div>

      <bk-container class="me-area me-write-box">
        <bk-main class="me-write-main">
          <div class="me-write-title">
            <bk-input resize="none"
                      type="textarea"
                      autosize
                      v-model="articleForm.title"
                      placeholder="请输入标题"
                      class="me-write-input">
            </bk-input>

          </div>
          <div id="placeholder" style="visibility: hidden;height: 89px;display: none;"></div>
          <markdown-editor :editor="articleForm.editor" class="me-write-editor"></markdown-editor>
        </bk-main>
      </bk-container>
    </bk-container>
  </div>
</template>

<script>
import {
  bkContainer, bkMain, bkButton, bkCol, bkRow, bkInput, bkAside, bkDialog, bkForm,
  bkFormItem, bkCheckbox, bkCheckboxGroup, bkSelect, bkOption
} from 'bk-magic-vue'
import BaseHeader from '../BaseHeader'
import MarkdownEditor from './MarkdownEditor'
import axios from "axios";
import {host} from "../../../static/js/host";

export default {
  name: 'BlogWrite',
  component: {
    bkContainer, bkMain, bkButton, bkCol, bkRow, bkInput, bkAside, bkDialog, bkForm, bkFormItem, bkCheckbox,
    bkCheckboxGroup, bkSelect, bkOption
  },
  mounted() {
    this.getTags()
    if (this.$route.params.id) {
      this.getArticle()
    }
    // this.editorToolBarToFixedWrapper = this.$_.throttle(this.editorToolBarToFixed, 200)
    // window.addEventListener('scroll', this.editorToolBarToFixedWrapper, false);
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.editorToolBarToFixedWrapper, false)
  },
  data() {
    this.token = localStorage.token || sessionStorage.token
    this.username = localStorage.username || sessionStorage.username
    return {
      publishVisible: false,
      categorys: [],
      tags: [],
      tag_value: "",
      articleForm: {
        id: '',
        title: '',
        summary: '',
        tags: [],
        editor: {
          value: '',
          ref: '',//保存mavonEditor实例  实际不该这样
          default_open: 'edit',
          toolbars: {
            bold: true, // 粗体
            italic: true, // 斜体
            header: true, // 标题
            underline: true, // 下划线
            strikethrough: true, // 中划线
            mark: true, // 标记
            superscript: true, // 上角标
            subscript: true, // 下角标
            quote: true, // 引用
            ol: true, // 有序列表
            ul: true, // 无序列表
            imagelink: true, // 图片链接
            code: true, // code
            fullscreen: true, // 全屏编辑
            readmodel: true, // 沉浸式阅读
            help: true, // 帮助
            undo: true, // 上一步
            redo: true, // 下一步
            trash: true, // 清空
            navigation: true, // 导航目录
            //subfield: true, // 单双栏模式
            preview: true, // 预览
          }
        }
      },
      rules: {
        summary: [
          {required: true, message: '请输入摘要', trigger: 'blur'},
          {max: 80, message: '不能大于80个字符', trigger: 'blur'}
        ],
        category: [
          {required: true, message: '请选择文章分类', trigger: 'change'}
        ],
        tags: [
          {type: 'array', required: true, message: '请选择标签', trigger: 'change'}
        ]
      }
    }
  },
  computed: {
    title() {
      return '写文章 - GDUT'
    }
  },
  methods: {
    getArticle() {
      let that = this
      axios.get(host + '/api/v1/questions/get_question/', { // 获取data列表中的数据
        headers: {
          'Authorization': 'Bearer ' + this.token
        },
        responseType: 'json',
        params: {question_id: that.$route.params.id}
      }).then(data => {
        this.articleForm.id = data.data.id
        that.articleForm.editor.ref.d_render = data.data.content
        that.articleForm.editor.value = data.data.content
        that.tag_value = data.data.tag
        that.articleForm.title = data.data.title
      }).catch(error => {
        alert(error)
      })
    },
    getArticleById(id) {
      let that = this
      let data = {tag: this.tag_value, title: this.articleForm.title, content: this.articleForm.editor.ref.d_render}
      axios.put(host + `/api/v1/questions/${id}/`, data, {
        responseType: 'json',
        withCredentials: true // 跨域情况可以携带cookie
      }).then(data => {
        this.articleForm.id = data.data.id
        this.$router.push(`/articleView/${data.data.id}`)
      }).catch(error => {
        if (error !== 'error') {
          that.$message({type: 'error', message: '文章加载失败', showClose: true})
        }
      })
    },
    publishShow() {
      if (!this.articleForm.title) {
        this.warningInfoBox('标题不能为空哦')
        return
      }
      if (this.articleForm.title.length > 30) {
        this.warningInfoBox('标题不能大于30个字符')
        return
      }
      if (!this.articleForm.editor.ref.d_render) {
        this.warningInfoBox('内容不能为空哦')
        return
      }
      if (!this.tag_value) {
        this.warningInfoBox('标签不能为空')
        return
      }
      let data = {tag: this.tag_value, title: this.articleForm.title, content: this.articleForm.editor.ref.d_render,
                  username: this.username}
      if (this.$route.params.id) {
        this.getArticleById(this.$route.params.id)
      } else {
      axios.post(host + '/api/v1/questions/', data, {
        responseType: 'json',
        withCredentials: true // 跨域情况可以携带cookie
      }).then(data => {
        this.articleForm.id = data.data.id
        this.$router.push(`/articleView/${data.data.id}`)
        this.successInfoBox("文章发布成功")
      }).catch(error => {
        this.errorInfoBox("文章发布失败")
      })
        }
    },
    publish(articleForm) {
      let that = this

      this.$refs[articleForm].validate((valid) => {
        if (valid) {

          let tags = this.articleForm.tags.map(function (item) {
            return {id: item};
          });

          let article = {
            id: this.articleForm.id,
            title: this.articleForm.title,
            summary: this.articleForm.summary,
            category: this.articleForm.category,
            tags: tags,
            body: {
              content: this.articleForm.editor.value,
              contentHtml: this.articleForm.editor.ref.d_render
            }

          }

          this.publishVisible = false;

          let loading = this.$loading({
            lock: true,
            text: '发布中，请稍后...'
          })

          publishArticle(article, this.$store.state.token).then((data) => {
            if (data.success) {
              loading.close();
              that.$message({message: '发布成功啦', type: 'success', showClose: true})
              that.$router.push({path: `/view/${data.data.id}`})
            } else {
              that.$message({message: error, type: '发布文章失败:' + data.msg, showClose: true});
            }

          }).catch((error) => {
            loading.close();
            if (error !== 'error') {
              that.$message({message: error, type: 'error', showClose: true});
            }
          })

        } else {
          return false;
        }
      });
    },
    // 取消按钮
    cancel() {
      this.$bkInfo({
        type: 'warning',
        title: '此操作会清空所写文章',
        confirmFn(vm) {
          location.reload();
          console.warn(vm)
        },
        cancelFn(vm) {
          console.warn(vm)
        },
        afterLeaveFn(vm) {
          console.log(vm)
        }
      })
    },
    // 获取所有标签
    getTags() {
      let that = this
      axios.get(host + '/api/v1/questions/list_tag/', { // 获取data列表中的数据
        headers: {
          'Authorization': 'Bearer ' + this.token
        },
        responseType: 'json'
      }).then(data => {
        that.tags = data.data.results
      }).catch(error => {
        that.$message({type: 'error', message: '标签加载失败', showClose: true})
      })
    },
    editorToolBarToFixed() {
      let toolbar = document.querySelector('.v-note-op');
      let curHeight = document.documentElement.scrollTop || document.body.scrollTop;
      if (curHeight >= 160) {
        document.getElementById("placeholder").style.display = "block"; //bad  用计算属性较好
        toolbar.classList.add("me-write-toolbar-fixed");
      } else {
        document.getElementById("placeholder").style.display = "none";
        toolbar.classList.remove("me-write-toolbar-fixed");
      }
    },
    warningInfoBox(msg) {
      this.$bkInfo({
        type: 'warning',
        title: msg,
        cancelFn(vm) {
          console.warn(vm)
        }
      })
    },
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
    }
  },
  components: {
    'base-header': BaseHeader,
    'markdown-editor': MarkdownEditor
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
.background {
  background-image: url("../../assets/star4.gif");
}

.select-use {
  text-align: center;
  color: #03f892;
  font-weight: bold; /*加粗*/
}

.me-write-info {
  font-size: 1.2rem;
  font-weight: bold;
  color: #4a4a4a;
  line-height: 60px;
}

.me-write-info-left {
  font-size: 1.2rem;
  font-weight: bold;
  color: #4a4a4a;
  line-height: 60px;
  text-align: left;
}

.me-write-btn {
  margin-top: 10px;
  display: flex;
  gap: 1rem;
}

.publish-btn,
.cancel-btn {
  border-radius: 20px;
  font-size: 1rem;
  font-weight: bold;
  text-transform: uppercase;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
}

.publish-btn {
  background-image: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
  color: #fff;
}

.publish-btn:hover {
  background-image: linear-gradient(to right, #2575fc 0%, #6a11cb 100%);
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #4a4a4a;
}

.cancel-btn:hover {
  background-color: #e0e0e0;
}


.me-write-box {
  max-width: 100%;
  margin: 80px auto 0;
}

.me-write-main {
  padding: 0;
}

.me-write-title {
}

.me-write-input textarea {
  font-size: 32px;
  font-weight: 600;
  height: 20px;
  border: none;
}

.me-write-editor {
  min-height: 400px !important;
  max-height: 520px;
}

.me-title img {
  max-height: 2.4rem;
  max-width: 100%;
}

.custom-option .icon-close {
  display: none;
  position: absolute;
  right: 0;
  top: 3px;
  font-size: 26px;
  color: #f50057;
  width: 26px;
  height: 26px;
  line-height: 26px;
  text-align: center;
}

.custom-option:hover .icon-close {
  display: block;
}
</style>
