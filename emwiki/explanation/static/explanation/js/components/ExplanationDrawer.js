
export const ExplanationDrawer = {
  data() {
    return {
      explanations: [],
      headers: [{text: 'title', value: 'title'}],
      queryText: '',
      selectedID: '',
    };
  },
  mounted() {
    axios.get('/explanation/explanation')
        .then((response) => {
          this.explanations = response.data.index;
        })
        .catch((error) => console.log(error));
  },
  methods: {
    onExplanationRowClick(row) {
      for (let i = 0; i < this.explanations.length; i++) {
        if (row.id === this.explanations[i].id) {
          this.selectedTitle = this.explanations[i].title;
          console.log(this.selectedTitle);
        }
      }
      location.href = '/explanation/detail/' + this.selectedTitle;
    },
    reloadCreate_form() {
      location.href = '/explanation/create';
    },
  },

  template: `
    <div>
        <v-data-table
            :headers="headers"
            :items="explanations"
            :search="queryText"
            :items-per-page="-1"
            item-key="title"
            dense
            :footer-props="{'items-per-page-options': [100, 500, 1000, -1]}"
            @click:row="onExplanationRowClick"
        >
            <template v-slot:item.title="props">
                <p
                    class="mb-0 py-2"
                    v-html="queryText === ''
                        ? props.item.title
                        : props.item.highlightedName"
                >
                </p>
            </template>
        </v-data-table>
        <v-btn style="width: 100%;" @click=reloadCreate_form()>Create New
        </v-btn>
    </div>
    `,
  delimiters: ['$(', ')'],
};
