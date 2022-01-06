import {router} from './router/index.js';
import {ArticleDrawer} from './components/ArticleDrawer.js';
import {TheoremDrawer} from './components/TheoremDrawer.js';
import {context} from '../../js/context.js';
import {splitter} from '../../js/splitter.js';

new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  router,
  components: {
    'article-drawer': ArticleDrawer,
    'theorem-drawer': TheoremDrawer,
    'splitter': splitter,
  },
  data: () => ({
    drawer: true,
    drawerWidth: 256,
    disableResizeWatcher: false,
    menuButton: true,
  }),
  created() {
    if (context['target'] === 'theorem') {
      this.drawerWidth = 512;
      this.disableResizeWatcher = true;
    }
  },
  delimiters: ['$(', ')'],
});
