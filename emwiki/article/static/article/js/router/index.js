import {context} from '../../../js/context.js';
import {ArticleView} from '../views/ArticleView.js';

export const router = new VueRouter({
  mode: 'history',
  base: context['article_base_uri'],
  routes: [
    {
      path: '/:name',
      name: 'Article',
      component: ArticleView,
    },
  ],
});
