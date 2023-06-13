/**
 * A service of Explanation
 */
export class ExplanationService {
  /**
   * Get title.
   * @param {string} url url of title API.
   * @return {Promise} title.
   */
  static getTitle(url) {
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
  static getText(url) {
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
  static getArticle(url, name) {
    return axios.get(url,
        {params: {article_name: name}},
    ).then((response) => {
      console.log(response);
      return response;
    });
  }
};
