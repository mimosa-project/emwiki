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
