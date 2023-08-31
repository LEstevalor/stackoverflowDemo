<template>
  <bk-card class="me-area" :body-style="{ padding: '16px' }">
    <div class="me-article-header">

      <a @click="articleView(id)" class="me-article-title">贴：{{ title }}</a>
      <bk-button v-if="weight > 0" class="me-article-icon" type="text">置顶</bk-button>
      <span class="me-pull-right me-article-count">
	    	<i class="me-icon-comment"></i>&nbsp;赞同 {{ upvotes }}
	    </span>
      <span class="me-pull-right me-article-count">
	    	<i class="bk-icon"></i>&nbsp;反对 {{ downvotes }}
	    </span>
    </div>

    <div class="me-artile-description" style="text-align: left;">
      {{ content }}
    </div>
    <div class="me-article-footer">
	  	<span class="me-article-author">
	    	<i class="me-icon-author"></i>&nbsp;作者：{{ username }}
	    </span>
      <!--      多个标签，但这里只有一个-->
      <!--      <bk-tag v-for="t in tags" :key="t.tag" size="mini" type="success">{{t.tag}}</bk-tag>-->
      <bk-tag type="success">{{ tag }}</bk-tag>
      <span class="me-pull-right me-article-count">
	    	<i class="bk-timeline-icon"></i>&nbsp;时间：{{ formatDate(create_time) }}
	    </span>

    </div>
  </bk-card>
</template>

<script>
import {bkCard, bkButton, bkTag} from 'bk-magic-vue'
import {formatTime} from "../../api/time";

export default {
  name: 'ArticleItem',
  components: [
    bkCard,
    bkButton,
    bkTag
  ],
  props: {
    id: String,
    weight: Number,
    title: String,
    upvotes: Number,
    downvotes: Number,
    content: String,
    username: String,
    tag: String,
    create_time: String
  },
  data() {
    return {}
  },
  methods: {
    articleView(id) {
      console.log(id)
      this.$router.push(`/articleView/${id}`)
    },
    /*数据库时间变为年月日时间*/
    formatDate(dateString) {
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');
      return `${year}-${month}-${day}`;
    }
  }
}
</script>

<style scoped>

.me-article-header {
  /*padding: 10px 18px;*/
  padding-bottom: 10px;
}

.me-article-title {
  font-weight: 600;
}

.me-article-icon {
  padding: 3px 8px;
}

.me-article-count {
  color: #a6a6a6;
  padding-left: 14px;
  font-size: 13px;
}

.me-pull-right {
  float: right;
}

.me-artile-description {
  font-size: 15px;
  line-height: 20px;
  margin-bottom: 12px;
}

.me-article-author {
  color: #a6a6a6;
  padding-right: 18px;
  font-size: 13px;
}

.bk-tag {
  margin-left: 6px;
}

</style>
