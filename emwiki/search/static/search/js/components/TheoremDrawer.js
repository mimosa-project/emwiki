// eslint-disable-next-line no-unused-vars
const TheoremDrawer = {
  data: () => ({
    articleHeight: 0,
    searchHeight: 0,
    searchText: '',
    isAscii: true,
    loading: false,
    TheoremModels: [],
  }),
  mounted() {
    // 検索結果表示枠の高さを計算
    this.searchHeight =
      document.getElementsByTagName('body')[0].clientHeight -
      document.getElementById('search-btn').getBoundingClientRect().bottom;
  },
  methods: {
    search(searchText) {
      // asciiの場合のみ検索を実行
      if (searchText.match(/^[\x20-\x7e\s]+$/)) {
        this.isAscii = true;
        this.loading = true;
        TheoremService.searchTheorem(searchText).then((response) => {
          this.TheoremModels = response.searchResults;
          this.loading = false;
        });
      } else {
        this.isAscii = false;
      }
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
      TheoremService.recordReactions(id, buttonType);
      if (buttonType === 'fav') {
        // ボタンの見た目を切り替える
        const btnElement = document.getElementById('fav-btm-' + id);
        if (btnElement.className.match(/blue/)) {
          btnElement.classList.remove('blue');
        } else {
          btnElement.classList.add('blue');
        }
      }
    },
  },
  template:
    `<div>
      <v-textarea
        outlined
        name="search"
        label="search theorem"
        v-model="searchText"
        @keydown.shift.enter="search(searchText)"
        class="pt-10"
      >
      </v-textarea>
      <v-btn v-if="loading" block disabled>
        <v-progress-circular indeterminate color="primary" />
      </v-btn>
      <v-btn v-else block @click="search(searchText)" id="search-btn">
        Search
      </v-btn>
      <div v-if="!isAscii" class="alert alert-danger m-3" role="alert">
        Search text allows ascii characters only
      </div>
        <div v-bind:style="'height: ' + searchHeight + 'px; overflow-y: auto;'">
          <v-card
            v-for="TheoremModel in TheoremModels"
            :key="TheoremModel.id"
            :name="TheoremModel.id"
          >
            <v-btn
              text
              block
              color="blue"
              class="theorem-label p-4 pl-2" 
              @click.once="recordReactions(TheoremModel.id, 'url')"
              @click="loadArticle(TheoremModel.url)"
            >
              <p class="text-h5 m-0 mr-auto">$(TheoremModel.label)</p>
            </v-btn>
            <v-card-text class="black--text">$(TheoremModel.text)</v-card-text>
            <v-card-actions outlined rounded text background-color="blue">
              <v-btn
                @click="recordReactions(TheoremModel.id, 'fav')"
                :id="'fav-btm-' + TheoremModel.id"
                class="mr-3"
              >
                <v-icon color="blue">mdi-thumb-up</v-icon>
              </v-btn>
              <span class="pr-5 text-subtitle-2 grey--text text--darken-2">
                relevance: $(TheoremModel.relevance)
              </span>
              <span class="pr-5 text-subtitle-2 grey--text text--darken-2">
                file: $(TheoremModel.filename) $(TheoremModel.line_no)
              </span>
            </v-card-actions>
          </v-card>
        </div>
    </div>`,
  delimiters: ['$(', ')'],
};
