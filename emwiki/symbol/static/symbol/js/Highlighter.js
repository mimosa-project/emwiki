/**
 * Highlighter of symbol
 */
export class Highlighter {
  /**
   * @param {String} s
   * @return {String} escaped string
   */
  escapeText(s) {
    // eslint-disable-next-line max-len
    return s.split('&').join('&amp;').split('<').join('&lt;').split('>').join('&gt;');
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
   * @param {string} symbol
   * @param {String} query
   * @return {String}
   */
  highlightAsIs(symbol, query) {
    const pos = symbol.toLowerCase().indexOf(query);
    return this.highlightSubstring(symbol, pos, query.length);
  };

  /**
   * @param {string} symbol
   * @param {String} query
   * @param {Array<RegExp>} regexps
   * @param {Array<String>} highlighters
   * @return {String}
   */
  highlightQuery(symbol, query, regexps, highlighters) {
    const q = query.split(/\s+/)[0];
    const len = q.length;
    const pos = symbol.toLowerCase().indexOf(q);
    const numberOfRegexps = regexps.length;
    symbol = this.highlightSubstring(symbol, pos, len);
    for (let i = 1; i < numberOfRegexps; i++) {
      symbol = symbol.replace(regexps[i], highlighters[i]);
    }
    return symbol;
  };

  /**
   * @param {String} symbol
   * @param {String} query
   * @return {String} highlighted symbol
   */
  run(symbol, query) {
    query = query.toLowerCase();
    const regexps = this.buildRegexps(query);
    const highlighters = this.buildHighlighters(query);
    let highlighted = '';
    if (symbol.toLowerCase().indexOf(query) === 0) {
      highlighted = this.highlightAsIs(symbol, query);
    } else {
      highlighted = this.highlightQuery(symbol, query, regexps, highlighters);
    }
    return this.escapeText(highlighted)
        .split('\u0001').join('<span class="blue lighten-4">')
        .split('\u0002').join('</span>');
  };
}
