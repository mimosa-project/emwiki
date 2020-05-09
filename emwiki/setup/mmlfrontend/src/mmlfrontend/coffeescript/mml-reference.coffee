escape_txt = (s) ->
  s.split('&').join('&amp;')
   .split('<').join('&lt;')
   .split('>').join('&gt;')

# The following class is referred to Ruby on Rails API Reference
class Searcher
  @CHUNK_SIZE: 1000
  @MAX_RESULT: 1000
  @search_id: 0

  # search
  build_regexps: (query) =>
    queries = $.grep(query.split(/\s+/), (s)->s.match(/\S/))
    converter = (s) ->
      if "\\*+.?{}()[]^$-|".indexOf(s) != -1
        s = "\\" + s
      "([#{s}])([^#{s}]*?)"
    (new RegExp(q.replace(/(.)/g, converter), 'i') for q in queries)

  match_beginning_as_is: (symbol, query, regexps) =>
    symbol.toLowerCase().indexOf(query) == 0

  match_beginning: (symbol, query, regexps) =>
    q = query.split(/\s+/)[0]
    ls = symbol.toLowerCase()
    return false unless ls.indexOf(q) == 0
    for r in regexps[1...]
      return false unless ls.match(r)
    return true

  match_beginning_substrings: (symbol, query, regexps) =>
    queries = query.split(/\s+/)
    for i in [0 ... queries.length]
      pos = symbol.toLowerCase().indexOf(queries[i])
      if i == 0 and pos != 0
        return false
      else if pos < 0
        return false
    return true

  match_containing_as_is: (symbol, query, regexps) =>
    symbol.toLowerCase().indexOf(query) >= 0

  match_containing: (symbol, query, regexps) =>
    q = query.split(/\s+/)[0]
    ls = symbol.toLowerCase()
    return false unless ls.indexOf(q) > 0
    for r in regexps[1...]
      return false unless ls.match(r)
    return true

  match_containing_substrings: (symbol, query, regexps) =>
    queries = query.split(/\s+/)
    for q in queries
      pos = symbol.toLowerCase().indexOf(q)
      if pos < 0
        return false
    return true

  # highlight
  build_highlighters: (query) =>
    queries = $.grep(query.split(/\s+/), (s)->s.match(/\S/))
    ((("\u0001$" + (i*2+1) + "\u0002$" + (i*2+2) for i in [0...q.length]).join("")) for q in queries)

  highlight_substring: (s, pos, len) =>
    return s[0...pos] + "\u0001" + s[pos...pos+len] + "\u0002" + s[pos+len...]

  highlight_as_is: (symbol, query, regexps, highlighters) =>
    pos = symbol.toLowerCase().indexOf(query)
    @highlight_substring(symbol, pos, query.length)

  highlight_query: (symbol, query, regexps, highlighters) =>
    q = query.split(/\s+/)[0]
    len = q.length
    pos = symbol.toLowerCase().indexOf(q)
    symbol = @highlight_substring(symbol, pos, len)
    for i in [1...regexps.length]
      symbol = symbol.replace(regexps[i], highlighters[i])
    return symbol

  # main codes for finding
  search_in_chunk: (query, regexps, highlighters, state) =>
    results = []
    len = index_data.symbols.length
    for k in [0...@constructor.CHUNK_SIZE]
      i = state.counter % len
      j = Math.floor(state.counter / len)
      ++state.counter
      break if j > 4
      continue if state[String(i)]

      [match_fn, hlt_fn] =
        switch j
          when 0 then [@match_beginning_as_is, @highlight_as_is]
          when 1 then [@match_beginning_substrings, @highlight_query]
          when 2 then [@match_containing_substrings, @highlight_query]
          when 3 then [@match_beginning, @highlight_query]
          when 4 then [@match_containing, @highlight_query]
          else [null, null]

      symbol = index_data.symbols[i]
      if match_fn(symbol, query, regexps, highlighters)
        state[String(i)] = true
        highlighted = hlt_fn(symbol, query, regexps, highlighters)
        results.push({"index": i, "highlighted": highlighted})
        break if ++state.matched > @constructor.MAX_RESULT

    return results

  update_search_results: (results) =>
    li = ""
    for result in results
      i = result.index
      t = index_data.types[i]
      s = escape_txt(result.highlighted)
        .split("\u0001").join("<b>")
        .split("\u0002").join("</b>")
      li += "<li data-order='#{i}' class='#{t}'>#{s}</li>"
    $("#result ul").append(li)

  run: (query) =>
    return unless query?
    query = query.toLowerCase()
    regexps = @build_regexps(query)
    highlighters = @build_highlighters(query)
    state = {"counter": 0, "matched": 0, "search_id": ++@constructor.search_id}

    runner = =>
      return if state.search_id != @constructor.search_id
      results = @search_in_chunk(query, regexps, highlighters, state)
      @update_search_results(results)
      if state.counter < 5 * index_data.symbols.length and
         state.matched < @constructor.MAX_RESULT
        setTimeout(runner, 1)
    runner()

jump_to = (filename, anchor = null, push_state = false) =>
  if filename?
    $("#content").load("mml-contents/#{filename} .mml-summary, .mml-element", null, =>
      $(".mml-element").removeClass('selected')
      if anchor
        $("##{anchor}").addClass('selected')

      offsetTop = if anchor? then $(".selected")[0].offsetTop else 0
      $('#content').animate({scrollTop: offsetTop}, "slow");
      if push_state
        history.pushState({filename: filename, anchor: anchor}, null, null)
    )
  else
    $("#content").load("./start.html #start", null, =>
      if push_state
        history.pushState({filename: filename, anchor: anchor}, null, null)
    )

$(document).ready ->
  # prepare index list
  len = index_data.symbols.length
  lists = []
  for i in [0...len-1]
    type = index_data.types[i]
    symbol = escape_txt(index_data.symbols[i])
    lists.push("<li data-order='#{i}' class='#{type}'>#{symbol}</a></li>")
  $("#index ul").append(lists.join(''))

  # prepare content
  jump_to(null)

  $(".select-pain ul").on("click", "li", ->
    i = $(@).attr("data-order")
    filename = index_data.filenames[i]
    jump_to(filename, null, true)
  )

  $("#content").on("click", "span[data-link]", ->
    links = $(@).attr("data-link").split('#')
    filename = links[0]
    anchor = links[1]
    jump_to(filename, anchor, true)
  )

  $("#content").on("click", "span[data-href]", ->
    url = ARTICLE_URL + $(@).attr("data-href")
    window.open(url, '_blank').focus()
  )

  $("#search-box").keyup ->
    $("#result ul").empty()
    query = $(@).val()
    if query? and query.length > 0
      $("#result").css("display", "block")
      searcher = new Searcher
      searcher.run(query)
    else
      $("#result").css("display", "none")

if window.history and window.history.pushState
  $(window).on('popstate', (event) ->
    state = event.originalEvent.state
    if state?
      jump_to(state.filename, state.anchor)
    else
      jump_to(null)
  )


