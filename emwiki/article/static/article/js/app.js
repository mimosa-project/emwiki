new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  router,
  components: {'article-drawer': ArticleDrawer},
  data: () => ({
    drawer: true,
  }),
  delimiters: ['$(', ')'],
});
