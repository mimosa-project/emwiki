/**
 * A service of Theorem
 */
export class TheoremService {
  /**
   * Search theorem
   * @param {string} url
   * @param {string} searchText
   * @return {Promise<Array>} search results
   */
  static searchTheorem(url, searchText) {
    return axios.get(url, {
      params: {
        search_query: searchText,
      },
    }).then((response) => {
      return response.data;
    });
  }
  /**
   * Record reactions
   * @param {string} url
   * @param {string} csrftoken
   * @param {int} id
   * @param {string} buttonType
   * @return {Promise<Object>} An Object that has a key 'id'
   */
  static recordReactions(url, csrftoken, id, buttonType) {
    const headers = {'X-CSRFToken': csrftoken};
    // content-typeをapplication/x-www-form-urlencodedに変換
    const params = new URLSearchParams();
    params.append('button_type', buttonType);
    params.append('id', id);
    return axios.post(url, params, {headers: headers});
  }
}
