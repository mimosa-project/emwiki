
export const deleteExplanation = {
  data: () => ({
    explanationTitle: '',
    url: '/explanation/explanation',
    detailurl: '/explanation/detail/',
  }),
  mounted() {
    return axios.get(this.url, {
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
        axios.delete(this.detailurl + this.explanationTitle +
          '/delete', {
        })
          .then(() => {
            location.href = '/explanation';
          })
          .catch((error) => console.log(error));
    },
    reloadDetail_form() {
      this.$router.push({
        name: 'Detail',
        params: { title: this.explanationTitle },
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
