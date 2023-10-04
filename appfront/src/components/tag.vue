<template>
  <div class="page-container">
    <bk-container class="me-allct-container">
      <bk-main>
        <div>
          <button class="tab-button" @click="selectedTab = '文章分类'">文章分类</button>
          <button class="tab-button" @click="selectedTab = '标签'">标签</button>
        </div>
        <div v-if="selectedTab === '文章分类'">
          <bk-tab-pane label="文章分类" name="category">
            <ul class="me-allct-items">
              <li v-for="c in tags" @click="view(c.id)" :key="c.id" class="me-allct-item">
                <div class="me-allct-content">
                  <a class="me-allct-info">
                    <h4 class="me-allct-name">{{ c.tag }}</h4>
                  </a>
                </div>
              </li>
            </ul>
          </bk-tab-pane>
        </div>
        <div v-if="selectedTab === '标签'">
          <bk-tab-pane label="标签" name="tag">
            <ul class="me-allct-items">
              <li v-for="t in tags" @click="view(t.id)" :key="t.id" class="me-allct-item">
                <div class="me-allct-content">
                  <a class="me-allct-info">
                    <h4 class="me-allct-name">{{ t.tag }}</h4>
                  </a>

                  <div class="me-allct-meta">
                    <span>{{ t.tag }}  类文章</span>
                  </div>
                </div>
              </li>
            </ul>
          </bk-tab-pane>
        </div>
      </bk-main>
    </bk-container>
  </div>
</template>

<script>
import {bkContainer, bkMain, bkTabs, bkTabPane} from 'bk-magic-vue'
import axios from 'axios'
import {host} from "../../static/js/host";

export default {
  name: 'tag',
  components: {
    bkMain,
    bkContainer,
    bkTabs,
    bkTabPane
  },
  created() {
    console.log(this.$route.params.type)
    // this.getCategorys()
    this.getTags()
  },
  mounted() {
    if (!this.token) {
      this.$router.push('/login')
    }
  },
  data() {
    return {
      selectedTab: '文章分类',
      token: localStorage.token || sessionStorage.token,
      categorys: [],
      tags: [],
      currentActiveName: 'tag'
    }
  },
  methods: {
    view(id) {
      this.$router.push({path: `/tag/${id}`})
    },
    getTags() {
      console.log("aaaaaaaaaaaaaaaaa")
      console.log(this.token)

      axios.get(host + '/api/v1/questions/list_tag/', { // 获取data列表中的数据
        headers: {
          'Authorization': 'Bearer ' + this.token
        },
        responseType: 'json'
      }).then(data => {
        this.tags = data.data.results
        console.log(data.data.results)
      }).catch(error => {
        if (error !== 'error') {
          this.$message({type: 'error', message: '标签加载失败', showClose: true})
        }
      })
    }
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
/*背景*/
.page-container {
  background-image: url("../assets/star5.gif");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center center;
}

.me-allct-container {
  width: 1000px;
}

.me-allct-items {
  padding-top: 2rem;
}

.me-allct-item {
  width: 25%;
  display: inline-block;
  margin-bottom: 2.4rem;
  padding: 0 .7rem;
  box-sizing: border-box;
}

.me-allct-content {
    display: inline-block;
    width: 100%;
    background-image: linear-gradient(to right, rgba(30, 213, 169, 0.8), rgba(1, 163, 164, 0.8)); /* 蓝绿色和深蓝色渐变背景 */
    border: none;
    transition: background-color .3s;
    text-align: center;
    padding: 1.5rem 0;
    font-family: 'Roboto', sans-serif;
    color: #ffffff;
}

.me-allct-content:hover {
    background-image: linear-gradient(to right, rgba(76, 209, 55, 1), rgba(72, 126, 176, 1)); /* 鼠标悬停时增加渐变背景的不透明度 */
}


.me-allct-info {
  cursor: pointer;
}

.me-allct-name {
  font-size: 21px;
  font-weight: 150;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-top: 4px;
}

.me-allct-meta {
  font-size: 12px;
  color: #4359a1;
}

.tab-button {
  background-image: linear-gradient(135deg, #6ec1e4 0%, #6f86d6 100%);
  border: none;
  border-radius: 60px;
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
  color: white;
  cursor: pointer;
  font-size: 25px;
  margin: 0 8px;
  padding: 8px 24px;
  text-align: center;
  text-decoration: none;
  transition: all 0.3s;
}

.tab-button:hover {
  background-image: linear-gradient(135deg, #6f86d6 0%, #6ec1e4 100%);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}
</style>
