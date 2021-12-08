import {SymbolView} from '../views/SymbolView.js';
import {context} from '../context.js';

// eslint-disable-next-line no-unused-vars
export const router = new VueRouter({
  mode: 'history',
  base: context['symbol_base_uri'],
  routes: [
    {
      path: '/:name',
      name: 'Symbol',
      component: SymbolView,
    },
  ],
});
