import {router} from './router/index.js';
import {SymbolDrawer} from './components/SymbolDrawer.js';
import {splitter} from '../../js/splitter.js';

new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  router,
  components: {
    'symbol-drawer': SymbolDrawer,
    'splitter': splitter,
  },
  data: () => ({
    drawer: true,
    drawerWidth: 256,
    disableResizeWatcher: false,
    menuButton: true,
  }),
  delimiters: ['$(', ')'],
});
