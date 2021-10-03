var context = JSON.parse(document.getElementById('context').textContent);
var jump_to;
// ページを切り替える関数
jump_to = (function (_this) {
    return function (filename, anchor, push_state) {
        filename = filename.replace(".html", "")
        if (anchor == null) {
            anchor = null;
        }
        if (push_state == null) {
            push_state = false;
        }
        if (filename != null) {
            return $("#htmlized-mml").load(context['article_base_uri'] + filename, null, function () {
                $("#article-name").text(filename);
                let article = new Article(filename, $("#htmlized-mml"));
                let parser = new Parser(article.element);
                let comments = parser.list_comments(article);
                Comment.bulk_fetch(article, comments, context["comment_uri"]);
                // bibテキストを取得
                $.get({
                    url: context['bib_uri'],
                    data: { article_name: filename }
                })
                    .done(function (respons) {
                        $("#bib-popover").attr("data-bs-content", "<pre>" + respons["bib_text"] + "</pre>");
                        var popover = new bootstrap.Popover(document.getElementById("bib-popover"), { "html": true })
                    }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
                        alert('Failed to get bib text\n' + textStatus);
                    });
                // アンカーの部分にselectedクラスを与え, その位置までスクロールする
                $("#htmlized-mml").removeClass('selected');
                if (anchor) {
                    $("[name=" + anchor + "]").addClass('selected');
                }
                // offsetTopがずれるので関数calculateMisalignmentでズレを計算し引いている
                offsetTop = anchor != null ? ($(".selected")[0].offsetTop - calculateMisalignment()) : 0;
                $('#htmlized-mml').animate({ scrollTop: offsetTop }, "slow");
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

//スクロールのズレを計算する関数
calculateMisalignment = function () {
    hight = $('html').height() - $('#htmlized-mml').height();
    return hight;
}

$(document).ready(function () {
    // サイドバーのボタンを生成
    var i, len, li;
    len = article_names.length;
    li = [];
    for (i = 0; i < len; i++) {
        article_name = article_names[i];
        li.push("<button class='list-group-item list-group-item-action py-0 d-flex justify-content-start align-items-center' " +
            "data-link='" + article_name + ".html'>" + article_name + "</button>");
    }
    $("#index-listdata").append(li.join(''));
    // Symbol, Searchアプリケーションからジャンプしてきた場合, クッキーで指定されたページをロード
    let next = Cookies.get('next-link');
    if (next != null) {
        Cookies.remove('next-link');
        let links, filename, anchor;
        links = next.split('#');
        filename = links[0];
        anchor = links[1];
        jump_to(filename, anchor, true);
    }
    // デフォルト
    else {
        jump_to(article_names[0], null, true);
    }
    // サイドバーのリンクがクリックされた場合
    $("#main").on("click", "button[data-link]", function () {
        let links, filename, anchor;
        links = $(this).attr("data-link").split('#');
        filename = links[0];
        anchor = links[1];
        return jump_to(filename, anchor, true);
    });
    // htmlized_mml内のリンクがクリックされた場合
    $("#main").on("click", "a[href]", function (event) {
        event.preventDefault();
        // proof, refがクリックされた場合はhrefに"javascript:()"という値が入っているので無視する
        if ($(this).attr("href") != "javascript:()") {
            let links, filename, anchor;
            links = $(this).attr("href").split('#');
            filename = links[0];
            anchor = links[1];
            return jump_to(filename, anchor, true);
        }
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

class Article {
    constructor(name, element) {
        this.name = name;
        this.element = element;
    }
}

class Editor {
    constructor(comment) {
        this.comment = comment;
        this.html =
            `<div class='edit'>
          <div class='d-flex flex-row'>
              <button type='button' class='editButton'>
              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
              </button>
              <div class='commentPreviewWrapper flex-fill'>    
                  <div class='commentPreview mathjax' style='display:block'></div>
              </div>
          </div>
          <div class='editcomment' style='display:none'>
              <textarea class='commentTextarea' cols='75' rows='10' wrap='hard'></textarea>
              <div class='toolbar'>
                  <button type='button' class='submitButton'>submit</button>
                  <button type='button' class='cancelButton'>cancel</button>
              </div>
          </div>
      </div>`;
        this.create();
    }

    get text() {
        return this.element.find(".commentTextarea").val();
    }

    set text(text) {
        this.element.find(".commentTextarea").val(text);
    }

    create() {
        let editor = this;
        editor.comment.element.before(editor.html);
        editor.element = editor.comment.element.prev();
        //edit class editButton clicked
        editor.element.find('.editButton').on("click", function (event) {
            if (context["is_authenticated"]) {
                editor.element.find(".editcomment").show();
                editor.element.find(".editButton").hide();
            } else {
                alert("Editing is only allowed to registered users \nPlease login or signup");
            }

            event.stopPropagation();
        });

        //edit class submitButton clicked
        editor.element.find('.submitButton').on("click", function () {
            editor.comment.submit(function () {
                editor.hide();
                editor.comment.fetch();
            });
        });
        //edit class cancelButton clicked
        editor.element.find(".cancelButton").on("click", function () {
            editor.hide();
            editor.comment.fetch();
        });

        //edit class commentTextarea changed
        editor.element.find(".commentTextarea").on("input", function () {
            editor.render();
        });
    }

    hide() {
        this.element.find(".editcomment").hide();
        this.element.find(".editButton").show();
    }

    show() {
        this.element.find(".editcomment").show();
        this.element.find(".editButton").hide();
    }

    render() {
        //convert commentText to HTML for converion to Tex format
        this.element.find(".commentPreview").html(Editor.commentText2html(this.text));
        MathJax.typesetPromise(this.element.find(".commentPreview"));
    }

    static bulk_render(editors) {
        editors.forEach((editor) => {
            editor.element.find(".commentPreview").html(Editor.commentText2html(editor.text));
        })
        MathJax.typesetPromise();
    }

    static commentText2html(commentText) {
        if (commentText === '') {
            return commentText
        }
        let commentText_lines = commentText.split(/\r\n|\r|\n/);
        var html = '';
        for (let index = 0; index < commentText_lines.length; index++) {
            html += `<p>${commentText_lines[index]}</p>`;
        }
        return html
    }
}

class Comment {
    constructor(article, element, block, block_order, comment_url) {
        this.article = article;
        this.block = block;
        this.block_order = block_order;
        this.comment_url = comment_url;
        if (block == 'proof') {
            this.element = element.closest('a')
        } else {
            this.element = element;
        }
        this.editor = new Editor(this);
    }

    get text() {
        return this.editor.text;
    };

    submit(callback = function () { }) {
        var csrftoken = Cookies.get('csrftoken');
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $.post({
            url: this.comment_url,
            dataType: 'text',
            data: {
                'article_name': this.article.name,
                'block': this.block,
                'block_order': this.block_order,
                'comment': this.text
            },
        }).done(function (data) {
            callback();
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest, textStatus, errorThrown)
            if (errorThrown === "Forbidden") {
                alert("Editing is only allowed to registered users \nPlease login or signup");
            } else {
                alert(`Error: ${textStatus}`)
            }
        });
    }

    static bulk_fetch(article, comments, comment_url = context["comment_uri"]) {
        $.get({
            url: comment_url,
            data: { article_name: article.name }
        })
            .done(function (data) {
                data.forEach((comment_fetched) => {
                    try {
                        comments.find((comment) => {
                            return (
                                comment.block === comment_fetched.fields.block &&
                                comment.block_order === comment_fetched.fields.block_order
                            )
                        }).editor.text = comment_fetched.fields.text;
                    } catch (e) {
                        console.log(comment_fetched)
                        console.log(e);
                    }
                })
                let editors = comments.map((comment) => comment.editor);
                Editor.bulk_render(editors);
            }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
                alert('Failed to get some comment\n' + textStatus);
            });
    }

    fetch(comment_url = context["comment_uri"]) {
        // declarate decause `this` reserved by jQuery in $.get
        let comment = this;
        $.get({
            url: `${comment_url}`,
            data: { article_name: comment.article.name, block: comment.block, block_order: comment.block_order },
        }).done(function (data) {
            comment.editor.text = data[0]["fields"]["text"];
            comment.editor.render();
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            alert('Failed to get some comment\n' + textStatus);
        });
    }
}


class Parser {
    constructor($root) {
        this.root = $root;
        this.target_block_names = [
            'definition',
            'theorem',
            'registration',
            'scheme',
            'notation',
        ];
        this.target_CSS_selector = 'span.kw';
    }
    list_comments(article) {
        let comments = [];
        let counter = {}
        this.target_block_names.forEach(function (value) {
            counter[value] = 0;
        });
        for (let target of this.root.find(this.target_CSS_selector)) {
            //sometimes $(target).text() return string like "theorem " so trim()
            let block_name = $(target).text().trim();
            if (this.target_block_names.includes(block_name)) {
                let comment = new Comment(
                    article,
                    $(target),
                    block_name,
                    ++counter[block_name],
                    "comments"
                );
                comments.push(comment);
            }
        };
        return comments
    }
}
