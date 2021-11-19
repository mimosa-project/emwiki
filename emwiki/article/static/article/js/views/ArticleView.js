const ArticleView = {
  data: () => ({
    bibTooltip: 'no bibs found',
    articleHtml: '',
    articleName: '',
    hash: '',
  }),
  mounted() {
    this.reloadArticle(this.$route.params.name.replace('.html', '')).then(() => {
      this.hash = this.$route.hash
    })
  },
  methods: {
    reloadArticle(name) {
      return new Promise((resolve) => {
        this.articleName = name.replace('.html', '')
        ArticleService.getBib(context['bibs_uri'], this.articleName).then((bibText) => {
          this.bibTooltip = bibText
        });
        ArticleService.getHtml(context['article_base_uri'], this.articleName).then((articleHtml) => {
          this.articleHtml = articleHtml
          this.$nextTick(() => {
            this.addComment(this.articleName, $("#htmlized-mml"));
          })
        }).then(() => {
          resolve()
        })
      })
    },
    addComment(name, root) {
      const article = new Article(name, root);
      const parser = new Parser(root);
      const comments = parser.list_comments(article);
      Comment.bulk_fetch(article, comments, context["comments_uri"]);
    }
  },
  watch: {
    $route(newRoute, oldRoute) {
      if(newRoute.params.name !== oldRoute.params.name) {
        this.reloadArticle(newRoute.params.name.replace('.html', ''))
      }
      if(newRoute.hash !== oldRoute.hash) {
        this.hash = newRoute.hash
      }
    },
    hash(newHash, oldHash) {
      if(oldHash) {
        oldHashElement = document.getElementsByName(oldHash.split('#')[1])[0]
        oldHashElement.style.backgroundColor = 'white'
      }
      if(newHash) {
        newHashElement = document.getElementsByName(newHash.split('#')[1])[0]
        // #5D9BF7 means default anchor color like blue
        newHashElement.style.backgroundColor = '#5D9BF7'
        newHashElement.scrollIntoView()
      } else {
        window.scroll({top: 0, behavior: 'smooth'})
      }
    }
  },
  template: `
      <v-container id="article" fluid>
          <v-row>
              <v-col class='display-3'>$( articleName )</v-col>
              <v-col>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn v-bind="attrs" v-on="on">
                      bib
                    </v-btn>
                  </template>
                  <pre>$(bibTooltip)</pre>
                </v-tooltip>
              </v-col>
          </v-row>
          <v-row>
              <div id="htmlized-mml" v-html="articleHtml">
              </div>
          </v-row>
      </v-container>`,
  delimiters: ['$(', ')']
}
