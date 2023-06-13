import {onTextAreaKeyDown} from '../models/editor.js';
import {escape, partialDescape} from '../models/markdown-mathjax.js';
export const createExplanation = {
  data() {
    return {
      title: '',
      text: '',
      preview: '',
      input: '',
      buffer: '',
      url: '/explanation/explanation',
      articleHtml: '',
    };
  },
  methods: {
    createExplanation() {
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
      axios.post(this.url, {
        title: this.title,
        text: this.text,
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
      this.preview = document.getElementById('preview-field');
      this.buffer = document.getElementById('preview-buffer');
      this.input = document.getElementById('input-field');
      // 入力した文字を取得
      let content = this.input.value;
      // content内の文字列をエスケープする
      content = escape(content);
      // preview-bufferにcontentを代入する
      this.buffer.innerHTML = content;
      // MathJaxを適用する
      MathJax.typesetPromise([this.buffer]).then(() => {
        this.preview.innerHTML =
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
    // insertArticle() {
    //   const Articlefield = document.getElementById('Article-field');
    //   Articlefield.style.display = 'block'; // inputを表示する
    //   Articlefield.focus(); // inputにフォーカスを当てる

    //   document.getElementById('Article-field')
    // .addEventListener('keyup', function (event) {
    //     if (event.key === 'Enter') { // Enterキーが押されたら
    //       const inputField = document.getElementById('input-field');
    //       const articleName = event.target.value; //入力された値をarticleNameに代入
    //       // const articleurl = "/article/htmls";
    //       ExplanationService.getArticle(
    //         context['article_html_base_uri'],
    //         articleName,
    //       ).then((articleHtml) => {
    //         this.articleHtml = articleHtml;
    //         console.log(this.articleHtml);
    //       });
    //       inputField.value = `${inputField.value}${articleName}`;
    //       event.target.style.display = 'none'; // inputを隠す
    //       event.target.value = ''; // 入力欄をリセットする
    //     }
    //   });
    // },
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
