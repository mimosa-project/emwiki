/**
 * Searcher of symbol or Article
 */
export class Searcher {
  /**
   * @param {Array<Object>} items
   * @param {'article'|'symbol'} searchTarget
   */
  constructor(items, searchTarget) {
    this.items = items;
    this.searchTarget = searchTarget;
    this.CHUNK_SIZE = 1000;
    this.MAX_RESULT = 1000;
    this.search_id = 0;
  }

  /**
   * @param {string} query
   * @return {Array<RegExp>}
   */
  buildRegexps(query) {
    const queries = query.split(/\s+/).filter(function(s) {
      return s.match(/\S/);
    });
    const converter = function(s) {
      if ('\\*+.?{}()[]^$-|'.indexOf(s) !== -1) {
        s = '\\' + s;
      }
      return '([' + s + '])([^' + s + ']*?)';
    };
    const results = [];
    const len = queries.length;
    for (let i = 0; i < len; i++) {
      const q = queries[i];
      results.push(new RegExp(q.replace(/(.)/g, converter), 'i'));
    }
    return results;
  };

  /**
   * @param {string} item
   * @param {string} query
   * @param {RegExp} regexps
   * @return {boolean}
   */
  matchBeginningAsIs(item, query, regexps) {
    return item.toLowerCase().indexOf(query) === 0;
  };

  /**
   * @param {string} item
   * @param {string} query
   * @param {RegExp} regexps
   * @return {boolean}
   */
  matchBeginningSubstrings(item, query, regexps) {
    const queries = query.split(/\s+/);
    const len = queries.length;
    for (let i = 0; i < len; i++) {
      const pos = item.toLowerCase().indexOf(queries[i]);
      if (i === 0 && pos !== 0) {
        return false;
      } else if (pos < 0) {
        return false;
      }
    }
    return true;
  };

  /**
   * @param {string} item
   * @param {string} query
   * @param {RegExp} regexps
   * @return {boolean}
   */
  matchContainingSubstrings(item, query, regexps) {
    const queries = query.split(/\s+/);
    const len = queries.length;
    for (let i = 0; i < len; i++) {
      const q = queries[i];
      const pos = item.toLowerCase().indexOf(q);
      if (pos < 0) {
        return false;
      }
    }
    return true;
  };

  /**
   * @param {string} item
   * @param {string} query
   * @param {RegExp} regexps
   * @return {boolean}
   */
  matchBeginning(item, query, regexps) {
    const q = query.split(/\s+/)[0];
    const lowerItem = item.toLowerCase();
    if (lowerItem.indexOf(q) !== 0) {
      return false;
    }
    const ref = regexps.slice(1);
    const len = ref.length;
    for (let i = 0; i < len; i++) {
      const r = ref[i];
      if (!lowerItem.match(r)) {
        return false;
      }
    }
    return true;
  };

  /**
   * @param {string} item
   * @param {string} query
   * @param {RegExp} regexps
   * @return {boolean}
   */
  matchContaining(item, query, regexps) {
    const q = query.split(/\s+/)[0];
    const lowerItem = item.toLowerCase();
    if (!(lowerItem.indexOf(q) > 0)) {
      return false;
    }
    const ref = regexps.slice(1);
    const len = ref.length;
    for (let i = 0; i < len; i++) {
      const r = ref[i];
      if (!lowerItem.match(r)) {
        return false;
      }
    }
    return true;
  };

  /**
   * @param {string} query
   * @param {RegExp} regexps
   * @param {Object} state
   * @return {Array<Object>} results in Chunk
   */
  searchInChunk(query, regexps, state) {
    const results = [];
    const len = this.items.length;
    for (let i = 0; i < this.CHUNK_SIZE; i++) {
      const j = state.counter % len;
      const k = Math.floor(state.counter / len);
      ++state.counter;
      if (k > 4) {
        break;
      }
      if (state[String(j)]) {
        continue;
      }
      const matchFunc = (function() {
        switch (k) {
          case 0:
            return this.matchBeginningAsIs;
          case 1:
            return this.matchBeginningSubstrings;
          case 2:
            return this.matchContainingSubstrings;
          case 3:
            return this.matchBeginning;
          case 4:
            return this.matchContaining;
          default:
            return null;
        }
      }).call(this);
      const item = this.items[j].name;
      if (matchFunc(item, query, regexps)) {
        state[String(j)] = true;
        if (this.searchTarget === 'article') {
          results.push({
            'name': this.items[j].name,
          });
        } else if (this.searchTarget === 'symbol') {
          results.push({
            'name': this.items[j].name,
            'type': this.items[j].type,
          });
        }
        if (++state.matched > this.MAX_RESULT) {
          break;
        }
      }
    }
    return results;
  };

  /**
   * @param {string} query
   * @param {Function} updateSearchResults
   * @return {Function}
   */
  run(query, updateSearchResults) {
    query = query.toLowerCase();
    const regexps = this.buildRegexps(query);
    const state = {
      'counter': 0,
      'matched': 0,
      'search_id': ++this.search_id,
    };
    const runner = (function(_this) {
      return function() {
        if (state.search_id !== _this.search_id) {
          return;
        }
        const resultsInChunk = _this.searchInChunk(query, regexps, state);
        updateSearchResults(resultsInChunk);
        if (state.counter < 5 * _this.items.length &&
          state.matched < _this.MAX_RESULT) {
          return setTimeout(runner, 1);
        }
      };
    })(this);
    return runner();
  };
}
