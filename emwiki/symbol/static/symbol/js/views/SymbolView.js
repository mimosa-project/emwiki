const SymbolView = {
    data: () => ({
      symbolHtml: '',
      symbolName: '',
      compiled: null,
      anchorElement: null
    }),
    async mounted () {
      this.reload(this.$route.params.name);
    },
    methods: {
      async reload (name) {
        this.symbolName = name;
        this.compiled = Vue.compile(await this.getSymbolHtml(name));
        this.jumpTo(this.$route.params.name, this.$route.hash);
      },
      getSymbolHtml(name) {
        return axios.get(context['symbol_html_uri'], {params: {symbol_name: name}}).then((response) => {
          return response.data
        })
      },
      jumpTo(name, anchor) {
        this.getSymbolHtml(name).then((symbolHtml) => {
          this.compiled = Vue.compile(symbolHtml);
          setTimeout(() => {
            anchorName = this.$route.hash.split('#')[1]
            if(anchorName) {
              this.anchorElement = document.getElementsByName(anchorName)[0]
            } else {
              window.scroll({top: 0, behavior: 'smooth'})
            }
          }, 1000);
        })
      }
    },
    watch: {
      $route () {
        this.reload(this.$route.params.name);
      },
      anchorElement(newVal, oldVal) {
        if(oldVal){
          oldVal.style.backgroundColor = "white"
        }
        // #5D9BF7 means default anchor color like blue
        newVal.style.backgroundColor = '#5D9BF7'
        newVal.scrollIntoView()
      }
    },
    template: `
      <v-container id="symbol" fluid>
          <v-row>
              <component :is="compiled"></component>
          </v-row>
      </v-container>`,
    delimiters: ['$(', ')']
}