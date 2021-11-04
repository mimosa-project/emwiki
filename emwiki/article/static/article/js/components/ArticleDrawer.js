var ArticleDrawer = {
  methods: {
    onArticleRowClick(row) {
      if (this.$route.params.name !== row.name) {
        this.$router.push({ name: 'Article', params: { name: row.name } })
      }
    }
  },
  data: () => ({
    headers: [{ text: 'name', value: 'name' }],
    searchText: '',
    index: []
  }),
  async mounted() {
    try {
      this.index = await ArticleService.getIndex(context['names_uri']);
    } catch (e) {
      alert(e);
    }
  },
  methods: {
    getIndex() {
      return axios.get(context['names_uri']).then((response) => {
        return response.data.index
      })
    },
    onArticleRowClick(row) {
      if (this.$route.params.name !== row.name) {
        this.$router.push({ name: 'Article', params: { name: row.name } })
      }
    }
  },
  template: `
<div>
    <v-text-field
        name="search"
        label="search"
        v-model="searchText"
    >
    </v-text-field>
    <v-data-table
        :headers="headers"
        :items="index"
        :search="searchText"
        :items-per-page="-1"
        item-key="name"
        dense
        hide-default-footer
        @click:row="onArticleRowClick"
    >
    </v-data-table>
</div>
        `
}