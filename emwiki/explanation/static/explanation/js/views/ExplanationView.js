import { escape, partialDescape } from '../models/markdown-mathjax.js';

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
      return axios.get(this.url,
        { params: { title: this.explanationTitle } }
      ).then((response) => {
        this.explanationText = response.data;
        // https://github.com/kerzol/markdown-mathjax/blob/master/editor.htmlを参考に作成
        this.content = document.getElementById('explanationText');
        this.content.innerHTML = escape(this.explanationText);
        MathJax.typesetPromise([this.content]).then(() => {
          this.content.innerHTML =
            marked(partialDescape(this.content.innerHTML));
        });
        return this.explanationTitle, this.explanationText;
      })
        .catch((error) => console.log(error));
    },
    getTextByTitle(dataArray, title) {
      const element = dataArray.find(item => item.title === title);
      return element ? element.text : null;
    },
    reloadUpdate_form() {
      this.$router.push({
        name: 'Update',
        params: { title: this.explanationTitle },
      });
      location.reload();
    },
    reloadDelete_form() {
      this.$router.push({
        name: 'Delete',
        params: { title: this.explanationTitle },
      });
    },
  },
  template:
    `<v-container fluid>
            <h1 class='display-3' id="explanationTitle">$( explanationTitle )
            </h1>
            <div id="explanationText" name="content"></div>

                <v-btn class="ma-2" outlined color="green" 
                    @click=reloadUpdate_form()>update</v-btn>
                <v-btn class="ma-2" outlined color="red" 
                    @click=reloadDelete_form()>delete</v-btn>
        </v-container>`,
  delimiters: ['$(', ')'],
};
