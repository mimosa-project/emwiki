import { onTextAreaKeyDown } from '../models/editor.js';
import { escape, partialDescape } from '../models/markdown-mathjax.js';

export const updateExplanation = {
  data() {
    return {
      text: '',
      preview: '',
      input: '',
      buffer: '',
      content: '',
      explanationTitle: '',
      explanationText: '',
      url: '/explanation/explanation',
      detailurl: '/explanation/detail/',
    };
  },
  mounted() {
    this.explanationTitle = this.$route.params.title;
    this.reload_Explanation();
  },
  methods: {
    reload_Explanation() {
      return axios.get(this.url).then((response) => {
        const explanations = response.data.explanation;
        this.explanationText = this.getTextByTitle(explanations, this.explanationTitle);
        this.preview = document.getElementById('preview-field');
        this.buffer = document.getElementById('preview-buffer');
        this.content = this.explanationText;
        this.content = escape(this.content);
        // preview-bufferにcontentを代入する
        this.buffer.innerHTML = this.content;
        // MathJaxを適用する
        MathJax.typesetPromise([this.buffer]).then(() => {
          this.preview.innerHTML =
            marked(partialDescape(this.buffer.innerHTML));
        });

        return this.explanationTitle, this.explanationText;
      })
        .catch((error) => console.log(error));
    },
    getTextByTitle(dataArray, title) {
      const element = dataArray.find(item => item.title === title);
      return element ? element.text : null;
    },
    changeExplanation() {
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
      axios.put(this.detailurl + this.explanationTitle +
        '/update', {
        text: this.explanationText,
      })
        .then(() => {
          location.href = '/explanation';
        })
        .catch((error) => console.log(error));
    },
    // https://github.com/kerzol/markdown-mathjax/blob/master/editor.htmlを参考に作成
    createPreview() {
      this.preview = document.getElementById('preview-field');
      this.buffer = document.getElementById('preview-buffer');
      this.input = document.getElementById('input-field');
      // 入力した文字を取得
      this.content = this.input.value;
      // content内の文字列をエスケープする
      this.content = escape(this.content);
      // preview-bufferにcontentを代入する
      this.buffer.innerHTML = this.content;
      // MathJaxを適用する
      MathJax.typesetPromise([this.buffer]).then(() => {
        this.preview.innerHTML =
          marked(partialDescape(this.buffer.innerHTML));
      });
    },
    complementwords() {
      const inputField = document.getElementById('input-field');
      inputField.onkeydown = function (event) {
        onTextAreaKeyDown(event, this);
      };
    },
    reloadDetail_form() {
      this.$router.push({
        name: 'Detail',
        params: { title: this.explanationTitle },
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
