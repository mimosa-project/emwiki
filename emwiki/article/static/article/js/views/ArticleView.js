const ArticleView = {
  data: () => ({
    bibTooltip: 'no bibs found',
    articleHtml: '',
    articleName: '',
    anchorElement: null
  }),
  mounted() {
    this.reload(this.$route.params.name);
  },
  methods: {
    reload(name) {
      name = name.replace('.html', '')
      ArticleService.getHtml(context['article_base_uri'], name).then((articleHtml) => {
        this.articleHtml = articleHtml
        this.$nextTick(() => {
          anchorName = this.$route.hash.split('#')[1]
          if(anchorName) {
            this.anchorElement = document.getElementsByName(anchorName)[0]
          } else {
            window.scroll({top: 0, behavior: 'smooth'})
          }
          this.addComment(name, $("#htmlized-mml"));
        })
      });
      ArticleService.getBib(context['bibs_uri'], name).then((bibText) => {
        this.bibTooltip = bibText
      });
      this.articleName = name;
    },
    addComment(name, root) {
      const article = new Article(name, root);
      const parser = new Parser(root);
      const comments = parser.list_comments(article);
      Comment.bulk_fetch(article, comments, context["comments_uri"]);
    }
  },
  watch: {
    $route(newVal, oldVal) {
      this.reload(this.$route.params.name);
    },
    anchorElement(newVal, oldVal) {
      if(oldVal){
        oldVal.style.backgroundColor = "white"
      }
      // #5D9BF7 means default anchor color like blue
      newVal.style.backgroundColor = '#5D9BF7'
      newVal.scrollIntoView()
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
