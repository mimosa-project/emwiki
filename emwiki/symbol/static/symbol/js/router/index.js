var context = JSON.parse(document.getElementById('context').textContent);
const router = new VueRouter({
  mode: 'history',
  base: context['symbol_base_uri'],
  routes: [
    {
      path: '/:name',
      name: 'Symbol',
      component: SymbolView
    }
  ]
})
