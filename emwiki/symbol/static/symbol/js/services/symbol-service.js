class SymbolService {
  static getIndex(url) {
    return axios.get(url).then((response) => {
      return response.data.index
    })
  }

  static getHtml(url, name) {
    return axios.get(url, { params: { symbol_name: name } }).then((response) => {
      return response.data
    })
  }
}
