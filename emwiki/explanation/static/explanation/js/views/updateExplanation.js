import {ArticleService} from '../../../article/js/services/article-service.js';
import {context} from '../../../js/context.js';
import {onTextAreaKeyDown} from '../models/editor.js';
import {escape, partialDescape} from '../models/markdown-mathjax.js';

export const updateExplanation = {
  data() {
    return {
      text: '',
      preview: '',
      input: '',
      output: '',
      buffer: '',
      content: '',
      explanationTitle: '',
      explanationText: '',
      explanationPreview: '',
      regex: '',
      embedUrl: '',
      embedHtml: '',
      endhtml: '',
      embedSources: [],
      embedHtmls: [],
      Articles: [],
    };
  },
  mounted() {
    this.explanationTitle = this.$route.params.title;
    this.reload_Explanation();
  },
  methods: {
    reload_Explanation() {
      return axios.get(context['explanation_uri'],
          {params: {title: this.explanationTitle}},
      ).then((response) => {
        this.explanationText = response.data.text;
        this.explanationPreview = response.data.preview;
        this.input = document.getElementById('input-field');
        this.output = document.getElementById('preview-field');
        this.input.value = this.explanationText;
        this.output.innerHTML = this.explanationPreview;

        this.regex = /embed\(\/article\/([^\/]+)#([^#\d]+)(\d+)\)/g;
        let match;
        while ((match = this.regex.exec(this.input.value)) !== null) {
          const url = match[0];
          if (!this.embedSources.includes(url)) {
            this.embedSources.push(url);
          }
        }
        return this.explanationTitle;
      })
          .catch((error) => console.log(error));
    },
    getTextByTitle(dataArray, title) {
      const element = dataArray.find((item) => item.title === title);
      return element ? element.text : null;
    },
    changeExplanation() {
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
      axios.put(this.$router.resolve({
        name: 'Update',
        params: {title: this.explanationTitle},
      }).href, {
        text: this.explanationText,
        preview: this.output.innerHTML,
        embedSources: this.embedSources,
      })
          .then(() => {
            location.href = context['base_uri'];
          })
          .catch(() => alert('Editing is only allowed to registered users \n' +
          'Please login or signup'));
    },
    // https://github.com/kerzol/markdown-mathjax/blob/master/editor.htmlを参考に作成
    createPreview() {
      this.buffer = document.getElementById('preview-buffer');
      // 入力した文字を取得
      let content = this.input.value;
      this.embedArticle();
      // content内の文字列をエスケープする
      content = escape(content);
      this.processEmbedSources();

      for (let i = 0; i < this.Articles.length; i++) {
        const url = this.Articles[i].url;
        const html = this.Articles[i].html;
        // const regex = new RegExp(url, 'g');
        content = content.replace(url, html);
      }
      this.content = content;

      // preview-bufferにcontentを代入する
      this.buffer.innerHTML = this.content;
      // MathJaxを適用する
      MathJax.typesetPromise([this.buffer]).then(() => {
        this.output.innerHTML =
          marked(partialDescape(this.buffer.innerHTML));
      });
    },
    complementwords() {
      const inputField = document.getElementById('input-field');
      inputField.onkeydown = function(event) {
        onTextAreaKeyDown(event, this);
      };
    },
    embedArticle() {
      const inputText = document.getElementById('input-field').value;
      this.regex = /embed\(\/article\/([^\/]+)#([^#\d]+)(\d+)\)/g;
      const matches = [];
      let match;

      while ((match = this.regex.exec(inputText)) !== null) {
        const url = match[0];
        const name = match[1];
        const fragment = match[2] + match[3];
        matches.push({name: name, fragment: fragment});

        if (!this.embedSources.includes(url)) {
          this.embedSources.push(url);
        }
      }
    },
    async processEmbedSources() {
      for (let i = 0; i < this.embedSources.length; i++) {
        this.regex.lastIndex = 0;
        const match = this.regex.exec(this.embedSources[i]);
        const articleName = match[1];
        const fragment = match[2] + match[3];

        try {
          const articleHtml = await ArticleService.getHtml(
              context['article_html_base_uri'],
              articleName,
          );
          const htmls = this.removePattern(articleHtml).split('\n</div>\n<br>');
          this.embedHtmls[i] = htmls.filter((html) =>
            html.includes('name="' + fragment + '"'));
          this.Articles.push({
            url: this.embedSources[i],
            html: this.embedHtmls[i],
          });
        } catch (error) {
          console.error('Error fetching HTML:', error);
          // Handle error as needed
        }
      }
    },
    removePattern(text) {
      const pattern = /<body class="no-mathjax">[\s\S]*?<br><br><div><\/div>/;
      // パターンにマッチする部分を空文字列に置換して削除
      const result = text.replace(pattern, '');
      return result;
    },
    reloadDetail_form() {
      this.$router.push({
        name: 'Detail',
        params: {title: this.explanationTitle},
      });
      location.reload();
    },
  },
  template:
    `<div class="container" id="app">
            <v-form ref="explanationForm">
                <div class="columns">
                    <div class="column is-6" id="input-field-wrapper">
                        <h2><i class="fas fa-edit"></i> Input</h2>
                        <textarea class="textarea" name="input-field" 
                            id="input-field" 
                            v-model="explanationText" 
                            @keyup="createPreview(); complementwords()" 
                            spellcheck="false"><br>
                        </textarea>
                    </div>
                    <div class="column is-6" id="preview-field-wrapper">
                        <h2><i class="fas fa-eye"></i> Preview</h2>
                        <div class="content" id="preview-field" 
                            v-model="preview"></div>
                        <div class="preview content" id="preview-buffer" 
                            style="display:none;
                            position:absolute; 
                            top:0; left: 0"></div>
                    </div>
                </div>

                <v-btn class="ma-2" outlined color="green" 
                    @click="changeExplanation()">submit</v-btn>
                <v-btn class="ma-2" outlined color="red" 
                    @click="reloadDetail_form()">cancel</v-btn>
            </v-form>
        </div>`,
  delimiters: ['$(', ')'],
};
