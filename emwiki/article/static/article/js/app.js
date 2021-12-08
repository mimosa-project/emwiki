import {router} from './router/index.js';
import {ArticleDrawer} from './components/ArticleDrawer.js';
import {TheoremDrawer} from './components/TheoremDrawer.js';
import {context} from './context.js';

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
    disableResizeWatcher: false,
    menuButton: true,
  }),
  mounted() {
    if (context['target'] === 'theorem') {
      this.drawerWidth = 512;
      this.disableResizeWatcher = true;
    }
  },
  delimiters: ['$(', ')'],
});
