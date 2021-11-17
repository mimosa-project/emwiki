const ArticleInSearchView = {
    props: {
      articleLink: String //ロードするアーティクル 例:graphsp#T42
    },
    data: () => ({
      bibTooltip: 'no bibs found',
      articleHtml: '',
      articleName: '',
      articleAnchor: '',
      anchorElement: null
    }),
    methods: {
      reload(articleLink) {
        this.articleHtml = ''
        this.articleName = articleLink.split('#')[0]
        this.articleAnchor = articleLink.split('#')[1]
        ArticleService.getHtml(context['article_html_uri'], this.articleName).then((articleHtml) => {
          this.articleHtml = articleHtml
          //DOMの更新が完了した後の動作
          this.$nextTick(() => {
            // anchorElementを置き換えることでwatchが実行されアンカーまで移動し色付け
            this.anchorElement = document.getElementsByName(this.articleAnchor)[0]
            // htmlized-mml内のaタグ(他アーティクルへのリンク)の動作を書き換え
            const aTagElements = this.$el.getElementsByTagName('a')
            for (let i = 0; i < aTagElements.length; i++) {
              if(aTagElements[i].href != 'javascript:()' && aTagElements[i].href != ''){
                aTagElements[i].addEventListener('click', function(event){
                  event.preventDefault();
                  // リンクを抽出 例: /search/theorem/graphsp.html#T42 -> graphsp#T42
                  const link = this.href.split('/').slice(-1)[0].replace('.html', '')
                  return window.open(context['article_base_uri'] + link, '_blank')
                })
              }
            }
            this.addComment(this.articleName, $("#htmlized-mml"));
          })
        });
        ArticleService.getBib(context['bibs_uri'], this.articleName).then((bibText) => {
          this.bibTooltip = bibText
        });
      },
      addComment(name, root) {
        const article = new Article(name, root);
        const parser = new Parser(root);
        const comments = parser.list_comments(article);
        Comment.bulk_fetch(article, comments, context["comments_uri"]);
      },
    },
    watch: {
      articleLink(newVal, oldVal){
        this.reload(newVal);
      },
      anchorElement(newVal, oldVal) {
        if(oldVal){
          oldVal.style.backgroundColor = "white"
        }
        // #5D9BF7 means default anchor color like blue
        newVal.style.backgroundColor = '#5D9BF7'
        newVal.scrollIntoView({behavior: "smooth"})
      }
    },
    template: `
    <v-container fluid v-if="articleAnchor">
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
      <div id="htmlized-mml" v-html="articleHtml" />
    </v-row>
    </v-container fluid>`,
    delimiters: ['$(', ')']
  }
