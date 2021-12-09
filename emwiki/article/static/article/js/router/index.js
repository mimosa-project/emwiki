import {ArticleView} from '../views/ArticleView.js';
import {context} from '../../../js/context.js';

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
