import {router} from './router/index.js';
import {SymbolDrawer} from './components/SymbolDrawer.js';

new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  router,
  components: {'symbol-drawer': SymbolDrawer},
  data: () => ({
    drawer: true,
    drawerWidth: 256,
    disableResizeWatcher: false,
    menuButton: true,
  }),
  delimiters: ['$(', ')'],
});
