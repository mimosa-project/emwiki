import {SymbolService} from '../services/symbol-service.js';
import {Searcher} from '../Searcher.js';
import {Highlighter} from '../Highlighter.js';
import {context} from '../../../js/context.js';

export const SymbolDrawer = {
  data: () => ({
    headers: [{text: 'type', value: 'type'}, {text: 'name', value: 'name'}],
    query: '',
    index: [],
    searchResult: [],
    items: [],
    searcher: null,
    highlighter: null,
  }),
  mounted() {
    SymbolService.getIndex(context['names_uri']).then((index) => {
      this.index = index;
      this.items = index;
      this.searcher = new Searcher(index);
    }).catch((e) => {
      alert(e);
    });
    this.highlighter = new Highlighter();
  },
  methods: {
    onSymbolRowClick(row) {
      if (this.$route.params.name !== row.name) {
        this.$router.push({name: 'Symbol', params: {name: row.name}});
      }
    },
    highlight(symbol) {
      if (this.query !== '') {
        return this.highlighter.run(symbol, this.query);
      } else {
        return symbol;
      }
    },
    // searcher.runで非同期で処理される関数
    updateSearchResults(resultsList) {
      resultsList.map((symbol) => {
        symbol.name = this.highlight(symbol.name);
        this.searchResult.push(symbol);
      });
    },
  },
  watch: {
    query(newQuery) {
      if (newQuery !== '') {
        this.searchResult = [];
        this.items = this.searchResult;
        this.searcher.run(newQuery, this.updateSearchResults);
      } else {
        this.items = this.index;
      }
    },
  },
  template: `
      <div>
          <v-text-field
              name="search"
              label="search"
              v-model="query"
              filled
          >
          </v-text-field>
          <v-data-table
              :headers="headers"
              :items="items"
              :items-per-page="1000"
              dense
              :footer-props="{'items-per-page-options': [100, 1000, 5000, -1]}"
              @click:row="onSymbolRowClick"
          >
            <template v-slot:item.name="props">
              <p class="m-0 p-2" v-html="props.item.name">
              </p>
            </template>
          </v-data-table>
      </div>`,
};
