class ArticleService {
    static getIndex(url) {
        return axios.get(url).then((response) => {
            return response.data.index
        })
    }

    static getHtml(url, name) {
        return axios.get(url, {params: {article_name: name}}).then((response) => {
            return response.data
        })
    }

    static getBib(url, name) {
        return axios.get(url, {params: {article_name: name}}).then((response) => {
            return response.data.bib_text
        })
    }
}
