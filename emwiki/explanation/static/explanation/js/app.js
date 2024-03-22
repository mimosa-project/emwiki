import {Splitter} from '../../js/Splitter.js';
import {ExplanationDrawer} from './components/ExplanationDrawer.js';
import {router} from './router/index.js';
import {createExplanation} from './views/createExplanation.js';


new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  router,
  components: {
    'explanation-drawer': ExplanationDrawer,
    'create-explanation': createExplanation,
    'splitter': Splitter,
  },
  data: () => ({
    drawerExists: true,
    drawerWidth: 256,
    disableResizeWatcher: false,
    menuButton: true,
  }),
  delimiters: ['$(', ')'],
});

