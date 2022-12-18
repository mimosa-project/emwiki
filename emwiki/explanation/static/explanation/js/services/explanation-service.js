/**
 * A service of Explanation
 */
export class ExplanationService {
    /**
   * Get index data.
   * @param {string} url url of index API.
   * @return {Promise} index data.
   */
    static getIndex(url) {
        return axios.get(url).then((response) => {
            return response.data.index;
        });
    }

    /**
     * Get HTML of the article.
     * @param {string} url
     * @param {string} name
     * @return {Promise}
     */
    static getHtml(url, name) {
        return axios.get(url, { params: { article_name: name } }).then((response) => {
            return response.data;
        });
    }
};