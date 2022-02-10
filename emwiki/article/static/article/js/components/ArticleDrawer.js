import {ArticleService} from '../services/article-service.js';
import {Searcher} from '../../../js/Searcher.js';
import {context} from '../../../js/context.js';

/**
 * ArticleDrawer
 */
export const ArticleDrawer = {
  data: () => ({
    headers: [{text: 'name', value: 'name'}],
    queryText: '',
    index: [],
    items: [],
    searcher: null,
  }),
  mounted() {
    ArticleService.getIndex(context['names_uri']).then((index) => {
      this.index = index;
      this.items = index;
      this.searcher = new Searcher(index, 'article');
    }).catch((e) => {
      alert(e);
    });
  },
  methods: {
    getIndex() {
      return axios.get(context['names_uri']).then((response) => {
        return response.data.index;
      });
    },
    onArticleRowClick(row) {
      if (this.$route.params.name !== row.name) {
        this.$router.push({name: 'Article', params: {name: row.name}});
      }
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
        :search="queryText"
        :items-per-page="-1"
        item-key="name"
        dense
        :footer-props="{'items-per-page-options': [100, 500, 1000, -1]}"
        @click:row="onArticleRowClick"
    >
        <template v-slot:item.name="props">
            <p 
                class="m-0 p-2" 
                v-html="queryText === '' 
                    ? props.item.name 
                    : props.item.highlightedName"
            >
            </p>
        </template>
    </v-data-table>
</div>
        `,
};
