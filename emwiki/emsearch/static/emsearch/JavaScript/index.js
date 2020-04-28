$(function(){
    function debounce(fn, duration) {
        var timer;
        return function(){
            clearTimeout(timer);
            timer = setTimeout(fn, duration);
        }
    }

    function ajax_search(){
        var search_query = $('#emsearch').val()
        console.log(search_query);
        if(search_query){
            console.log(true);
            $.ajax({
                url: '/search/search',
                type: 'GET',
                data: {'search_query': search_query},
                dataType: 'json',
                timespan: 1000
            }).done( response => {
                console.log(response)
                $('#search_result').empty();
                $('#search_result').append(`<div><span class='h2' id='number_of_results'>${response.search_results.length}</span> results</div>`);
                $('#search_result').append(`
                    <table class="table table-hover mt-3">
                     <thead>
                      <tr class=''>
                        <th scope="col" class='text-center' style='width:10%'>#</th>
                        <th scope="col" class='' style='width:10%'>Category</th>
                        <th scope="col" class='' style='width:70%'>Name</th>
                      </tr>
                      </thead>
                      <tbody id='result-table-body'>
                      </tbody>
                    </table>`
                )
                for(index in response.search_results){
                    let result = response.search_results[index]
                    $('#result-table-body').append(`
                        <tr class='position-relative'>
                            <th scope="row" class='text-center'>${parseInt(index) + 1}</th>
                            <td class="">
                            <span class='category-${result.category} py-1 px-2 rounded-pill'>${ result.category }</span>
                            </td>
                            <td class='position-relative'><a class='stretched-link' href='${ result.link }'>${ result.subject }</a></td>
                        </tr>
                    `);
                }
            })
        }else{
            console.log(false)
            $('#search_result').empty();
        }
    }

    ajax_search();
    $('#emsearch').on('keyup', debounce(ajax_search, 300));
});