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
    query: '',
    index: [],
    searchResult: [],
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
    highlight(articleName) {
      if (this.query !== '') {
        return this.highlighter.run(articleName, this.query);
      } else {
        return articleName;
      }
    },
    // searcher.runで非同期で処理される関数
    updateSearchResults(resultsList) {
      // チャンクごとの検索結果をハイライトしsearchResultに追加する
      resultsList.map((article) => {
        article.name = this.highlight(article.name);
        this.searchResult.push(article);
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
        :search="query"
        :items-per-page="-1"
        item-key="name"
        dense
        hide-default-footer
        @click:row="onArticleRowClick"
    >
      <template v-slot:item.name="props">
        <p class="m-0 p-2" v-html="props.item.name">
        </p>
       </template>
    </v-data-table>
</div>
        `,
};
