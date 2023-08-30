<template>
  <div class="search-container">
    <h1 class="title">Question Search</h1>
    <div class="search-input">
      <bk-input
        v-model="searchQuery"
        placeholder="Search for questions..."
        clearable
      ></bk-input>
      <bk-button
        theme="primary"
        icon="bk-icon icon-search"
        @click="searchQuestions"
      ></bk-button>
    </div>
    <bk-table style="margin-top: 15px;"
              :data="page_data"
              :pagination="pagination"
              @page-change="handlePageChange"
              @page-limit-change="handlePageLimitChange">
      <bk-table-column prop="title" label="Question"></bk-table-column>
      <bk-table-column prop="username" label="User"></bk-table-column>
      <bk-table-column prop="update_time" label="UpdateTime"></bk-table-column>
      <bk-table-column prop="tag" label="Tag"></bk-table-column>
      <bk-table-column prop="upvotes" label="Upvote"></bk-table-column>
      <bk-table-column prop="downvotes" label="Downvote"></bk-table-column>
    </bk-table>
  </div>
</template>

<script>
import {bkTable, bkTableColumn, bkButton, bkInput} from 'bk-magic-vue'
import axios from "axios";
import {host} from "../../static/js/host";

export default {
  name: "top_question",
  components: {
    bkTable, bkTableColumn, bkButton, bkInput
  },
  data() {
    this.token = localStorage.token || sessionStorage.token
    return {
      searchQuery: "",
      data: [
        {title: "进程和线程的区别", tag: "OS", username: "北大学姐", update_time: "2023-08-02", upvotes: "10", downvotes: "1"},
        {title: "B+树实现机制", tag: "数据结构与算法", username: "浙大学长", update_time: "2023-08-30", upvotes: "8", downvotes: "2"},
      ],
      page_data: [],
      pagination: {
        current: 1, // 首页
        count: 0, // 总数
        limit: 10, // 限制
        limitList: [10]  // 限制用户选分页选项
      },
    };
  },
  methods: {
    searchQuestions() {
      axios.get(host + '/api/v1/questions/', { // 获取data列表中的数据
          headers: {
            'Authorization': 'Bearer ' + this.token
          },
          responseType: 'json'
        }).then(response => {
          this.data = response.data.results // 列表的数据和data是绑一起的
          this.pagination.count = this.data.length
          this.getPageData()
        })
          .catch(error => {
            console.log(error.response.data)
          })
    },
    // 以下连续三个用于分页的函数
    getPageData() { // 分页操作显示列表
      this.page_data = []
      let start = (this.pagination.current - 1) * this.pagination.limit
      console.log(start)
      console.log(this.pagination.current * this.pagination.limit)
      console.log(this.pagination.count)
      for (let i = start; i < this.pagination.current * this.pagination.limit && i < this.pagination.count; i++) {
        this.page_data.push(this.data[i]);
      }
    },
    handlePageChange(page) { // 回调当前页
      this.pagination.current = page
      this.getPageData()
      // console.logs(this.pagination.current)
    },
    handlePageLimitChange() { // 当用户切换表格每页显示条数时会出发的事件
      console.log('handlePageLimitChange', arguments)
      this.pagination.limit = arguments[0]
      this.getPageData()
    },
  },
}
</script>

<style scoped>
.search-container {
  max-width: 1500px;
  margin: 0 auto;
  padding: 2rem;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  background-image: url("../assets/star2.gif");
}

.title {
  font-family: "Pacifico", cursive;
  font-size: 2rem;
  text-align: center;
  color: #5c6bc0;
  margin-bottom: 1rem;
}

.search-input {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1rem;
}

.bk-input {
  width: 100%;
  max-width: 600px;
  margin-right: 1rem;
}
</style>