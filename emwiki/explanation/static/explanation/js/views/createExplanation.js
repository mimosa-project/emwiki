import {onTextAreaKeyDown} from '../models/editor.js';
import {escape, partialDescape} from '../models/markdown-mathjax.js';
import {ArticleService} from '../../../article/js/services/article-service.js';
import {context} from '../../../js/context.js';
export const createExplanation = {
  data() {
    return {
      title: '',
      text: '',
      preview: '',
      input: '',
      output:'',
      buffer: '',
      url: '/explanation/explanation',
      articleHtmls: [],
    };
  },
  mounted() {
    // ArticleService.getIndex(context['article_names_uri']).then((index) => {
    //   this.index = index;
    //   console.log(this.index);
    // });
  },
  methods: {
    createExplanation() {
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
      axios.post(this.url, {
        title: this.title,
        text: this.text,
        preview: this.preview,
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
      let content = this.input.value;
      // content内の文字列をエスケープする
      this.embedArticle();
      content = escape(content);
      content = content.replace("embed(/article/abcmiz_0#D1)", this.articleHtmls[0])
      // preview-bufferにcontentを代入する
      this.buffer.innerHTML = content;
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
    embedArticle(){
      const inputText = document.getElementById('input-field').value;
      var regex = /embed\(\/article\/([^\/]+)#([^#\d]+)(\d+)\)/g;
      var matches = [];
      var match;

      while ((match = regex.exec(inputText)) !== null) {
        var name = match[1];
        var fragment = match[2];
        var number = match[3];
        matches.push({ name: name, fragment: fragment, number: number });
      }
      for(let i = 0; i < matches.length; i++){
        ArticleService.getHtml(
          context['article_html_base_uri'],
          matches[i].name,
        ).then((articleHtml) => {
          this.articleHtmls[i] = articleHtml;
        });
      }
      // console.log(this.articleHtmls);
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
