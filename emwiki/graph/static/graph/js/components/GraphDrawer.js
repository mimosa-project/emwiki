import {ArticleService} from '../../../article/js/services/article-service.js';
import {context} from '../context.js';

/**
 * GraphDrawer
 */
export const GraphDrawer = {
  name: 'GraphDrawer',
  props: ['graphArticleName', 'graphUpperLevel', 'graphLowerLevel'],
  data: () => ({
    headers: [{text: 'name', value: 'name'}],
    searchText: '',
    index: [],
  }),
  mounted() {
    ArticleService.getIndex(context['article_names_uri']).then((index) => {
      this.index = index;
    });
  },
  computed: {
    articleName: {
      get() {
        return this.graphArticleName;
      },
      set(newVal) {
        this.$emit('article-name-changed', newVal);
      },
    },
    upperLevel: {
      get() {
        if (this.graphUpperLevel) {
          return this.graphUpperLevel;
        } else {
          return 0;
        }
      },
      set(newVal) {
        this.$emit('upper-level-changed', newVal);
      },
    },
    lowerLevel: {
      get() {
        if (this.graphLowerLevel) {
          return this.graphLowerLevel;
        } else {
          return 0;
        }
      },
      set(newVal) {
        this.$emit('lower-level-changed', newVal);
      },
    },
  },
  methods: {
    onGraphRowClick(row) {
      this.articleName = row.name;
    },
  },
  template: `
    <div>
        <v-btn block @click="$emit('reset-clicked')">Reset</v-btn>
        <v-container>
        <v-row>
            <v-col>
            <v-text-field
                v-model="upperLevel"
                type="number"
                label="Upper level"
                min="0"
            ></v-text-field>
            </v-col>
            <v-col>
            <v-text-field
                v-model="lowerLevel"
                type="number"
                label="Lower level"
                min="0"
            ></v-text-field>
            </v-col>
        </v-row>
        </v-container>
        <v-text-field
        label="Search"
        v-model="searchText"
        ></v-text-field>
        <v-data-table
            :headers="headers"
            :items="index"
            :search="searchText"
            :items-per-page="-1"
            item-key="name"
            dense
            hide-default-footer
            @click:row="onGraphRowClick"
        >
        </v-data-table>
    </div>`,
};
