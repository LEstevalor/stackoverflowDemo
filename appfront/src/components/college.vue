<template>
  <div class="page-container" >
     <bk-compose-form-item class="select-demo">
       <div>&nbsp;</div>
        <bk-select class="bk-select-custom" v-model="value1" style="width: 140px" size="large" :clearable="false">
          <bk-option id="tag" name="标签" @click="option_tag"></bk-option>
        </bk-select>
        <bk-input class="bk-input-custom"  style="width: 400px" size="large" v-model=textcontent
                  v-if="value1 === 'tag'" key:1 placeholder="please search label information" :left-icon="'bk-icon icon-search'"></bk-input>
      <bk-button class="search-button" type="search" theme="warning" @click="search_data" size="large">search</bk-button>
     </bk-compose-form-item>
     <div style="float:right;" class="container">
      <div>&nbsp;</div>
      <bk-button class="style-button" theme="primary" @click="toggleTableSize">样式设置</bk-button>
      <span class="ml10">当前尺寸：{{ size }} &nbsp;&nbsp;&nbsp;</span>
      <div>&nbsp;</div>
      <!-- 添加标签 -->
      <div class="inner">
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <bk-popconfirm class="popconfirm"trigger="click" :ext-cls="'asadsadsads'" width="288" @confirm="addData()">
          <div slot="content">
              <bk-compose-form-item>
                <h3>标签: <bk-input v-model="create_tag" type='text'/></h3>
              </bk-compose-form-item>
          </div>
          <bk-button class="add-button" theme="primary" :disabled="status === 'USER'">添加</bk-button>
        </bk-popconfirm>
      </div>
      &nbsp;
    </div>
    <div style="float:left;">
      <div>&nbsp;</div>
      <div>&nbsp;</div>
      <div>&nbsp;</div>
      <div>&nbsp;</div>
      &nbsp;<bk-icon type="upload" />&nbsp;<bk-button theme="success" @click="load_excel()"> 数据导出</bk-button>
    </div>
    <bk-table style="margin-top: 15px;"
              class="table-bk"
        :data="page_data"
        :size="size"
        :pagination="pagination"
        @page-change="handlePageChange"
        @page-limit-change="handlePageLimitChange"
        @select="curSelected"
        @select-all="curAllSelected">
      <bk-table-column type="selection" width="60"></bk-table-column>  <!--可选的地方-->
      <bk-table-column type="index" label="序列" width="60"></bk-table-column>
      <bk-table-column label="标签" prop="tag"></bk-table-column>
      <!--  sortable属性赋予bk-table-column排序的能力   -->
      <bk-table-column label="贴数" prop="count" sortable></bk-table-column>
      <bk-table-column label="操作" width="150">
        <template slot-scope="props">
          <bk-popover class="dot-menu" placement="bottom-start" theme="dot-menu light"
                      :trigger="props.$index % 2 === 0 ? 'click' : 'mouseenter'" :arrow="false" offset="15"
                      :distance="0">
            <span class="dot-menu-trigger"></span>
          </bk-popover>
        </template>
      </bk-table-column>
    </bk-table>
  </div>
</template>

<script>
import {bkTable, bkTableColumn, bkButton, bkPopover, bkComposeFormItem, bkInput, bkSelect, bkOption, bkColorPicker,
  bkIcon, bkPopconfirm} from 'bk-magic-vue'
import axios from 'axios'
import {host} from '../../static/js/host'

