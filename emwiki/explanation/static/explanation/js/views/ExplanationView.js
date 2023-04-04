export const ExplanationView = {
    data: () => ({
        explanationID: '',
        explanationTitle: '',
        explanationText: '',
        content: '',
        preview: '',
        buffer: '',
    }),
    mounted() {
        this.explanationID = this.$route.params.id;
        this.reloadExplanation(this.explanationID);

    },
    methods: {
        reloadExplanation(id) {
            return axios.get('/explanation/explanation', {
            }).then((response) => {
                this.explanationTitle = response.data.index[id].title;
                this.content = response.data.index[id].text;
                this.buffer = document.getElementById("content");
                this.explanationText = document.getElementById("content");
                var text = this.Escape(this.content);
                this.buffer.innerHTML = this.preview = text;
                MathJax.typesetPromise([this.buffer]).then(() => {
                    this.PreviewDone();
                });
                return this.explanationTitle, this.content;
            })
                .catch(error => console.log(error));
        },
        reloadDelete_form() {
            this.$router.push({ name: 'Delete', params: { id: this.explanationID } });

        },
        reloadUpdate_form() {
            this.$router.push({ name: 'Update', params: { id: this.explanationID } });
            location.reload();
        },
        PreviewDone: function () {
            var detail = this.buffer.innerHTML;
            detail = this.PartialDescape(detail);
            // this.buffer.innerHTML = marked(content);
            this.explanationText.innerHTML = marked(detail);
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
        test: function () {
            console.log(this.explanationID);

        }
    },
    template:
        `
    <v-container fluid>
        <h1 class='display-3' id="explanationTitle">$( explanationTitle )</h1>
        <div id="content" name="content">$( content )</div>

        <v-btn class="ma-2" outlined color="green" @click=reloadUpdate_form()>update</v-btn>
        <v-btn class="ma-2" outlined color="red" @click=reloadDelete_form()>delete</v-btn>
    </v-container>
    `,
    delimiters: ['$(', ')'],
};