var SymbolDrawer = {
  methods: {
    onSymbolRowClick(row) {
      if (this.$route.params.name !== row.name) {
        this.$router.push({ name: 'Symbol', params: { name: row.name } })
      }
    }
  },
  data: () => ({
    headers: [{ text: 'name', value: 'name' }],
    searchText: '',
    index: []
  }),
  mounted() {
    SymbolService.getIndex(context['names_uri']).then((index) => {
      this.index = index
    }).catch((e) => {
      alert(e);
    });
  },
  methods: {
    onSymbolRowClick(row) {
      if (this.$route.params.name !== row.name) {
        this.$router.push({ name: 'Symbol', params: { name: row.name } })
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
              dense
              hide-default-footer
              @click:row="onSymbolRowClick"
          >
          </v-data-table>
      </div>`
}
