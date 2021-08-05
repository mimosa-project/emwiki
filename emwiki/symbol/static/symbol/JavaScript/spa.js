const app = Vue.createApp({})
// function getpath(symbolnamne) {
//   console.log(symbolnamne)
//   return '/static/symbol/components/0.vue';
// }
const options = {
  moduleCache: {
    vue: Vue
  },
  async getFile(url) {

    const res = await fetch(url);
    if (!res.ok)
      throw Object.assign(new Error(res.statusText + ' ' + url), { res });
    return {
      getContentData: asBinary => asBinary ? res.arrayBuffer() : res.text(),
    }
  },
  addStyle(textContent) {

    const style = Object.assign(document.createElement('style'), { textContent });
    const ref = document.head.getElementsByTagName('style')[0] || null;
    document.head.insertBefore(style, ref);
  },
}
const { loadModule } = window['vue3-sfc-loader'];

// app.component('symbol', {
//     components: {
//         'my-component': Vue.defineAsyncComponent( () => loadModule('/static/symbol/components/0.vue', options) )
//     },
//     template: '{{this.$route.params.symbolname}}<my-component></my-component>'
// })


const symbol = {
  data() {
    return {
      currentComponent: "/static/symbol/components/0.vue",
    }
  },
  computed: {
    // 算出 getter 関数
    getpath() {
        this.currentComponent  = this.$route.params.symbolname
    }
  },
  components: {
    'my-component': Vue.defineAsyncComponent(() => loadModule(path, options))
  },
  template: '{{this.$route.params.symbolname}}<my-component></my-component>'
}
app.component('symbol',symbol)

const routes = [
  { path: '/symbol/', component: { template: "index" } },
  { path: '/symbol/:symbolname', name: 'symbol', component: symbol }
]

const router = VueRouter.createRouter({
  //history: VueRouter.createWebHistory('configure-admin'),
  history: VueRouter.createWebHistory(),
  routes,
})

app.use(router)
app.mount("#app")

path = this.$refs.symbolv.currentComponent
