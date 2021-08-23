var context = JSON.parse(document.getElementById('context').textContent);
var jump_to, get_badge;
jump_to = (function (_this) {
  return function (filename, anchor, push_state) {
    if (anchor == null) {
      anchor = null;
    }
    if (push_state == null) {
      push_state = false;
    }
    if (filename != null) {
      return $("#symbol").load(context['symbol_base_uri'] + filename + " .mml-summary, .mml-element", null, function () {
        let offsetTop;
        $(".mml-element").removeClass('selected');
        if (anchor) {
          $("#" + anchor).addClass('selected');
        }
        offsetTop = anchor != null ? $(".selected")[0].offsetTop : 0;
        $('#symbol').animate({scrollTop: offsetTop}, "slow");
        if (push_state) {
          return history.pushState({
            filename: filename,
            anchor: anchor
          }, null, null);
        }
      });
    }
  };
})(this);

get_badge = function (type) {
  let badge;
  switch (type) {
    case 'pred':
      badge = 'warning';
      break;
    case 'struct':
      badge = 'secondary';
      break;
    case 'mode':
      badge = 'success';
      break;
    case 'func':
      badge = 'primary';
      break;
    case 'attr':
      badge = 'danger';
      break;
  }
  return badge;
}

$(document).ready(function () {
  var i, len, li, symbol, type, filename, badge, _i, _ref;
  len = index_data.symbols.length;
  li = [];
  for (i = _i = 0, _ref = len - 1; 0 <= _ref ? _i < _ref : _i > _ref; i = 0 <= _ref ? ++_i : --_i) {
    type = index_data.types[i];
    badge = get_badge(type);
    symbol = escape_txt(index_data.symbols[i]);
    filename = index_data.filenames[i];
    li.push("<button class='list-group-item list-group-item-action py-0 d-flex justify-content-start align-items-center "
      + type + "' data-link='" + filename + "'><span class='badge rounded-pill bg-" + badge + " text-monospace'>"
      + type[0].toUpperCase() + "</span>" + "<span class='text-monospace px-2'> " + symbol + "</span></button>");
  }
  $("#index-listdata").append(li.join(''));
  jump_to(index_data.filenames[0], null, true);
  $("#symbol-name").val(index_data.symbols[0]);
  $("#main").on("click", "button[data-link],span[data-link]", function () {
    let anchor, filename, links, index;
    links = $(this).attr("data-link").split('#');
    filename = links[0];
    anchor = links[1];
    index = index_data.filenames.indexOf(filename)
    $("#symbol-name").val(index_data.symbols[index]);
    return jump_to(filename, anchor, true);
  });
  $("#main").on("click", "span[data-href]", function () {
    let url;
    url = context['article_base_uri'] + $(this).attr("data-href");
    return window.open(url, '_blank').focus();
  });
  $("#search-input").keyup(function () {
    var query, searcher;
    $("#index-listdata").css("display", "none");
    $("#results-listdata").empty();
    query = $(this).val();
    if ((query != null) && query.length > 0) {
      $("#results-listdata").css("display", "block");
      searcher = new Searcher;
      return searcher.run(query);
    } else {
      $("#index-listdata").css("display", "block");
      return $("#results-listdata").css("display", "none");
    }
  });
});

if (window.history && window.history.pushState) {
  $(window).on('popstate', function (event) {
    var state;
    state = event.originalEvent.state;
    if (state != null) {
      return jump_to(state.filename, state.anchor);
    } else {
      jump_to(index_data.filenames[0], null, true);
    }
  });
}
