<template>
  <bk-header class="me-area">
    <link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <bk-row class="me-header">
      <bk-col :span="16" class="me-header-left">
        <router-link to="/tag" class="me-title">
          <i class="fas fa-tags"></i> 标签
        </router-link>
      </bk-col>
    </bk-row>
    <BlogWrite></BlogWrite>
  </bk-header>
</template>

<script>
import {bkHeader, bkCol, bkRow, bkMenu, bkSubmenu, bkMenuItem} from 'bk-magic-vue'
import BlogWrite from "./blog/BlogWrite";

export default {
  name: 'BaseHeader',
  components: {
    bkHeader, bkCol, bkRow, bkMenu, bkSubmenu, bkMenuItem,
    BlogWrite
  },
  props: {
    activeIndex: String,
    simple: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {}
  },
  computed: {
    user() {
      let avatar = this.$store.state.avatar
      return {
        login, avatar
      }
    }
  },
  methods: {
    logout() {
      let that = this
      this.$store.dispatch('logout').then(() => {
        this.$router.push({path: '/'})
      }).catch((error) => {
        if (error !== 'error') {
          that.$message({message: error, type: 'error', showClose: true});
        }
      })
    }
  }
}
</script>

<style>
body {
  font-family: 'Roboto', sans-serif;
}

.me-header {
  padding: 10px 0;
  position: fixed;
  z-index: 1024;
  min-width: 100%;
  box-shadow: 0 2px 3px hsla(0, 0%, 7%, .1), 0 0 0 1px hsla(0, 0%, 7%, .1);
}

.me-title {
  margin-top: 20px;
  font-size: 25px;
  transition: all 0.3s ease;
}

.me-title:hover {
  transform: translateY(-5px);
}

.me-header-left {
  margin-top: 25px;
}

.me-title img {
  max-height: 2.4rem;
  max-width: 100%;
}

.me-header-picture {
  width: 36px;
  height: 36px;
  border: 1px solid #ddd;
  border-radius: 50%;
  vertical-align: middle;
  background-color: #5fb878;
}
</style>
