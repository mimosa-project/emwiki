import { Splitter } from '../../js/Splitter.js';
import { ExplanationDrawer } from './components/ExplanationDrawer.js';
import { createExplanation } from './createExplanation.js';
import { router } from './router/index.js';


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

