/**
 * Service of Symbol
 */
export class SymbolService {
  /**
   * Get index data of Symbol
   * @param {string} url
   * @return {Array<Object>} index data
   */
  static getIndex(url) {
    return axios.get(url).then((response) => {
      return response.data.index;
    });
  }

  /**
   * Get HTML string
   * @param {string} url
   * @param {string} name
   * @return {stirng} HTML of symbol
   */
  static getHtml(url, name) {
    return axios.get(url, {params: {symbol_name: name}}).then((response) => {
      return response.data;
    });
  }
}
