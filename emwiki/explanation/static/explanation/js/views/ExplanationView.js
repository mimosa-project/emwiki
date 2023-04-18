import { Escape, PartialDescape } from "../models/markdown-mathjax.js";

export const ExplanationView = {
    data: () => ({
        explanationTitle: '',
        explanationText: '',
        content: '',
        url: '/explanation/explanation',
    }),
    mounted() {
        this.explanationTitle = this.$route.params.title;
        this.reloadExplanation();

    },
    methods: {
        reloadExplanation() {
            return axios.get(this.url, {
            }).then((response) => {
                this.explanations = response.data.index;
                for (var i = 0; i < this.explanations.length; i++) {
                    if (this.explanationTitle === this.explanations[i].title) {
                        this.explanationText = this.explanations[i].text;
                    }
                }

                this.content = document.getElementById("explanationText");
                this.content.innerHTML = Escape(this.explanationText);
                MathJax.typesetPromise([this.content]).then(() => {
                    this.content.innerHTML = marked(PartialDescape(this.content.innerHTML));
                });
                return this.explanationTitle;
            })
                .catch(error => console.log(error));
        },
        reloadUpdate_form() {
            this.$router.push({ name: 'Update', params: { title: this.explanationTitle } });
            location.reload();
        },
        reloadDelete_form() {
            this.$router.push({ name: 'Delete', params: { title: this.explanationTitle } });

        },
    },
    template:
        `<v-container fluid>
            <h1 class='display-3' id="explanationTitle">$( explanationTitle )</h1>
            <div id="explanationText" name="content"></div>

                <v-btn class="ma-2" outlined color="green" @click=reloadUpdate_form()>update</v-btn>
                <v-btn class="ma-2" outlined color="red" @click=reloadDelete_form()>delete</v-btn>
        </v-container>`,
    delimiters: ['$(', ')'],
};