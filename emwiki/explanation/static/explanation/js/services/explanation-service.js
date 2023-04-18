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
     * Get HTML of the explanation.
     * @param {string} url
     * @param {int} id
     * @return {Promise}
     */
    static getExplanation(url, id) {
        return axios.get(url, { params: { id: id } }).then((response) => {
            return response.data.title;
        });
    }
};