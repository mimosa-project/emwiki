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
            alert(error.response.data.errors[this.title]);
          });
    },
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
        alert('You can not use that character.');
        this.title = '';
      }
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
            <v-btn class="ma-2" @click="insertArticle()">insert</v-btn>
            <textarea id="Article-field" class='display-1' style="display:none" 
                spellcheck="false">
            </textarea>
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
