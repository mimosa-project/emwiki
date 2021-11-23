/* eslint-disable no-unused-vars */
/**
 * A service of Theorem
 */
class TheoremService {
  /**
   * Search theorem
   * @param {string} searchText
   * @return {Array<Object>} search results
   */
  static searchTheorem(searchText) {
    return axios.get(context['search_uri'], {
      params: {
        search_query: searchText,
      },
    }).then((response) => {
      return response.data;
    });
  }
  /**
   * Record reactions
   * @param {int} id
   * @param {string} buttonType
   * @return {Promise<Object>} An Object that has a key 'id'
   */
  static recordReactions(id, buttonType) {
    const csrftoken = Cookies.get('csrftoken');
    const headers = {'X-CSRFToken': csrftoken};
    // content-typeをapplication/x-www-form-urlencodedに変換
    const params = new URLSearchParams();
    params.append('button_type', buttonType);
    params.append('id', id);
    return axios.post(context['search_uri'], params, {headers: headers});
  }
}
