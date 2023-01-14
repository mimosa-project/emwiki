
export const deleteExplanation = {
    data: () => ({
        explanationID: '',
        explanationTitle: '',
        explanationText: '',
        url: '/explanation/explanation',
        deleteurl: '/explanation/detail/',
    }),
    mounted() {
        return axios.get(this.url, {
        }).then((response) => {
            this.explanationID = this.$route.params.id;
            this.explanationTitle = response.data.index[this.explanationID].title;
            this.texplanationText = response.data.index[this.$route.params.id].text;
            return this.explanationID, this.explanationTitle, this.texplanationText;
        })
            .catch(error => console.log(error));
    },
    methods: {
        Explanationdelete() {
            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
            axios.delete(this.deleteurl + this.explanationID + '/delete', {
                id: this.explanationID,
                title: this.explanationTitle,
                text: this.texplanationText,

            })
                .then((response) => {
                    console.log(response);
                    location.href = "/explanation";
                })
                .catch(error => console.log(error))
        },
        reloadDetail_form() {
            this.$router.push({ name: 'Detail', params: { id: this.explanationID } });
            location.reload();
        },

    },
    template: `
    <div class='mt-4'>
        <h1>Delete explanation</h1>
        <p>Do you want to delete explanation?</p>

        <v-form>
            <v-btn class="ma-2" outlined color="green" @click="Explanationdelete()">delete</v-btn>
            <v-btn class="ma-2" outlined color="red" @click="reloadDetail_form()">cancel</v-btn>
        </v-form>


    </div>
    `,
    delimiters: ['$(', ')'],
};