export default {
  name: 'college',
  components: {
    bkTable,
    bkTableColumn,
    bkButton,
    bkPopover,
    bkComposeFormItem,
    bkInput,
    bkSelect,
    bkOption,
    bkColorPicker,
    bkIcon,
    bkPopconfirm
  },
  data () {
    this.token = localStorage.token || sessionStorage.token
    return {
      textcontent: '', // 搜索框输入内容
      size: 'small',
      data: [
        {
          tag: '数学与统计学院',
          id: 1
        },
        {
          tag: '管理学院',
          id: 2
        }
      ],
      pagination: {
        current: 1, // 首页
        count: 0, // 总数
        limit: 10 // 限制
      },
      page_data: [],
      value1: 'tag',
      token: localStorage.token || sessionStorage.token,
      username: localStorage.username || sessionStorage.username,
      status: sessionStorage.status,
      create_tag: '',
      cur_getData: true,
      select_list: [], // 判断是否被选中的列表，被点后全部实时更新
      select_list_all: false // 判断是否被全选
    }
  },
  mounted () {
    this.getData()
  },
  methods: {
    getData () {
      axios.get(host + '/api/v1/questions/list_tag_and_count/', { // 获取data列表中的数据
        headers: {
          'Authorization': 'Bearer ' + this.token
        },
        responseType: 'json',
        params: {num: 101}
      }).then(response => {
        console.log('信息' + response.data.results)
        this.data = response.data.results // 列表的数据和data是绑一起的
        this.pagination['count'] = this.data.length
        this.cur_getData = true
        this.getPageData()
      })
        .catch(error => {
          console.log(error.response.data)
        })
    },
    getPageData () { // 分页操作显示列表
      this.page_data = []
      let start = (this.pagination.current - 1) * this.pagination.limit
      for (let i = start; i < this.pagination.current * this.pagination.limit  && i < this.pagination.count; i++) {
          this.page_data.push(this.data[i]);
      }
    },
    addData () {
      // 添加数据
      if (this.create_tag) {
        axios.post(host + '/api/v1/questions/add_tag/', JSON.parse(JSON.stringify(
          {
            'tag': this.create_tag
          })), {
          headers: {
            'Authorization': 'Bearer ' + this.token
          },
          responseType: 'json'
        }).then(response => {
          // console.logs(response.data)
          // console.logs(Number(response.data.id))
          this.data.push({
            'tag': this.create_tag,
            'id': Number(response.data.id)
          })
          this.handleSingle('标签 Tag', '添加标签成功', {theme: 'success'})
        }).catch(error => {
          alert(error.response.data.message)
          console.log(error.response.data.message)
        })
      } else {
        this.errorInfoBox('不能存在输入为空')
      }
    },
    search_data () { // 通过v-model绑定的textcontent获取文本内容，通过下滑框对应的value1获取下拉框选择的对象  搜索数据
      if (!this.textcontent) {
        this.handleSingle('欢迎使用GDUT DBA', '龙洞小助手提醒您搜索内容请有所输入，否则还是原信息', {theme: 'warning'})
        if (!this.cur_getData) {
          this.getData()
        }
      } else {
        let param = ''
        if (this.value1 === 'tag') {
          param = {tag: this.textcontent, num: 101}
        } else {
          alert('操作客户端变量被篡改的风险，请刷新页面')
        }

        axios.get(host + '/api/v1/questions/list_tag_and_count/', { // 获取data列表中的数据
          headers: {
            'Authorization': 'Bearer ' + this.token
          },
          responseType: 'json',
          params: param
        }).then(response => {
          console.log('筛选的学院信息：' + response.data.results)
          this.data = response.data.results // 列表的数据和data是绑一起的
          this.pagination['count'] = this.data.length
          this.cur_getData = false
          this.getPageData()
        })
          .catch(error => {
            console.log(error.response.data)
          })
      }
    },
    load_excel () { // JSON格式
      if (!this.select_list_all && this.select_list == null) {
        return
      }
      this.to_excel(this.select_list_all ? this.data : this.select_list)
    },
    to_excel (data) { // 转化成excel
      let str = '<tr><td>序号</td><td>贴数</td><td>创建时间</td><td>更新时间</td><td>标签名称</td></tr>' // 列标题
      // 循环遍历，每行加入tr标签，每个单元格加td标签
      for (let i = 0; i < data.length; i++) {
        str += '<tr>'
        for (const key in data[i]) { // 增加' '为了不让表格显示科学计数法或者其他格式
          str += '<td>' + data[i][key] + ' ' + '</td>'
        }
        str += '</tr>'
      }
      const worksheet = 'Sheet1' // Worksheet名
      const uri = 'data:application/vnd.ms-excel;base64,'

      // 下载的表格模板数据
      const template = `<html xmlns:o="urn:schemas-microsoft-com:office:office"
      xmlns:x="urn:schemas-microsoft-com:office:excel"
      xmlns="http://www.w3.org/TR/REC-html40">
      <head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet>
      <x:Name>${worksheet}</x:Name>
      <x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet>
      </x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]-->
      </head><body><table>${str}</table></body></html>`
      // 下载模板
      window.location.href = uri + window.btoa(unescape(encodeURIComponent(template))) // +后是编码
    },
    option_tag () { // 根据下化框选择标签
      this.value1 = 'tag'
    },
    toggleTableSize () { // 调整尺寸函数
      const size = ['small', 'medium', 'large']
      const index = (size.indexOf(this.size) + 1) % 3
      this.size = size[index]
    },
    handlePageChange (page) { // 回调当前页
      this.pagination.current = page
      this.getPageData()
      // console.logs(this.pagination.current)
    },
    handlePageLimitChange () { // 当用户切换表格每页显示条数时会出发的事件
      console.log('handlePageLimitChange', arguments)
      this.pagination.limit = arguments[0]
      this.getPageData()
    },
    curSelected (selection, row) { // 根据文档提示的回调函数及对应参数，（selection, row）其中row就可以把选中行所有数据取出来，但我们这里只需要从data把值该位selected
      console.log(selection)
      this.select_list = []
      for (let i = 0; i < selection.length; i++) {
        this.select_list.add(selection[i])
      }
    },
    curAllSelected (selection) { // 点首栏的选择全部才会进入这里
      this.select_list = [] // 清空select_list_id，以防突然地不勾选或勾选
      this.select_list_all = selection.length > 0
    },
    errorInfoBox (msg) {
      const a = this.$bkInfo({
        type: 'error',
        title: 'Fail:' + msg,
        subTitle: '窗口2秒后关闭',
        showFooter: false
      })
      let num = 2
      let t = setInterval(() => {
        a.subTitle = `此窗口${--num}秒后关闭`
        if (num === 0) {
          clearInterval(t)
          a.close()
        }
      }, 1000)
    },
    handleSingle (title, message, msg) {
      msg.title = title
      msg.message = message
      msg.offsetY = 80
      msg.limitLine = 3
      this.$bkNotify(msg)
    }
  }
}
</script>

