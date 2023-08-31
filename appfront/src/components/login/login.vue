<template>
  <div id='logintwo'>
    <div class='avue-home' v-if='loading' style='z-index: 99;'>
      <div class='avue-home__main'>
        <img class='avue-home__loading' src='../../assets/loading-spin.svg' alt='loading'>
        <div class='avue-home__title'>
          GDUT龙洞小助手努力加载中...
        </div>
      </div>
    </div>

    <div style='display: flex;width: 100%;height: 100%;overflow: hidden;'>
      <div v-show='page==="login"' class='login-modal' id='loginDiv'>
        <form>
          <h1 style='text-align: center;color: aliceblue;'>WELCOME TO GDUT</h1>
          <p>账 号: <input id='username' v-model="username" type='text'>
            <span v-bk-tooltips.top-start="'用户账号或邮箱'" class='top-start'>
                <i class='bk-icon icon-info-circle-shape'></i>
            </span>
          </p>
          <p>密 码: <input id='password' v-model="password" type='password'>
            <span v-bk-tooltips.top-start="'忘记密码请找管理员'" class='top-start'>
                <i class='bk-icon icon-info-circle-shape'></i>
            </span>
          </p>
          <p>
            <label id="rememberMeLabel">
              <input id="rememberMe" v-model="rememberMe" type="checkbox"> 记住密码
            </label>
          </p>
          <div style='text-align: center;margin-top: 35px;'>
            <input type='submit' class='button' value='Login up' @click.prevent='handleSubmit'>
            <input type='reset' class='button' value='Reset'>
            <input type='submit' class='button' value='Register' @click.prevent='register'>
          </div>
        </form>
      </div>
      <div v-show='page==="register"' class='login-modal' id='loginDiv2'>
        <form>
          <h1 style='text-align: center;color: aliceblue;'> WELCOME TO GDUT</h1>
          <p> 账 号: <input id='username2' v-model="username" type='text'></p>
          <p> 密 码: <input id='password2' v-model="password" type='password'></p>
          <p>重输密码: <input id='password22' v-model="password2" type='password'></p>
          <p> 邮 箱: <input id='email' v-model="email" type='text'></p>
          <p><label>验证码:</label>
            <input type="text" v-model="sms_code" @blur="check_sms_code" name="msg_code" id="msg_code"
                   class="msg_input">
            <bk-button ext-cls="mr5" @click="send_sms_code" theme="primary" title="提交" class="get_msg_code">
              {{ sms_code_tip }}
            </bk-button>
          </p>

          <div style='text-align: center;margin-top: 35px;'>
            <input type='submit' class='button' value='Register' @click.prevent='trueRegister'>
            <input type='reset' class='button' value='Reset'>
            <input type='submit' class='button' value='Back login' @click.prevent='backLogin'>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script>
import {bkInput} from 'bk-magic-vue'
import axios from 'axios'
import {host} from '../../../static/js/host'

