export const createExplanation = {
    data() {
        return {
            id: '',
            title: '',
            text: '',
            preview: '',
            input: '',
            output: '',
            buffer: '',
            oldtext: '',
            url: '/explanation/explanation',
        };
    },
    methods: {
        createExplanation: function () {
            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
            axios.post(this.url, {
                title: this.title,
                text: this.text,
            })
                .then((response) => {
                    console.log("取得成功", response);
                    location.href = "/explanation";
                })
                .catch(error => console.log(error))
        },
        // SwapBuffers: function () {
        //     var buffer = this.preview;
        //     var preview = this.buffer;
        //     this.buffer = buffer;
        //     this.preview = preview;
        // },
        createPreview: function () {
            this.preview = document.getElementById("preview-field");
            this.buffer = document.getElementById("preview-buffer");
            this.input = document.getElementById("input-field");
            var content = this.input.value;
            if (content === this.oldtext) return;
            content = this.Escape(content);
            this.buffer.innerHTML = this.oldtext = content;
            MathJax.typesetPromise([this.buffer]).then(() => {
                this.PreviewDone();
            });
            // MathJax.typeset([this.buffer]).then(() => {
            //     this.PreviewDone();
            // });
            // this.PreviewDone();
        },
        PreviewDone: function () {
            var content = this.buffer.innerHTML;
            content = this.PartialDescape(content);
            // this.buffer.innerHTML = marked(content);
            this.preview.innerHTML = marked(content);
            // this.SwapBuffers();
        },
        Escape: function (html, encode) {
            return html
                .replace(!encode ? /&(?!#?\w+;)/g : /&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
        },
        PartialDescape: function (html) {
            var lines = html.split('\n');
            var out = '';

            // is true when we are 
            // ```
            //  inside a code block
            // ```
            var inside_code = false;

            for (var i = 0; i < lines.length; i++) {
                // a hack to properly rendre the blockquotes
                if (lines[i].startsWith('&gt;')) {
                    lines[i] = lines[i].replace(/&gt;/g, '>');
                }

                // rendrer properly stuff like this
                // ```c
                //  if (a > b)
                // ```
                if (inside_code) {
                    // inside the code we descape stuff
                    lines[i] = lines[i]
                        .replace(/&lt;/g, '<')
                        .replace(/&gt;/g, '>')
                        .replace(/&quot;/g, '"')
                        .replace(/&#39;/g, '\'');
                }
                if (lines[i].startsWith('```')) {
                    inside_code = !inside_code;
                }
                out += lines[i] + '\n';
            }
            return out;
        },
    },
    template:
        `<div class="container" id="app">
        <v-form ref="explanationForm">
            <p>TITLE:</p><input  id="title" v-model='title'/>
            <div class="columns">
                <div class="column is-6" id="input-field-wrapper">
                    <h2><i class="fas fa-edit"></i> Input</h2>
                    <textarea class="textarea" name="input-field" id="input-field" v-model="text" v-on:keyup=createPreview><br>
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

            <v-btn class="ma-2" outlined color="green" @click="createExplanation">submit</v-btn>
            <v-btn class="ma-2" outlined color="red" @click="history.back()">cancel</v-btn>
        </v-form>
    </div>`,
    delimiters: ['$(', ')'],
};