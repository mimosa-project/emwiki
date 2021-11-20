var context = JSON.parse(document.getElementById('context').textContent);
new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    router,
    components: {'symbol-drawer': SymbolDrawer},
    data: () => ({
        drawer: true,
        drawerWidth: 256
    }),
    delimiters: ['$(', ')']
})
