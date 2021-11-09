const router = new VueRouter({
  mode: 'history',
  base: '/article/',
  routes: [
    {
      path: '/:name',
      name: 'Article',
      component: ArticleView
    }
  ]
})
