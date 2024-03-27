import {context} from '../../../js/context.js';
export const ExplanationView = {
  data: () => ({
    explanationTitle: '',
    explanationText: '',
    explanationPreview: '',
    content: '',
  }),
  mounted() {
    this.explanationTitle = this.$route.params.title;
    this.reloadExplanation();
  },
  methods: {
    reloadExplanation() {
      return axios.get(context['explanation_uri'],
          {params: {title: this.explanationTitle}},
      ).then((response) => {
        this.explanationPreview = response.data.preview;
        this.content = document.getElementById('explanationText');
        this.content.innerHTML = this.explanationPreview;
        return this.explanationTitle;
      })
          .catch((error) => console.log(error));
    },
    getTextByTitle(dataArray, title) {
      const element = dataArray.find((item) => item.title === title);
      return element ? element.text : null;
    },
    reloadUpdate_form() {
      this.$router.push({
        name: 'Update',
        params: {title: this.explanationTitle},
      });
      location.reload();
    },
    reloadDelete_form() {
      this.$router.push({
        name: 'Delete',
        params: {title: this.explanationTitle},
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
