$(function() {
    var context = JSON.parse(document.getElementById('context').textContent);

    $listdata = $('#listdata')
    $.getJSON(
        context['names_url'],
        function(data){
            $.each(data, function(index, article){
                $listdata.append(
                    `<a class="list-group-item list-group-item-action py-0" 
                        href="${article.pk}">
                        ${article.pk}
                    </a>`
                )
            })
        }
    )

    $("#listdata").searcher({
        itemSelector: "a",
        textSelector:  "", // the text is within the item element (li) itself
        inputSelector: "#search-input"
    });
});