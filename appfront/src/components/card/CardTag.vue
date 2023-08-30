<template>
  <bk-card :body-style="{ padding: '8px 18px' }">
    <div slot="header" class="me-tag-header">
      <span>最热标签</span>
      <a @click="moreTags" class="me-pull-right me-tag-more">查看全部</a>
    </div>

    <ul class="me-tag-list">
      <li class="me-tag-item" v-for="t in tags" :key="t.id">
        <!--type="primary"-->
        <bk-button class="custom-button" @click="tag(t.id)" size="mini" type="primary" round plain>{{ t.tag }}
        </bk-button>
      </li>
    </ul>
  </bk-card>

</template>

<script>
import {bkCard, bkButton} from 'bk-magic-vue'

export default {
  name: 'CardTag',
  components: {
    bkCard,
    bkButton
  },
  props: {
    tags: Array
  },
  data() {
    return {}
  },
  methods: {
    moreTags() {
      this.$router.push('/tag')
    },
    tag(id) {
      this.$router.push({path: `/tag/${id}`})
    }
  }
}
</script>

<style scoped>

.me-tag-header {
  font-weight: 600;
}

.me-tag-more {
  font-size: 14px;
  color: #78b6f7;
}

.me-tag-list {
  list-style-type: none;
}

.me-tag-item {
  display: inline-block;
  padding: 4px;
  font-size: 14px;
  color: #5FB878;
}

.me-tag-item a:hover {
  text-decoration: underline;
}

/* 按钮优化化，绑定class="custom-button" */
.custom-button {
  background-image: linear-gradient(135deg, #a6c0fe 0%, #f68084 100%);
  border: none;
  border-radius: 50px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  color: rgba(47, 79, 79, 0.8);
  font-size: 20px;
  padding: 20px 50px;
  text-decoration: none;
  min-width: 60px;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
}

.custom-button:hover {
  background-image: linear-gradient(135deg, #f68084 0%, #a6c0fe 100%);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
  color: rgba(47, 79, 79, 1);
  cursor: pointer;
  transform: translateY(-2px);
}

.custom-button:focus {
  outline: none;
}
</style>
