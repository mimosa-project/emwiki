/**
 * @typedef {Object} Article
 * @property {string} name
 */
/**
 * @typedef {Object} Symbol
 * @property {String} name
 * @property {String} type
 */
/**
 * Searcher of symbol or Article
 */
export class Searcher {
  /**
   * @param {Array<Article|Symbol>} articleOrSymbolArray
   * @param {'article'|'symbol'} searchTarget
   */
  constructor(articleOrSymbolArray, searchTarget) {
    this.articleOrSymbolArray = articleOrSymbolArray;
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
   * @param {String} s
   * @return {String} escaped string
   */
  escapeText(s) {
    // eslint-disable-next-line max-len
    return s.split('&').join('&amp;').split('<').join('&lt;').split('>').join('&gt;');
  }

  // Search
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

  // highlight
  /**
   * @param {string} query
   * @return {Array<String>}
   */
  buildHighlighters(query) {
    const queries = query.split(/\s+/).filter(function(s) {
      return s.match(/\S/);
    });
    const results = [];
    const numberOfQueries = queries.length;
    for (let i = 0; i < numberOfQueries; i++) {
      const query = queries[i];
      results.push(((function() {
        const ref = [];
        const len = query.length;
        for (let j = 0; j < len; j++) {
          ref.push('\u0001$' + (j * 2 + 1) + '\u0002$' + (j * 2 + 2));
        }
        return ref;
      })()).join(''));
    }
    return results;
  };

  /**
   * @param {string} s
   * @param {Number} pos
   * @param {Number} len
   * @return {String}
   */
  highlightSubstring(s, pos, len) {
    // eslint-disable-next-line max-len
    return s.slice(0, pos) + '\u0001' + s.slice(pos, pos + len) + '\u0002' + s.slice(pos + len);
  };

  /**
   * @param {string} item
   * @param {String} query
   * @param {Array<RegExp>} regexps
   * @param {Array<String>} highlighters
   * @return {String}
   */
  highlightAsIs(item, query, regexps, highlighters) {
    const pos = item.toLowerCase().indexOf(query);
    return this.highlightSubstring(item, pos, query.length);
  };

  /**
   * @param {string} item
   * @param {String} query
   * @param {Array<RegExp>} regexps
   * @param {Array<String>} highlighters
   * @return {String}
   */
  highlightQuery(item, query, regexps, highlighters) {
    const q = query.split(/\s+/)[0];
    const len = q.length;
    const pos = item.toLowerCase().indexOf(q);
    const numberOfRegexps = regexps.length;
    item = this.highlightSubstring(item, pos, len);
    for (let i = 1; i < numberOfRegexps; i++) {
      item = item.replace(regexps[i], highlighters[i]);
    }
    return item;
  };

  // main codes for finding
  /**
   * @param {string} query
   * @param {RegExp} regexps
   * @param {Array<String>} highlighters
   * @param {Object} state
   * @return {Array<Object>} results in Chunk
   */
  searchInChunk(query, regexps, highlighters, state) {
    const results = [];
    const len = this.articleOrSymbolArray.length;
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
      const [matchFunc, highlightFunc] = (function() {
        switch (k) {
          case 0:
            return [this.matchBeginningAsIs, this.highlightAsIs];
          case 1:
            return [this.matchBeginningSubstrings, this.highlightQuery];
          case 2:
            return [this.matchContainingSubstrings, this.highlightQuery];
          case 3:
            return [this.matchBeginning, this.highlightQuery];
          case 4:
            return [this.matchContaining, this.highlightQuery];
          default:
            return null;
        }
      }).call(this);
      const item = this.articleOrSymbolArray[j].name;
      if (matchFunc(item, query, regexps)) {
        state[String(j)] = true;
        // eslint-disable-next-line max-len
        const highlightedName = this.escapeText(highlightFunc.bind(this)(this.articleOrSymbolArray[j].name, query, regexps, highlighters))
            .split('\u0001').join('<span class="blue lighten-4">')
            .split('\u0002').join('</span>');
        if (this.searchTarget === 'article') {
          results.push({
            'name': this.articleOrSymbolArray[j].name,
            'highlightedName': highlightedName,
          });
        } else if (this.searchTarget === 'symbol') {
          results.push({
            'name': this.articleOrSymbolArray[j].name,
            'highlightedName': highlightedName,
            'type': this.articleOrSymbolArray[j].type,
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
   * @param {Function} setResults
   * @param {Function} pushResults
   * @return {Function}
   */
  run(query, setResults, pushResults) {
    query = query.toLowerCase();
    const regexps = this.buildRegexps(query);
    const highlighters = this.buildHighlighters(query);
    const state = {
      'counter': 0,
      'matched': 0,
      'search_id': ++this.search_id,
    };
    // search_idを更新した後にresultsを初期化する
    setResults([]);
    if (query === '') {
      setResults(this.articleOrSymbolArray);
      return;
    }
    const runner = (function(_this) {
      return function() {
        if (state.search_id !== _this.search_id) {
          return;
        }
        pushResults(_this.searchInChunk(query, regexps, highlighters, state));
        if (state.counter < 5 * _this.articleOrSymbolArray.length &&
          state.matched < _this.MAX_RESULT) {
          return setTimeout(runner, 1);
        }
      };
    })(this);
    return runner();
  };
}