<style>
/*动态背景*/
.page-container {
  background-image: url("../assets/star2.gif");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center center;
}


/*首栏优化*/
.select-demo {
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: linear-gradient(135deg, #3a3a3a, #1c1c1c);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.bk-input-custom {
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  color: #ffffff;
}

.bk-input-custom .bk-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.bk-input-custom .bk-icon {
  color: #ffffff;
}

.search-button {
  margin-left: 15px;
  background-image: linear-gradient(135deg, #9c27b0, #f50057);
  color: #ffffff;
  border: none;
  transition: background-image 0.3s, transform 0.3s;
}

.search-button:hover {
  background-image: linear-gradient(135deg, #f50057, #9c27b0);
  transform: scale(1.1);
}

/*中栏优化*/
.container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.ml10 {
  color: #78b6f7;
}

.style-button {
  background-image: linear-gradient(135deg, #3a3a3a, #1c1c1c);
  border: none;
  color: #ffffff;
  transition: background-image 0.3s, transform 0.3s;
}

.style-button:hover {
  background-image: linear-gradient(135deg, #1c1c1c, #3a3a3a);
  transform: scale(1.1);
}

.table-bk {
  color: #0720c4;
  font-weight: bold; /*加粗*/
}


.add-button {
  margin-left: 15px;
  background-image: linear-gradient(135deg, #9c27b0, #f50057);
  color: #ffffff;
  border: none;
  transition: background-image 0.3s, transform 0.3s;
}

.add-button:hover {
  background-image: linear-gradient(135deg, #f50057, #9c27b0);
  transform: scale(1.1);
}


.dot-menu {
    display: inline-block;
    vertical-align: middle;
}
.dot-menu-trigger {
    display: block;
    width: 30px;
    height: 30px;
    line-height: 30px;
    border-radius: 50%;
    text-align: center;
    font-size: 0;
    color: #979BA5;
    cursor: pointer;
}
.dot-menu-trigger:hover {
    color: #3A84FF;
    background-color: #EBECF0;
}
.dot-menu-trigger:before {
    content: "";
    display: inline-block;
    width: 3px;
    height: 3px;
    border-radius: 50%;
    background-color: currentColor;
    box-shadow: 0 -4px 0 currentColor, 0 4px 0 currentColor;
}
.dot-menu-list .dot-menu-item {
    padding: 0 10px;
    font-size: 12px;
    line-height: 26px;
    cursor: pointer;
}
.dot-menu-list .dot-menu-item:hover {
    background-color: #eaf3ff;
    color: #3a84ff;
}

.inner {
  display: flex;
  align-items: center;
  justify-content: center;
}

.popconfirm {
  animation: fadeIn 0.4s;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
