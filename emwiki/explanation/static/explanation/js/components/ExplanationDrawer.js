export const ExplanationDrawer = {
    data() {
        return {
            explanations: [],
        };
    },
    mounted() {
        axios.get('/explanation/explanation')
            .then((response) => {
                console.log("取得成功", response);
            })

            .catch(error => console.log(error))
    },
    template: `
    <div id="app">
        <p>title</p>
        <ul>
            <li v-for="explanation in explanations">
                $( explanation.title )
            </li>
            
        <ul>
    </div>
    `,
    delimiters: ['$(', ')'],
};