class TheoremService {
    static async searchTheorem (searchText) {
      return axios.get(context['search_uri'], {
        params: {
          search_query: searchText
        }
      }).then((response) => {
        return response.data
      })
    }
  
    static async recordLoading (id) {
      const csrftoken = Cookies.get('csrftoken')
      const headers = {'X-CSRFToken': csrftoken}
      // content-typeをapplication/x-www-form-urlencodedに変換
      const params = new URLSearchParams()
      params.append('button_type', 'url')
      params.append('id', id + '')
      return await axios.post(context['search_uri'], params, {headers: headers})
    }
  
    static async recordFavorite (id) {
      const csrftoken = Cookies.get('csrftoken')
      const headers = {'X-CSRFToken': csrftoken}
      const params = new URLSearchParams()
      params.append('button_type', 'fav')
      params.append('id', id + '')
      await axios.post(context['search_uri'], params, {headers: headers})
    }
  }