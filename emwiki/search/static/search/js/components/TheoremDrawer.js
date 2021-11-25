const regex = new RegExp(/^[\x20-\x7e\s]+$/);
// eslint-disable-next-line no-unused-vars
const TheoremDrawer = {
  data: () => ({
    searchHeight: 0,
    searchText: '',
    loading: false,
    theoremModels: [],
  }),
  mounted() {
    // 検索結果表示枠の高さを計算
    this.searchHeight =
      document.getElementsByTagName('body')[0].clientHeight -
      document.getElementById('search-btn').getBoundingClientRect().bottom;
  },
  methods: {
    // 検索クエリのバリデーション
    isAscii(value) {
      if (regex.test(value)) {
        return true;
      } else {
        return 'Search text allows ascii characters only';
      }
    },
    search(searchText) {
      this.loading = true;
      TheoremService.searchTheorem(
          context['search_uri'], searchText).then((response) => {
        this.theoremModels = response.searchResults;
        this.loading = false;
      });
    },
    loadArticle(url) {
      // urlの例: graphsp#T42
      const linkAndHash = url.split('#');
      this.$router.push({
        name: 'Article',
        params: {name: linkAndHash[0]},
        hash: '#' + linkAndHash[1],
        query: {target: 'theorem'}});
    },
    recordReactions(id, buttonType) {
      const csrftoken = Cookies.get('csrftoken');
      TheoremService.recordReactions(
          context['search_uri'], csrftoken, id, buttonType);
      if (buttonType === 'fav') {
        // ボタンの見た目を切り替える
        const btnElement = document.getElementById('fav-btn-' + id);
        if (btnElement.className.match(/grey/)) {
          btnElement.classList.remove('grey');
        } else {
          btnElement.classList.add('grey');
        }
      }
    },
  },
  template:
  `<div>
    <v-form ref="searchForm">
      <v-textarea
        outlined
        clearable
        name="search"
        label="search theorem"
        v-model="searchText"
        @keydown.shift.enter="search(searchText)"
        :rules="[isAscii]"
        class="pt-10"
      >
      </v-textarea>
      <v-btn
        id="search-btn"
        block
        @click="search(searchText)"
        :disabled="isAscii(searchText) !== true"
      >
        <v-progress-circular indeterminate v-if="loading" color="primary" />
        <p v-else class="m-auto">Search</p>
      </v-btn>
    </v-form>
    <v-list :height="searchHeight" class="overflow-auto">
      <v-list-item-group>
        <v-list-item
          v-for="theoremModel in theoremModels"
          :key="theoremModel.id"
          @click.once="recordReactions(theoremModel.id, 'url')"
          @click="loadArticle(theoremModel.url)"
        >
          <v-list-item-content v-bind:name="theoremModel.id">
            <v-card-title class="d-flex justify-space-between">
              $(theoremModel.label)
              <v-chip color="secondary" small>
                relevance: $(theoremModel.relevance)
              </v-chip>
              <v-btn
                @click.stop="recordReactions(theoremModel.id, 'fav')" 
                :id="'fav-btn-' + theoremModel.id"
              >
                <v-icon color="blue">mdi-thumb-up</v-icon>
              </v-btn>
            </v-card-title>
            <v-card-text><code>$(theoremModel.text)</code></v-card-text>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </div>`,
  delimiters: ['$(', ')'],
};
