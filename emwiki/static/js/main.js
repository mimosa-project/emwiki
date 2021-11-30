new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: () => ({
    drawer: false,
    drawerWidth: 256,
    // stateless->true:drawerの表示・非表示を手動で管理. false:画面サイズに合わせて自動で表示・非表示が切り替わる.
    stateless: true,
    // drawerの表示・非表示を切り替えるボタンの有無
    MenuButton: false,
  }),
  delimiters: ['$(', ')'],
});
