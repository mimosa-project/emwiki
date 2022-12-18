import { context } from '../../../js/context.js';
import { Article } from '../models/article.js';
import { Comment } from '../models/comment.js';
import { Parser } from '../models/parser.js';
import { ArticleService } from '../services/article-service.js';

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
            this.addComment(
              this.articleName,
              document.getElementById('htmlized-mml'),
            );
            this.addLinkToKeyword();
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
    addLinkToKeyword() {
      // Lemmaにリンクを追加
      const LemmaElements =
        document.querySelectorAll('#htmlized-mml>[typeof="oo:Lemma"]');
      LemmaElements.forEach((LemmaElement) => {
        if (LemmaElement.previousElementSibling) {
          LemmaElement.previousElementSibling.style.cursor = 'pointer';
          LemmaElement.previousElementSibling.addEventListener('click', () => {
            this.$router.push({
              name: 'Article',
              params: { name: this.articleName },
              hash: LemmaElement.getAttribute('about'),
            });
          });
        }
      });
      // Lemma以外のキーワードにリンクを追加
      document.querySelectorAll('a[name]').forEach((element) => {
        if (element.querySelector('.kw, .comment')) {
          element.addEventListener('click', () => {
            this.$router.push({
              name: 'Article',
              params: { name: this.articleName },
              hash: '#' + element.getAttribute('name'),
            });
          });
        }
      });
    },
    navigateToHash(hash) {
      if (hash) {
        const newHashElement =
          document.querySelector(`[name=${hash.replace('#', '')}]`);
        // Lemmaでは, name属性を持っているa要素が空文字なので, 次の要素をハイライトする
        // <a name="E2"></a>
        // <span>Lm1</span>
        if (hash.startsWith('#E')) {
          newHashElement.nextElementSibling.classList.add('selected');
        } else {
          newHashElement.classList.add('selected');
        }
        newHashElement.scrollIntoView();
      }
    },
  },
  watch: {
    async $route(newRoute, oldRoute) {
      if (newRoute.params.name.replace('.html', '') !==
        oldRoute.params.name.replace('.html', '')
      ) {
        await this.reloadArticle(newRoute.params.name.replace('.html', ''));
      } else {
        if (oldRoute.hash) {
          document.querySelector('.selected')?.classList.remove('selected');
        }
      }
      if (newRoute.hash) {
        this.navigateToHash(newRoute.hash);
      } else {
        window.scroll({ top: 0, behavior: 'smooth' });
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