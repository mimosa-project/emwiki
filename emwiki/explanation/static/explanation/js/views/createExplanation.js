import { onTextAreaKeyDown } from "../models/editor.js";
import { Escape, PartialDescape } from "../models/markdown-mathjax.js";

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
            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
            axios.post(this.url, {
                title: this.title,
                text: this.text,
            })
                .then(() => {
                    location.href = "/explanation";
                })
                .catch((error) => {
                    alert(error.response.data.errors[this.title]);
                })
        },
        createPreview() {
            this.preview = document.getElementById("preview-field");
            this.buffer = document.getElementById("preview-buffer");
            this.input = document.getElementById("input-field");
            // 入力した文字を取得
            var content = this.input.value;
            // content内の文字列をエスケープする
            content = Escape(content);
            //preview-bufferにcontentを代入する
            this.buffer.innerHTML = content;
            //MathJaxを適用する
            MathJax.typesetPromise([this.buffer]).then(() => {
                this.preview.innerHTML = marked(PartialDescape(this.buffer.innerHTML));
            });
        },

        complementwords() {
            const inputField = document.getElementById("input-field");
            inputField.onkeydown = function (event) {
                onTextAreaKeyDown(event, this);
            }
        },
        checkInput() {
            const invalidChars = /[!@$%#^&*()=+\[\]{};':"\\|,<>\/?]/g;
            if (this.title.match(invalidChars)) {
                alert("You can't use that character.");
                this.title = '';
            }
        },
    },
    template:
        `<div class="container" id="app">
        <v-form ref="explanationForm">
            <div class="flex-container">
                <p class='display-3'>TITLE:</p>
                <input id="title" v-model='title' class='display-3' @keyup="checkInput"/>
            </div>
            <div class="columns">
                <div class="column is-6" id="input-field-wrapper">
                    <h2><i class="fas fa-edit"></i> Input</h2>
                    <textarea class="textarea" name="input-field" id="input-field" v-model="text" 
                        @keyup="createPreview(); complementwords();"><br>
                    </textarea>
                </div>
                <div class="column is-6" id="preview-field-wrapper">
                    <h2><i class="fas fa-eye"></i> Preview</h2>
                    <div class="content" id="preview-field" v-model="preview"></div>
                    <div class="preview content" id="preview-buffer" style="display:none;
                    position:absolute; 
                    top:0; left: 0"></div>
                </div>
            </div>

            <v-btn class="ma-2" outlined color="green" @click="createExplanation()">submit</v-btn>
            <v-btn class="ma-2" outlined color="red" @click="history.back()">cancel</v-btn>
        </v-form>
    </div>`,
    delimiters: ['$(', ')'],
};