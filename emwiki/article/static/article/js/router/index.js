// eslint-disable-next-line no-var
var context = JSON.parse(document.getElementById('context').textContent);
// eslint-disable-next-line no-unused-vars
const router = new VueRouter({
  mode: 'history',
  base: context['article_base_uri'],
  routes: [
    {
      path: '/:name',
      name: 'Article',
      component: ArticleView,
    },
  ],
});
