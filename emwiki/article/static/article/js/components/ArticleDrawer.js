import {ArticleService} from '../services/article-service.js';
import {Searcher} from '../../../js/Searcher.js';
import {Highlighter} from '../../../js/Highlighter.js';
import {context} from '../../../js/context.js';

/**
 * ArticleDrawer
 */
export const ArticleDrawer = {
  data: () => ({
    headers: [{text: 'name', value: 'name'}],
    queryText: '',
    index: [],
    searchResults: [],
    items: [],
    searcher: null,
    highlighter: null,
  }),
  mounted() {
    ArticleService.getIndex(context['names_uri']).then((index) => {
      this.index = index;
      this.items = index;
      this.searcher = new Searcher(index, 'article');
    }).catch((e) => {
      alert(e);
    });
    this.highlighter = new Highlighter();
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
    highlight(articleName, queryText) {
      if (queryText !== '') {
        return this.highlighter.run(articleName, queryText);
      } else {
        return articleName;
      }
    },
    // searcher.runで非同期で処理される関数
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
        :search="queryText"
        :items-per-page="-1"
        item-key="name"
        dense
        @click:row="onArticleRowClick"
    >
      <template v-slot:item.name="props">
        <p class="m-0 p-2" v-html="props.item.name"></p>
       </template>
    </v-data-table>
</div>
        `,
};
