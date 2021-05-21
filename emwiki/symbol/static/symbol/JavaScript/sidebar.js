function search(query, searcher) {
    if ((query != null) && query.length > 0) {
        $("#listdata").empty();
        return searcher.run(query);
    }
}

function input_search_initial_value(searcher) {
    if(Cookies.get('symbol_query')) {
        $("#search-input").val(Cookies.get('symbol_query'));
        return search(Cookies.get('symbol_query'), searcher);
    }
}


$(function(){
	var symbols;
	var searcher;
	if(Cookies.get('symbols') != null) {
		searcher = new Searcher(Cookies.get("symbols"));
		input_search_initial_value(searcher);
	} else {
		$.getJSON(
			context["names_url"],
			function(data){
				symbols = data;
				Cookies.set('symbols', data);
				searcher = new Searcher(data);
				input_search_initial_value(searcher);
			},
		)
	}

	$('#search-input').on('keyup', function(){
		search($('#search-input').val(), searcher);
    })
	$('#search-input').on('change', function(){
		search($('#search-input').val(), searcher);
    })

});