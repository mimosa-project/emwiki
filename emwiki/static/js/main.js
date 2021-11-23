new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: () => ({
    drawer: false,
    drawerWidth: 256,
  }),
  delimiters: ['$(', ')'],
});