export default {
  components: {
    bkInput
  },
  name: 'login',
  data() {
    return {
      page: 'login',
      loading: true,
      passwordType: 'password',
      sms_code_tip: '获取邮箱验证码',
      password2: '', // 重输密码
      email: '', // 邮箱
      sms_code: '', // 短信验证码
      send_flag: true, // 用于标志允许用户发送验证码
      check_unique_username_res: false,
      check_unique_email_res: false,
      check_send_code_res: false,
      loginForm: {
        username: '', // 用户名
        password: '', // 密码
        rememberMe: false,  // 记住密码
      }
    }
  },
  mounted() {
    let that = this
    setTimeout(function () {
      that.loading = false
    }, 500)
    if (localStorage.rememberMe !== 'true') {
      localStorage.clear()
    } else {
      this.username = localStorage.username;
      this.password = localStorage.password;
      this.rememberMe = true;
    }
  },
  methods: {
    check_error_username() {
      // console.log(this.username.length)
      return !this.username || !(this.username.length < 20)
    },
    handleSubmit() {
      if (this.check_error_username()) {
        this.warningInfoBox('请输入不超过20位的用户名')
      } else if (!this.password) {
        this.warningInfoBox('请输入密码')
      } else {
        axios.post(host + '/api/v1/user/login/', {username: this.username, password: this.password}, {
          responseType: 'json',
          withCredentials: true // 跨域情况可以携带cookie
        }).then(response => {
          this.successInfoBox('牛，登录成功了')
          // 记住登录
          sessionStorage.clear()
          localStorage.clear()
          // 记住密码
          if (this.rememberMe) {
            // 如果用户选择记住密码，将用户名和密码保存到localStorage
            localStorage.setItem("username", this.username);
            localStorage.setItem("password", this.password);
            localStorage.setItem("rememberMe", true);
          } else {
            // 如果用户取消记住密码，从localStorage中删除用户名和密码
            localStorage.removeItem("username");
            localStorage.removeItem("password");
            localStorage.removeItem("rememberMe");
          }
          localStorage.token = response.data.token
          localStorage.username = response.data.username
          this.$router.push('/top') // 根据index.js的路由跳转到top.vue
        }).catch(error => {
          if (error.response.status === 400) {
            this.errorInfoBox(error.response.data.message) // 展示发送短信错误提示
          } else {
            this.username = ''
            this.password = ''
            console.log(this.username)
            console.log(this.password)

            console.log(error.response.data)
            this.errorInfoBox('哦吼，登录失败！')
          }
        })
      }
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.page = 'login'
          this.$loading({
            lock: true,
            text: '登录中,请稍后。。。',
            spinner: 'el-icon-loading'
          })
        }
      })
    },
    register() {
      this.username = ''
      this.password = ''
      this.page = 'register'
    },
    backLogin() {
      this.username = ''
      this.password = ''
      this.page = 'login'
    },
    check_sms_code() {
      return !this.sms_code
    },
    send_sms_code() {
      if (this.send_flag && this.check_before_email()) {
        this.send_flag = false // 60s后才允许再次发送
        // console.logs(host + '/email_codes/' + this.email + '/')
        axios.get(host + '/api/v1/users/email_send/', {responseType: 'json', params: {email: this.email}})
          .then(response => {
            var num = 60 // 倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
            // 设置一个计时器
            var t = setInterval(() => {
              if (num === 1) { // 如果计时器到最后, 清除计时器对象
                clearInterval(t)
                this.sms_code_tip = '获取短信验证码' // 将点击获取验证码的按钮展示的文本回复成原始文本
                this.send_flag = true // 将点击按钮的onclick事件函数恢复回去
              } else {
                num -= 1
                this.sms_code_tip = num + '秒' // 展示倒计时信息
              }
            }, 1000, 60)
          }).catch(error => {
          if (error.response.status === 400) {
            this.errorInfoBox(error.response.data.message) // 展示发送短信错误提示
          } else {
            console.log(error.response.data)
          }
          this.send_flag = true
        })
      }
    },
    check_before_email() {
      if (this.check_error_username()) {
        this.warningInfoBox('请输入不超过20位的账号')
        return false
      } else if (!this.password || this.password.length < 6) {
        this.warningInfoBox('请输入密码且密码大于等于6位')
        return false
      } else if (this.password !== this.password2) {
        this.warningInfoBox('请确保两次密码输入相同')
        return false
      } else if (!(/^\w+@\w+\.\w+$/i.test(this.email))) {
        this.warningInfoBox('请确保输入的email格式正确')
        return false
      } else {
        return true
      }
    },
    check_send_code() { // 验证码校验
      if (this.sms_code === '' || this.sms_code.length !== 6) {
        this.warningInfoBox('验证码错误')
        return
      }
      axios.get(host + '/api/v1/users/email_verify/', {
        responseType: 'json',
        params: {sms_code: this.sms_code, email: this.email}
      })
        .then(response => {
          this.check_send_code_res = true
          this.successInfoBox('验证码正确√')
        })
        .catch(error => {
          if (error.response.status === 400) {
            this.errorInfoBox(error.response.data.message) // 展示发送短信错误提示
          } else {
            console.log(error.response.data)
          }
          this.check_send_code_res = false
        })
    },
    check_unique_username() { // 账号是否注册过
      axios.get(host + '/api/v1/user/unique/', {
        responseType: 'json',
        params: {username: this.username, str: 'username'}
      })
        .then(response => {
          if (response.data.count > 0) {
            this.errorInfoBox('账号已注册过')
            this.check_unique_username_res = false
          } else {
            console.log('账号unique')
            this.check_unique_username_res = true
          }
        }).catch(error => {
        console.log(error.response.data)
        this.check_unique_username_res = false
      })
    },
    check_unique_email() { // 邮箱是否唯一
      axios.get(host + '/api/v1/user/unique/', {
        responseType: 'json',
        params: {email: this.email, str: 'email'}
      })
        .then(response => {
          if (response.data.count > 0) {
            this.errorInfoBox('邮箱已注册过')
            this.check_unique_email_res = false
          } else {
            console.log('邮箱unique')
            this.check_unique_email_res = true
          }
        }).catch(error => {
        console.log(error.response.data)
        this.check_unique_email_res = false
      })
    },
    trueRegister() { // 注册
      if (this.check_before_email()) { // 填了前面的信息，后面的邮箱验证码校验才有意义
        this.check_unique_username()
        this.check_unique_email()
        this.check_send_code()

        console.log(this.check_unique_username_res)
        console.log(this.check_unique_email_res)
        console.log(this.check_send_code_res)

        if (this.check_unique_username_res && this.check_unique_email_res && this.check_send_code_res) {
          axios.post(host + '/api/v1/user/register/', {
            username: this.username,
            password: this.password,
            password2: this.password2,
            email: this.email
          }, {responseType: 'json'})
            .then(response => {
              this.successInfoBox('注册正确')
              // 记录用户的登录状态
              sessionStorage.clear()
              localStorage.clear()
              localStorage.token = response.data.token
              localStorage.username = response.data.username
              localStorage.user_id = response.data.id
              this.$router.push('/top') // 根据index.js的路由跳转到top.vue
            })
            .catch(error => {
              if (error.response.status === 400) {
                this.warningInfoBox('数据错误')
              } else {
                console.log(error.response.data)
              }
            })
        }
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
    errorInfoBox(msg) {
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
  }
}
</script>

<style scoped>
#loginDiv {
  width: 40%;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 45%;
  background-color: rgba(75, 81, 95, 0.3);
  box-shadow: 7px 7px 17px rgba(52, 56, 66, 0.5);
  border-radius: 10px;
}

