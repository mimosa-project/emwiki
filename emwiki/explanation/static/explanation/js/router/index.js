import { context } from '../../../js/context.js';
import { updateExplanation } from '../updateExplanation.js';
import { deleteExplanation } from '../views/DeleteView.js';
import { ExplanationView } from "../views/ExplanationView.js";

export const router = new VueRouter({
    mode: 'history',
    base: context['explanation_detail_uri'],
    routes: [
        {
            path: '/:id',
            name: 'Detail',
            component: ExplanationView,
        },
        {
            path: '/:id/delete',
            name: 'Delete',
            component: deleteExplanation,
        },
        {
            path: '/:id/update',
            name: 'Update',
            component: updateExplanation,
        }
    ],
});
