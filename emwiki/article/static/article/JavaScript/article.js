var context = JSON.parse(document.getElementById('context').textContent);

$(function () {
    var popover = new bootstrap.Popover(document.getElementById("bib-popover"), { "html": true })
    let article = new Article(context["name"], $("#article"));
    let parser = new Parser(article.element);
    let comments = parser.list_comments(article);
    Comment.bulk_fetch(article, comments);
    // selectedクラスを持つ箇所の位置を取得し, そこまでスクロール
    // ずれるで130を引いている
    offsetTop = $(".selected")[0] != null ? ($(".selected")[0].offsetTop -130) : 0;

    $('#htmlized-mml').animate({ scrollTop: offsetTop }, "slow");
});