#loginDiv2 {
  width: 40%;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70%;
  background-color: rgba(75, 81, 95, 0.3);
  box-shadow: 7px 7px 17px rgba(52, 56, 66, 0.5);
  border-radius: 10px;
}

p {
  margin-top: 50px;
  margin-left: 50px;
  color: #e85404;
  font-size: 18px;
  font-weight: bold;
}

input {
  margin-left: 20px;
  border-radius: 12px;
  border-style: hidden;
  height: 40px;
  width: 300px;
  background-color: rgba(210, 183, 210, 0.5);
  outline: none;
  color: #3f4eee;
  padding-left: 5px;
}

.button {
  border-color: cornsilk;
  background-color: rgba(100, 149, 237, .7);
  color: aliceblue;
  border-style: hidden;
  border-radius: 5px;
  width: 100px;
  height: 31px;
  font-size: 16px;
}

#logintwo {
  width: 100%;
  height: 100%;
  background-size: 100% 100%;
  background-image: url('../../assets/gdutDragon.jpg');
  background-repeat: no-repeat;
  background-position: center center;
  overflow: auto;
  position: fixed;
  line-height: 100%;
}

.logo img {
  width: 32px;
  height: 32px;
  margin: 14px 10px 0 15px;
}

.avue-home {
  /*background-color: #303133;*/
  background-color: rgba(39, 51, 59, 1.0);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.avue-home__main {
  user-select: none;
  width: 100%;
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.avue-home__footer > a {
  font-size: 12px;
  color: #ABABAB;
  text-decoration: none;
}

.avue-home__loading {
  height: 32px;
  width: 32px;
  margin-bottom: 20px;
}

.avue-home__title {
  color: #FFF;
  font-size: 14px;
  margin-bottom: 10px;
}

::-webkit-scrollbar {
  width: 7px;
  height: 7px;
  display: none;
  background-color: transparent;
}

::-webkit-scrollbar-thumb {
  border-radius: 5px;
  background-color: rgba(39, 51, 59, 1.0);

}

::-webkit-scrollbar-track-piece {
  background-color: transparent;
}

a {
  color: #FFFFFF;
  text-decoration: none;
}

.login-modal {
  position: relative;
  width: 420px;
  height: 450px;
  margin: 0 auto;
  top: 50%;
  margin-top: -225px;
  background-color: #FFFFFF;
  border-radius: 5px;
}

/*确认按钮选项*/
/* 隐藏默认的复选框 */
#rememberMe {
  appearance: none;
  background-color: #efe4e4;
  border: 4px solid #490202;
  width: 18px;
  height: 18px;
  cursor: pointer;
  position: relative;
  margin-left: 10px;
}

/* 自定义复选框勾选状态 */
#rememberMe:checked {
  background-color: #afe79c;
  border: 3px solid #340303;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='black' width='18px' height='18px'%3E%3Cpath d='M0 0h24v24H0z' fill='none'/%3E%3Cpath d='M9 16.2l-3.5-3.5a.984.984 0 0 0-1.4 0 .984.984 0 0 0 0 1.4l4.19 4.19c.37.37 1.02.37 1.39 0L20.3 7.7a.984.984 0 0 0 0-1.4.984.984 0 0 0-1.4 0L9 16.2z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
}
</style>
