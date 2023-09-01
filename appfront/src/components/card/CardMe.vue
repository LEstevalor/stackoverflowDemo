<template>
  <bk-card>
    <h1 class="me-author-name">科技文海</h1>
    <div class="me-author-description">
      <span><i class="el-icon-location-outline"></i> &nbsp;地球村</span>
      <span><i class="me-icon-job"></i> &nbsp;专业SE</span>
      <span><i class="me-icon-job"></i> &nbsp;作者：LEstevalor</span>
    </div>
  </bk-card>
</template>

<script>
import {bkCard} from 'bk-magic-vue'

export default {
  name: 'CardMe',
  components: {
    bkCard
  },
  data() {
    return {
      token: localStorage.token || sessionStorage.token,
      qq: {title: 'QQ', message: '2534891955'},
    }
  },
  methods: {}
}
</script>

<style scoped>
.me-author-name {
  margin-top: 0.1px;
  text-align: center;
  font-size: 25px;
  border-bottom: 1px solid #5FB878;
}

.me-author-description {
  padding: 8px 0;
}

.me-icon-job {
  padding-left: 16px;
}
</style>
