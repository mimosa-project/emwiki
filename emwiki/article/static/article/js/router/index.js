var context = JSON.parse(document.getElementById('context').textContent);
const router = new VueRouter({
  mode: 'history',
  base: context['article_base_uri'],
  routes: [
    {
      path: '/:name',
      name: 'Article',
      component: ArticleView
    }
  ]
})
