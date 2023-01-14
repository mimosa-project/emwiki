
export const ExplanationDrawer = {
    data() {
        return {
            explanations: [],
            headers: [{ text: 'title', value: 'title' }],
            queryText: '',
            selectedID: '',
        };
    },
    mounted() {
        axios.get('/explanation/explanation')
            .then((response) => {
                this.explanations = response.data.index;
            })
            .catch(error => console.log(error))
    },
    methods: {
        onExplanationRowClick(row) {
            for (var i = 0; i < this.explanations.length; i++) {
                if (row.id === this.explanations[i].id) {
                    this.selectedID = i;
                }
            }
            location.href = "/explanation/detail/" + this.selectedID;
        },
    },

    template: `
    <div>
        <v-data-table
            :headers="headers"
            :items="explanations"
            :search="queryText"
            :items-per-page="-1"
            item-key="title"
            dense
            :footer-props="{'items-per-page-options': [100, 500, 1000, -1]}"
            @click:row="onExplanationRowClick"
        >
            <template v-slot:item.title="props">
                <p
                    class="mb-0 py-2"
                    v-html="queryText === ''
                        ? props.item.title
                        : props.item.highlightedName"
                >
                </p>
            </template>
        </v-data-table>
    </div>
    `,
    delimiters: ['$(', ')'],
};