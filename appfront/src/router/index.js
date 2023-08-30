import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

export default new Router({
  routes: [
    // {
    //   path: '/',
    //   name: 'HelloWorld',
    //   component: HelloWorld
    // }
    {
      path: '/', // 公有模板页
      name: 'index',
      component: () => import('../components/index.vue'),
      children: [
        {
          path: '/tag',
          name: 'index.tag',
          component: () => import('../components/tag.vue')
        },
        {
          path: '/first',
          name: 'index.first',
          component: () => import('../components/first.vue')
        },
        {
          path: '/BaseHeader',
          name: 'index.BaseHeader',
          component: () => import('../components/BaseHeader.vue')
        },
        {
          path: '/top', // 要跟在父路径的路径后，/father/child
          name: 'index.top', // 名称也是
          component: () => import('../components/top.vue')
        },
        {
          path: '/college',
          name: 'index.college',
          component: () => import('../components/college.vue')
        },
        {
          path: '/major',
          name: 'index.major',
          component: () => import('../components/major.vue')
        },
        {
          path: '/student',
          name: 'index.student',
          component: () => import('../components/student.vue')
        },
        {
          path: '/ArticleScrollPage',
          name: 'index.ArticleScrollPage',
          component: () => import('../components/ArticleScrollPage.vue')
        },
        {
          path: '/top_question',
          name: 'index.top_question',
          component: () => import('../components/top_question.vue')
        },
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../components/login/login.vue')
      // component: login
    }
  ]
})
