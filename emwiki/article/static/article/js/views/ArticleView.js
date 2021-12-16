import {ArticleService} from '../services/article-service.js';
import {Article} from '../models/article.js';
import {Comment} from '../models/comment.js';
import {Parser} from '../models/parser.js';
import {context} from '../../../js/context.js';

export const ArticleView = {
  data: () => ({
    bibTooltip: 'no bibs found',
    articleHtml: '',
    articleName: '',
  }),
  mounted() {
    this.reloadArticle(this.$route.params.name.replace('.html', ''))
        .then(() => {
          this.navigateToHash(this.$route.hash);
        });
  },
  methods: {
    reloadArticle(name) {
      return new Promise((resolve) => {
        this.articleName = name.replace('.html', '');
        ArticleService.getBib(context['bibs_uri'], this.articleName)
            .then((bibText) => {
              this.bibTooltip = bibText;
            });
        ArticleService.getHtml(
            context['article_html_base_uri'],
            this.articleName,
        ).then((articleHtml) => {
          this.articleHtml = articleHtml;
          this.$nextTick(() => {
            // targetがtheoremの場合はaタグの挙動を変更(変更しないとページが再ロードされ定理検索の結果が消えてしまうため)
            if (context['target'] === 'theorem') {
              const aTagElements = this.$el.getElementsByTagName('a');
              for (let i = 0; i < aTagElements.length; i++) {
                if (aTagElements[i].href !== 'javascript:()' &&
                    aTagElements[i].href !== '') {
                  aTagElements[i].addEventListener('click', (event) => {
                    event.preventDefault();
                    return window.open(event.target.href, '_blank');
                  });
                }
              }
            }
            this.addComment(this.articleName, $('#htmlized-mml'));
          });
        }).then(() => {
          resolve();
        });
      });
    },
    addComment(name, root) {
      const article = new Article(name, root);
      const parser = new Parser(root);
      const comments = parser.list_comments(article, context['comments_uri']);
      Comment.bulkFetch(article, comments, context['comments_uri']);
    },
    navigateToHash(hash) {
      const newHashElement =
        document.getElementsByName(hash.replace('#', ''))[0];
      // #5D9BF7 means default anchor color like blue
      newHashElement.style.backgroundColor = '#5D9BF7';
      newHashElement.scrollIntoView();
    },
  },
  watch: {
    async $route(newRoute, oldRoute) {
      if (newRoute.params.name !== oldRoute.params.name) {
        await this.reloadArticle(newRoute.params.name.replace('.html', ''));
      } else {
        if (oldRoute.hash) {
          const oldHashElement =
            document.getElementsByName(oldRoute.hash.replace('#', ''));
          if (oldHashElement.length) {
            oldHashElement[0].style.backgroundColor = 'white';
          }
        }
      }
      if (newRoute.hash) {
        this.navigateToHash(newRoute.hash);
      } else {
        window.scroll({top: 0, behavior: 'smooth'});
      }
    },
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
  delimiters: ['$(', ')'],
};
