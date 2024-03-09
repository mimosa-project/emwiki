// import { context } from '../../../js/context.js';
import {ExplanationService} from '../services/explanation-service.js';
export const ExplanationDrawer = {
  data() {
    return {
      Titles: [],
      headers: [{text: 'title', value: 'title'}],
      queryText: '',
      selectedTitle: '',
    };
  },
  mounted() {
    ExplanationService.getTitle('/explanation/titles')
        .then((titles) => {
          this.Titles = titles;
        })
        .catch((error) => console.log(error));
  },
  methods: {
    getTitle() {
      return axios.get('/explanation/titles').then((response) => {
        return response.data.index;
      });
    },
    onExplanationRowClick(row) {
      this.selectedTitle = row.title;
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
            :items="Titles"
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
    </div>
    `,
  delimiters: ['$(', ')'],
};
