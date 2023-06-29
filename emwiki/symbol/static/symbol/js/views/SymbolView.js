import {SymbolService} from '../services/symbol-service.js';
import {context} from '../../../js/context.js';

/**
 * View of Symbol
 */
export const SymbolView = {
  data: () => ({
    symbolName: '',
    compiled: null,
    anchorElement: null,
  }),
  mounted() {
    this.reload(this.$route.params.name, this.$route.hash);
  },
  methods: {
    reload(name, hash) {
      this.symbolName = name;
      this.jumpTo(name, hash);
    },
    jumpTo(name, hash) {
      SymbolService.getHtml(context['symbol_html_uri'], name)
          .then((symbolHtml) => {
            this.compiled = Vue.compile(symbolHtml);
            this.$nextTick(() => {
              const anchorName = hash.replace('#', '');
              this.anchorElement = anchorName ?
                document.getElementById(anchorName) :
                null;
            });
          });
    },
  },
  watch: {
    $route() {
      this.reload(this.$route.params.name, this.$route.hash);
    },
    anchorElement(newVal, oldVal) {
      if (oldVal) {
        oldVal.classList.remove('selected');
      }
      if (newVal) {
        newVal.classList.add('selected');
        newVal.scrollIntoView();
      }
    },
  },
  template: `
      <v-container id="symbol" fluid>
          <v-row>
              <component :is="compiled"></component>
          </v-row>
      </v-container>`,
  delimiters: ['$(', ')'],
};
