$(window).on('load resize', function(){
    var height = $('.navbar').innerHeight();
    $('main').css('padding-top',height); 
});