var context = JSON.parse(document.getElementById('context').textContent);
new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    components: {'theorem-view': TheoremView},
    data: () => ({
        drawer: false,
    }),
    delimiters: ['$(', ')']
})
