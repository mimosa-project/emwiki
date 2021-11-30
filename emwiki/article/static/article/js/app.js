new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  router,
  components: {
    'article-drawer': ArticleDrawer,
    'theorem-drawer': TheoremDrawer,
  },
  data: () => ({
    drawer: true,
    drawerWidth: 256,
    stateless: false,
    MenuButton: true,
  }),
  mounted() {
    if (context['target'] === 'theorem') {
      this.drawerWidth = 512;
      this.stateless = true;
    }
  },
  delimiters: ['$(', ')'],
});
