<template>
  <bk-card>
    <h1 class="me-author-name">相关文章</h1>
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
      token: localStorage.token || sessionStorage.token
    }
  },
  methods: {}
}
</script>

<style scoped>
.me-author-name {
  text-align: center;
  font-size: 20px;
  border-bottom: 1px solid #5FB878;
}
</style>
