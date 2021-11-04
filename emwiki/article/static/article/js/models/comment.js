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

    static bulk_fetch(article, comments, comment_url = context["comments_uri"]) {
        $.get({
            url: comment_url,
            data: { article_name: article.name }
        })
            .done(function (data) {
                data.forEach((comment_fetched) => {
                    try {
                        const comment = comments.find((comment) => {
                            return (
                                comment.block === comment_fetched.fields.block &&
                                comment.block_order === comment_fetched.fields.block_order
                            )
                        })
                        if(comment){
                            comment.editor.text = comment_fetched.fields.text;
                        }
                    } catch (e) {
                        console.log(e);
                    }
                })
                let editors = comments.map((comment) => comment.editor);
                Editor.bulk_render(editors);
            }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
                alert('Failed to get some comment\n' + textStatus);
            });
    }

    fetch(comment_url = context["comments_uri"]) {
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