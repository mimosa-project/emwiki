import {ArticleService} from '../../../article/js/services/article-service.js';
import {context} from '../../../js/context.js';
import {onTextAreaKeyDown} from '../models/editor.js';
import {escape, partialDescape} from '../models/markdown-mathjax.js';
export const createExplanation = {
  data() {
    return {
      title: '',
      text: '',
      preview: '',
      input: '',
      output: '',
      buffer: '',
      content: '',
      url: '/explanation/explanation',
      regex: '',
      embedUrl: '',
      embedHtml: '',
      endhtml: '',
      embedSources: [],
      embedHtmls: [],
      Articles: [],
    };
  },

  methods: {
    createExplanation() {
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
      axios.post(this.url, {
        title: this.title,
        text: this.text,
        preview: this.output.innerHTML,
      })
          .then(() => {
            location.href = '/explanation';
          })
          .catch((error) => {
            alert(error.response.data.errors);
          });
    },
    // https://github.com/kerzol/markdown-mathjax/blob/master/editor.htmlを参考に作成
    createPreview() {
      this.output = document.getElementById('preview-field');
      this.buffer = document.getElementById('preview-buffer');
      this.input = document.getElementById('input-field');
      // 入力した文字を取得
      const content = this.input.value;
      this.embedArticle();
      // content内の文字列をエスケープする
      content = escape(content);

      this.processEmbedSources();
      for (let i = 0; i < this.Articles.length; i++) {
        const url = this.Articles[i].url;
        const html = this.Articles[i].html;
        // this.removePattern(html);
        // const regex = new RegExp(url, 'g');
        content = content.replace(url, html);
      }
      this.content = content;
      // console.log(this.output);

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
    checkTitle() {
      const invalidChars = /[!@$%#^&*()=+\[\]{};':"\\|,<>\/?]/g;
      if (this.title.match(invalidChars)) {
        const invalidChar = this.title.match(invalidChars);
        alert(invalidChar + 'cannot be used in titles');
        this.title = '';
      }
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
          // console.log(typeof JSON.stringify(this.embedHtmls[i]));
          // this.removePattern(JSON.stringify(this.embedHtmls[i]));
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
  },
  template:
    `<div class="container" id="app">
        <v-form ref="explanationForm">
            <div class="flex-container">
                <p class='display-3'>TITLE:</p>
                <input id="title" v-model='title' class='display-3' 
                    @keyup="checkTitle"/>
            </div>
            <p id='notes'>
              The following characters cannot be used in the title.
            </p>
            <p  id='notes'>'! @$%#^&*()=+\[\]{};':"\\|,<>\/?'</p>
            <div class="columns">
                <div class="column is-6" id="input-field-wrapper">
                    <h2><i class="fas fa-edit"></i> Input</h2>
                    <textarea class="input-field" name="input-field" 
                        id="input-field" v-model="text" 
                        v-model="text" @keyup="createPreview(); 
                        complementwords()" spellcheck="false"><br>
                    </textarea>
                </div>
                <div class="column is-6" id="preview-field-wrapper">
                    <h2><i class="fas fa-eye"></i> Preview</h2>
                    <div class="content" id="preview-field" v-model="preview">
                    </div>
                    <div class="buffer content" id="preview-buffer" 
                    style="display:none;
                    position:absolute; 
                    top:0; left: 0"></div>
                </div>
            </div>

            <v-btn class="ma-2" outlined color="green" 
                @click="createExplanation()">submit</v-btn>
            <v-btn class="ma-2" outlined color="red" 
                @click="history.back()">cancel</v-btn>
        </v-form>
    </div>`,
  delimiters: ['$(', ')'],
};
