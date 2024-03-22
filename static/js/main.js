new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: () => ({
    drawerExists: false,
    drawerWidth: 256,
    // disableResizeWatcher->true:画面サイズが変更されてもdrawerが自動的に開いたり閉じたりしない
    disableResizeWatcher: true,
    // drawerの表示・非表示を切り替えるボタンの有無
    menuButton: false,
  }),
  delimiters: ['$(', ')'],
});
