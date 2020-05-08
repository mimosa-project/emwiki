$(function(){
    function debounce(fn, duration) {
        var timer;
        return function(){
            clearTimeout(timer);
            timer = setTimeout(fn, duration);
        }
    }

    function ajax_search(){
        var search_query = $('#emsearch').val();
        var category = $('#category-select').val();
        if(search_query){
            $('#search_result').html(`
                <div class="spinner-border text-primary"  role="status">
                    <span class="sr-only">Loading...</span>
                </div>
            `)
            $.ajax({
                url: '/search/search',
                type: 'GET',
                data: {'search_query': search_query},
                dataType: 'json',
                timespan: 1000
            }).done( response => {
                var result_counter = 0;
                $('#search_result').empty();
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
                    if(category === 'all' || category === result.category){
                        $('#result-table-body').append(`
                            <tr class='position-relative'>
                                <th scope="row" class='text-center'>${parseInt(index) + 1}</th>
                                <td class="">
                                <span class='category-${result.category} py-1 px-2 rounded-pill'>${ result.category }</span>
                                </td>
                                <td class='position-relative'><a class='stretched-link' href='${ result.link }'>${ result.subject }</a></td>
                            </tr>
                        `);
                        result_counter++;
                    }
                }
                $('#search_result').prepend(`<div><span class='h2' id='number_of_results'>${result_counter}</span> results</div>`);
            })
        }else{
            console.log(false)
            $('#search_result').empty();
        }
    }

    ajax_search();
    $('#emsearch').on('keyup', debounce(ajax_search, 300));
    $('#category-select').on('change', ajax_search);
});