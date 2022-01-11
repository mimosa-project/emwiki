import {router} from './router/index.js';
import {SymbolDrawer} from './components/SymbolDrawer.js';
import {Splitter} from '../../js/Splitter.js';

new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  router,
  components: {
    'symbol-drawer': SymbolDrawer,
    'splitter': Splitter,
  },
  data: () => ({
    drawer: true,
    drawerWidth: 256,
    disableResizeWatcher: false,
    menuButton: true,
  }),
  delimiters: ['$(', ')'],
});
