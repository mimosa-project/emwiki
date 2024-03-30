import {context} from '../../../js/context.js';

export const deleteExplanation = {
  data: () => ({
    explanationTitle: '',
  }),
  mounted() {
    return axios.get(context['explanation_uri'], {
    }).then(() => {
      this.explanationTitle = this.$route.params.title;
      return this.explanationTitle;
    })
        .catch((error) => console.log(error));
  },
  methods: {
    Explanationdelete() {
      axios.defaults.xsrfCookieName = 'csrftoken',
      axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN',
      axios.delete(this.$router.resolve({
        name: 'Delete',
        params: {title: this.explanationTitle},
      }).href, {
      })
          .then(() => {
            location.href = context['base_uri'];
          })
          .catch(() => alert('Deleting is only allowed to registered users \n' +
            'Please login or signup'));
    },
    reloadDetail_form() {
      this.$router.push({
        name: 'Detail',
        params: {title: this.explanationTitle},
      });
      location.reload();
    },
  },
  template: `
    <v-container fluid>
        <h1>Delete document</h1>
        <p>Are you sure?</p>

        <v-form>
            <v-btn class="ma-2" outlined color="green" 
                @click="Explanationdelete()">delete</v-btn>
            <v-btn class="ma-2" outlined color="red" 
                @click="reloadDetail_form()">cancel</v-btn>
        </v-form>
    <v-container>
    `,
  delimiters: ['$(', ')'],
};
