import {context} from '../../../js/context.js';
import {deleteExplanation} from '../views/DeleteView.js';
import {ExplanationView} from '../views/ExplanationView.js';
import {updateExplanation} from '../views/updateExplanation.js';

export const router = new VueRouter({
  mode: 'history',
  base: context['explanation_detail_uri'],
  routes: [
    {
      path: '/:title',
      name: 'Detail',
      component: ExplanationView,
    },
    {
      path: '/:title/delete',
      name: 'Delete',
      component: deleteExplanation,
    },
    {
      path: '/:title/update',
      name: 'Update',
      component: updateExplanation,
    },
  ],
});
