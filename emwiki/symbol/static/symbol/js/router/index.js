const router = new VueRouter({
  mode: 'history',
  base: '/symbol/',
  routes: [
    {
      path: '/:name',
      name: 'Symbol',
      component: SymbolView
    }
  ]
})
