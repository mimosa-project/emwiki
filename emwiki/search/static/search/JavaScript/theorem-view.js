const TheoremView = {
    components:{'article-in-search-view': ArticleInSearchView},
    data: () => ({
      articleHeight: 0,
      searchHeight: 0,
      searchText: '',
      isAscii: true,
      loading: false,
      TheoremModels: [],
      articleLink: ''
    }),
    mounted() {
      // Article枠と検索結果表示枠の高さを計算
      this.articleHeight = document.getElementsByTagName('body')[0].clientHeight - document.getElementById('toolbar').getBoundingClientRect().bottom
      this.searchHeight = document.getElementsByTagName('body')[0].clientHeight - document.getElementById('search-btn').getBoundingClientRect().bottom
    },
    methods: {
      search (searchText) {
        // asciiの場合のみ検索を実行
        if (searchText.match(/^[\x20-\x7e\s]+$/)) {
          this.isAscii = true
          this.loading = true
          TheoremService.searchTheorem(searchText).then((response) => {
            this.TheoremModels = response.searchResults
            this.loading = false
          })
        } else {
          this.isAscii = false
        }
      },
      loadArticle (url) {
        // urlの例: graphsp#T42
        this.articleLink = url
      },
      recordLoading (id) {
        TheoremService.recordLoading(id)
      },
      recordFavorite (id) {
        TheoremService.recordFavorite(id)
        // ボタンの見た目を切り替える
        const btnElement = document.getElementById('fav-btm-' + id)
        if (btnElement.className.match(/blue/)) {
          btnElement.classList.remove('blue')
        } else {
          btnElement.classList.add('blue')
        }
      },
    },
    template: 
    `<v-container fluid>
      <v-row>
        <v-col v-bind:style="'height: ' + articleHeight + 'px;'">
          <div>
            <v-textarea
              name="search"
              label="search"
              v-model="searchText"
            >
            </v-textarea>
            <v-btn v-if="loading" block disabled>
              <v-progress-circular indeterminate color="primary" />
            </v-btn>
            <v-btn v-else block @click="search(searchText)" id="search-btn">Search</v-btn>
            <div v-if="!isAscii" class="alert alert-danger m-3" role="alert">Search text allows ascii characters only</div>
              <div v-bind:style="'height: ' + searchHeight + 'px; overflow-y: auto;'">
                <div v-for="TheoremModel in TheoremModels" :key="TheoremModel.id">
                  <v-card v-bind:name="TheoremModel.id">
                    <v-btn
                     text
                     block
                     class="theorem-label p-4 pl-2" 
                     @click="loadArticle(TheoremModel.url)"
                     @click.once="recordLoading(TheoremModel.id)"
                     style="color: blue;"
                     >
                      <p class="text-h5 m-0 mr-auto">$(TheoremModel.label)</p>
                    </v-btn>
                    <v-card-text class="black--text">$(TheoremModel.text)</v-card-text>
                    <v-card-actions outlined rounded text background-color="blue">
                      <v-btn @click="recordFavorite(TheoremModel.id)" v-bind:id="'fav-btm-' + TheoremModel.id" class="mr-3">
                        ☆
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
              </div>
          </div>
        </v-col>
        <v-col v-bind:style="'height: ' + articleHeight + 'px; overflow-y: auto;'">
          <article-in-search-view v-bind:articleLink="articleLink" />
        </v-col>
      </v-row>
    </v-container>`,
    delimiters: ['$(', ')']
  }
  
  // <v-card-title class="headline">$(TheoremModel.label)</v-card-title>