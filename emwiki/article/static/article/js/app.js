var context = JSON.parse(document.getElementById('context').textContent);
new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    router,
    components: {'article-drawer': ArticleDrawer, 'theorem-drawer': theoremDrawer},
    data: () => ({
        drawer: true,
        drawerWidth: 256,
    }),
    mounted() {
        if(context['target'] === 'theorem'){
            this.drawerWidth = 512
        }
    },
    delimiters: ['$(', ')']
})
