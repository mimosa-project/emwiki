var Searcher, escape_txt;
__bind = function (fn, me) { return function () { return fn.apply(me, arguments); }; };

escape_txt = function (s) {
	return s.split('&').join('&amp;').split('<').join('&lt;').split('>').join('&gt;');
};
var Searcher = (function () {
	function Searcher(articles) {
		this.articles = articles
		this.run = __bind(this.run, this);
		this.update_search_results = __bind(this.update_search_results, this);
		this.search_in_chunk = __bind(this.search_in_chunk, this);
		this.highlight_query = __bind(this.highlight_query, this);
		this.highlight_as_is = __bind(this.highlight_as_is, this);
		this.highlight_substring = __bind(this.highlight_substring, this);
		this.build_highlighters = __bind(this.build_highlighters, this);
		this.match_containing_substrings = __bind(this.match_containing_substrings, this);
		this.match_containing = __bind(this.match_containing, this);
		this.match_containing_as_is = __bind(this.match_containing_as_is, this);
		this.match_beginning_substrings = __bind(this.match_beginning_substrings, this);
		this.match_beginning = __bind(this.match_beginning, this);
		this.match_beginning_as_is = __bind(this.match_beginning_as_is, this);
		this.build_regexps = __bind(this.build_regexps, this);
	}

	Searcher.CHUNK_SIZE = 1000;

	Searcher.MAX_RESULT = 1000;

	Searcher.search_id = 0;

	Searcher.prototype.build_regexps = function (query) {
		var converter, q, queries, _i, _len, _results;
		queries = $.grep(query.split(/\s+/), function (s) {
			return s.match(/\S/);
		});
		converter = function (s) {
			if ("\\*+.?{}()[]^$-|".indexOf(s) !== -1) {
				s = "\\" + s;
			}
			return "([" + s + "])([^" + s + "]*?)";
		};
		_results = [];
		for (_i = 0, _len = queries.length; _i < _len; _i++) {
			q = queries[_i];
			_results.push(new RegExp(q.replace(/(.)/g, converter), 'i'));
		}
		return _results;
	};

	Searcher.prototype.match_beginning_as_is = function (article, query, regexps) {
		return article.toLowerCase().indexOf(query) === 0;
	};

	Searcher.prototype.match_beginning = function (article, query, regexps) {
		var ls, q, r, _i, _len, _ref;
		q = query.split(/\s+/)[0];
		ls = article.toLowerCase();
		if (ls.indexOf(q) !== 0) {
			return false;
		}
		_ref = regexps.slice(1);
		for (_i = 0, _len = _ref.length; _i < _len; _i++) {
			r = _ref[_i];
			if (!ls.match(r)) {
				return false;
			}
		}
		return true;
	};

	Searcher.prototype.match_beginning_substrings = function (article, query, regexps) {
		var i, pos, queries, _i, _ref;
		queries = query.split(/\s+/);
		for (i = _i = 0, _ref = queries.length; 0 <= _ref ? _i < _ref : _i > _ref; i = 0 <= _ref ? ++_i : --_i) {
			pos = article.toLowerCase().indexOf(queries[i]);
			if (i === 0 && pos !== 0) {
				return false;
			} else if (pos < 0) {
				return false;
			}
		}
		return true;
	};

	Searcher.prototype.match_containing_as_is = function (article, query, regexps) {
		return article.toLowerCase().indexOf(query) >= 0;
	};

	Searcher.prototype.match_containing = function (article, query, regexps) {
		var ls, q, r, _i, _len, _ref;
		q = query.split(/\s+/)[0];
		ls = article.toLowerCase();
		if (!(ls.indexOf(q) > 0)) {
			return false;
		}
		_ref = regexps.slice(1);
		for (_i = 0, _len = _ref.length; _i < _len; _i++) {
			r = _ref[_i];
			if (!ls.match(r)) {
				return false;
			}
		}
		return true;
	};

	Searcher.prototype.match_containing_substrings = function (article, query, regexps) {
		var pos, q, queries, _i, _len;
		queries = query.split(/\s+/);
		for (_i = 0, _len = queries.length; _i < _len; _i++) {
			q = queries[_i];
			pos = article.toLowerCase().indexOf(q);
			if (pos < 0) {
				return false;
			}
		}
		return true;
	};

	Searcher.prototype.build_highlighters = function (query) {
		var i, q, queries, _i, _len, _results;
		queries = $.grep(query.split(/\s+/), function (s) {
			return s.match(/\S/);
		});
		_results = [];
		for (_i = 0, _len = queries.length; _i < _len; _i++) {
			q = queries[_i];
			_results.push(((function () {
				var _j, _ref, _results1;
				_results1 = [];
				for (i = _j = 0, _ref = q.length; 0 <= _ref ? _j < _ref : _j > _ref; i = 0 <= _ref ? ++_j : --_j) {
					_results1.push("\u0001$" + (i * 2 + 1) + "\u0002$" + (i * 2 + 2));
				}
				return _results1;
			})()).join(""));
		}
		return _results;
	};

	Searcher.prototype.highlight_substring = function (s, pos, len) {
		return s.slice(0, pos) + "\u0001" + s.slice(pos, pos + len) + "\u0002" + s.slice(pos + len);
	};

	Searcher.prototype.highlight_as_is = function (article, query, regexps, highlighters) {
		var pos;
		pos = article.toLowerCase().indexOf(query);
		return this.highlight_substring(article, pos, query.length);
	};

	Searcher.prototype.highlight_query = function (article, query, regexps, highlighters) {
		var i, len, pos, q, _i, _ref;
		q = query.split(/\s+/)[0];
		len = q.length;
		pos = article.toLowerCase().indexOf(q);
		article = this.highlight_substring(article, pos, len);
		for (i = _i = 1, _ref = regexps.length; 1 <= _ref ? _i < _ref : _i > _ref; i = 1 <= _ref ? ++_i : --_i) {
			article = article.replace(regexps[i], highlighters[i]);
		}
		return article;
	};

	Searcher.prototype.search_in_chunk = function (query, regexps, highlighters, state) {
		var highlighted, hlt_fn, i, j, k, len, match_fn, results, article, _i, _ref, _ref1;
		results = [];
		len = article_names.length;
		for (k = _i = 0, _ref = this.constructor.CHUNK_SIZE; 0 <= _ref ? _i < _ref : _i > _ref; k = 0 <= _ref ? ++_i : --_i) {
			i = state.counter % len;
			j = Math.floor(state.counter / len);
			++state.counter;
			if (j > 4) {
				break;
			}
			if (state[String(i)]) {
				continue;
			}
			_ref1 = (function () {
				switch (j) {
					case 0:
						return [this.match_beginning_as_is, this.highlight_as_is];
					case 1:
						return [this.match_beginning_substrings, this.highlight_query];
					case 2:
						return [this.match_containing_substrings, this.highlight_query];
					case 3:
						return [this.match_beginning, this.highlight_query];
					case 4:
						return [this.match_containing, this.highlight_query];
					default:
						return [null, null];
				}
			}).call(this);
			match_fn = _ref1[0];
			hlt_fn = _ref1[1];
			article = article_names[i];
			if (match_fn(article, query, regexps, highlighters)) {
				state[String(i)] = true;
				highlighted = hlt_fn(article, query, regexps, highlighters);
				results.push({
					"index": i,
					"highlighted": highlighted
				});
				if (++state.matched > this.constructor.MAX_RESULT) {
					break;
				}
			}
		}
		return results;
	};

	Searcher.prototype.update_search_results = function (results) {
		var i, li, result, article, article_name, _i, _len;
		li = [];
		for (_i = 0, _len = results.length; _i < _len; _i++) {
			result = results[_i];
			i = result.index;
			article = escape_txt(result.highlighted).split("\u0001").join("<mark>").split("\u0002").join("</mark>");
			article_name = article_names[i];
			li.push("<button class='list-group-item list-group-item-action py-0 d-flex justify-content-start align-items-center' " + 
			"data-link='" + article_name + ".html'>" + article + "</button>");
		}
		$("#results-listdata").append(li.join(''));
		return
	};

	Searcher.prototype.run = function (query) {
		var highlighters, regexps, runner, state;
		if (query == null) {
			return;
		}
		query = query.toLowerCase();
		regexps = this.build_regexps(query);
		highlighters = this.build_highlighters(query);
		state = {
			"counter": 0,
			"matched": 0,
			"search_id": ++this.constructor.search_id
		};
		runner = (function (_this) {
			return function () {
				var results;
				if (state.search_id !== _this.constructor.search_id) {
					return;
				}
				results = _this.search_in_chunk(query, regexps, highlighters, state);
				_this.update_search_results(results);
				if (state.counter < 5 * article_names.length && state.matched < _this.constructor.MAX_RESULT) {
					return setTimeout(runner, 1);
				}
			};
		})(this);
		return runner();
	};

	return Searcher;

})();