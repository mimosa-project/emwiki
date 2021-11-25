new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  router,
  components: {'symbol-drawer': SymbolDrawer},
  data: () => ({
    drawer: true,
  }),
  delimiters: ['$(', ')'],
});
