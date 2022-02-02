import {SymbolService} from '../services/symbol-service.js';
import {Searcher} from '../../../js/Searcher.js';
import {Highlighter} from '../../../js/Highlighter.js';
import {context} from '../../../js/context.js';

export const SymbolDrawer = {
  data: () => ({
    headers: [{text: 'type', value: 'type'}, {text: 'name', value: 'name'}],
    queryText: '',
    index: [],
    searchResults: [],
    items: [],
    searcher: null,
    highlighter: null,
  }),
  mounted() {
    SymbolService.getIndex(context['names_uri']).then((index) => {
      this.index = index;
      this.items = index;
      this.searcher = new Searcher(index, 'symbol');
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
    highlight(symbolName, queryText) {
      if (queryText !== '') {
        return this.highlighter.run(symbolName, queryText);
      } else {
        return symbolName;
      }
    },
    updateSearchResults(resultList) {
      // チャンクごとの検索結果をハイライトしsearchResultに追加する
      resultList.forEach((result) => {
        result.name = this.highlight(result.name, this.queryText);
        this.searchResults.push(result);
      });
    },
  },
  watch: {
    queryText(newQueryText) {
      if (newQueryText !== '') {
        this.searchResults = [];
        this.items = this.searchResults;
        this.searcher.run(newQueryText, this.updateSearchResults);
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
              v-model="queryText"
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
              <p class="m-0 p-2" v-html="props.item.name"></p>
            </template>
          </v-data-table>
      </div>`,
};
