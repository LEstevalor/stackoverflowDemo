import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

const router = new Router({
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
          path: '/setting',
          name: 'index.setting',
          component: () => import('../components/setting.vue')
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
        {
          path: '/articleView/:id', // 跳转id可外键传入
          name: 'index.articleView', // 添加一个名称，例如 'view'
          component: () => import('../components/blog/articleView.vue')
        },
        {
          path: '/write/:id?',
          name: 'index.BlogWrite',
          component: () => import('../components/blog/BlogWrite.vue')
        },
        {
          path: '/tag/:id?',
          name: 'index.BlogCategoryTag',
          component: () => import('../components/blog/BlogCategoryTag.vue')
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
});

function isTokenExpired(token) {
  // 判断token是否过期
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return Date.now() >= payload.exp * 1000;
  } catch (error) {
    return true;
  }
}

router.beforeEach((to, from, next) => {
  // 检查用户是否已登录
  const token = localStorage.getItem('token');
  const isLoggedIn = !!token && !isTokenExpired(token);
  // 如果用户未登录且试图访问非登录页面，则重定向到登录页面
  if (!isLoggedIn && to.path !== '/login') {
    next('/login');
  } else {
    next();
  }
});

export default router;
