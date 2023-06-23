import {SymbolService} from '../services/symbol-service.js';
import {Searcher} from '../../../js/Searcher.js';
import {context} from '../../../js/context.js';

export const SymbolDrawer = {
  data: () => ({
    headers: [{text: 'type', value: 'type'}, {text: 'name', value: 'name'}],
    queryText: '',
    index: [],
    items: [],
    searcher: null,
  }),
  mounted() {
    SymbolService.getIndex(context['names_uri']).then((index) => {
      this.index = index;
      this.items = index;
      this.searcher = new Searcher(index, 'symbol');
    }).catch((e) => {
      alert(e);
    });
  },
  methods: {
    onSymbolRowClick(row) {
      this.$router.push({name: 'Symbol', params: {name: row.name}});
      window.scroll({top: 0, behavior: 'smooth'});
    },
  },
  watch: {
    queryText(newQueryText) {
      this.searcher.run(
          newQueryText,
          (items) => this.items = items,
          (items) => items.forEach((item) => this.items.push(item)) );
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
                <p
                    class="mb-0 py-2"
                    v-html="queryText === ''
                        ? props.item.name
                        : props.item.highlightedName"
                >
                </p>
            </template>
          </v-data-table>
      </div>`,
};
