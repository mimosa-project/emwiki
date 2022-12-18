import { Splitter } from '../../js/Splitter.js';
import { ExplanationDrawer } from './components/ExplanationDrawer.js';
import { createExplanation } from './views/ExplanationView.js';


new Vue({
    el: '#app',
    vuetify: new Vuetify(),
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

