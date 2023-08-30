<template>
  <bk-header class="me-area">
    <bk-row class="me-header">

      <bk-col :span="4" class="me-header-left">
        <router-link to="/" class="me-title">
          <img src="../assets/gdut_img.png" />
        </router-link>
      </bk-col>

      <bk-col v-if="!simple" :span="16">
        <bk-menu :router=true menu-trigger="click" active-text-color="#5FB878" :default-active="activeIndex"
                 mode="horizontal">
          <bk-menu-item index="/">首页</bk-menu-item>
          <bk-menu-item index="/category/all">文章分类</bk-menu-item>
          <bk-menu-item index="/tag/all">标签</bk-menu-item>
          <bk-col :span="4" :offset="4">
            <bk-menu-item index="/write"><i class="bk-icon-edit"></i>写文章</bk-menu-item>
          </bk-col>

        </bk-menu>
      </bk-col>

    </bk-row>
  </bk-header>
</template>

<script>
import {bkHeader, bkCol, bkRow, bkMenu, bkSubmenu, bkMenuItem} from 'bk-magic-vue'
  export default {
    name: 'BaseHeader',
    components: {
      bkHeader, bkCol, bkRow, bkMenu, bkSubmenu, bkMenuItem
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

  .bk-header {
    position: fixed;
    z-index: 1024;
    min-width: 100%;
    box-shadow: 0 2px 3px hsla(0, 0%, 7%, .1), 0 0 0 1px hsla(0, 0%, 7%, .1);
  }

  .me-title {
    margin-top: 10px;
    font-size: 24px;
  }

  .me-header-left {
    margin-top: 10px;
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
