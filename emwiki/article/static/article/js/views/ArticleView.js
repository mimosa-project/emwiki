const ArticleView = {
  data: () => ({
    bibTooltip: false,
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
        setTimeout(() => {
          anchorName = this.$route.hash.split('#')[1]
          if(anchorName) {
            this.anchorElement = document.getElementsByName(anchorName)[0]
          } else {
            window.scroll({top: 0, behavior: 'smooth'})
          }
          this.addComment(name, $("#htmlized-mml"));
        }, 1000);
      });
      ArticleService.getBib(context['bibs_uri'], name).then((bibText) => {
        this.bibText = bibText
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
              <v-tooltip
                  v-model="bibTooltip"
                  top
              > id="bib-popover" tabindex="0" class="btn btn-secondary" role="button" data-bs-toggle="popover"
                  data-bs-placement="bottom" data-bs-trigger="focus" data-bs-content="">
                  bib
              </v-btn>
          </v-row>
          <v-row>
              <div id="htmlized-mml" v-html="articleHtml">
              </div>
          </v-row>
      </v-container>`,
  delimiters: ['$(', ')']
}
