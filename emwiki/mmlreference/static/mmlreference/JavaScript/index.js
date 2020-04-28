$(function(){
    var filename = JSON.parse(document.getElementById('filename').textContent)['filename'];
    $("#mmlreference-content").load(`mml-contents/${filename} .mml-summary, .mml-element`, null, function(){
        let anchor = location.hash;
        if(anchor !== ''){
            let offset_top = $(anchor).position().top - $(anchor).parent().position().top
            $(anchor).addClass('shadow-lg mx-3 bg-light');
            $('#mmlreference-content').animate({
                scrollTop: offset_top
            }, "slow");
        }
        
        $("#mmlreference-content").on("click", "span[data-link]", function() {
            var link = $(this).attr("data-link");
            window.location.href = `/mmlreference/${link}`
        });

        $("#mmlreference-content").on("click", "span[data-href]", function() {
            var url = $(this).attr("data-href");
            window.location.href = `/article/${url}`
        });

        $("#mmlreference-content .mml-summary").addClass(
            "card m-3"
        )
        $("#mmlreference-content .mml-summary h1").addClass(
            "card-header"
        )
        $("#mmlreference-content .mml-summary h2").addClass(
            "card-body"
        )
        $("#mmlreference-content .mml-summary ol").addClass(
            "card-body ml-3 list-group"
        ) 
        $("#mmlreference-content .mml-summary li").addClass(
            "list-group-item"
        ) 

        $("#mmlreference-content .mml-element").addClass(
            "card m-3"
        )
        $("#mmlreference-content .mml-element h3").addClass(
            "card-body"
        )
        $("#mmlreference-content .mml-element .source-box").addClass(
            "card-body border border-dark m-2"
        )
        $("#mmlreference-content .mml-element h2").addClass(
            "card-header"
        )
    });
});