import {context} from '../../../js/context.js';

/* eslint-disable max-len */
/**
 * Editor
 */
export class Editor {
  /**
   * Constructor of Editor
   * @param {Comment} comment
   */
  constructor(comment) {
    this.comment = comment;
    this.html =
      `<div class='edit'>
          <div class='d-flex flex-row'>
              <button type='button' class='editButton'>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="12"
                height="12"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="feather feather-edit">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
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

  /** Getter of comment text */
  get text() {
    return this.element.find('.commentTextarea').val();
  }

  /**
   * Setter of comment text
   * @param {string} text
   */
  set text(text) {
    this.element.find('.commentTextarea').val(text);
  }

  /**
   * Create Elements and Events
   */
  create() {
    const editor = this;
    editor.comment.element.before(editor.html);
    editor.element = editor.comment.element.prev();
    // edit class editButton clicked
    editor.element.find('.editButton').on('click', function(event) {
      if (context['is_authenticated']) {
        editor.element.find('.editcomment').show();
        editor.element.find('.editButton').hide();
      } else {
        alert('Editing is only allowed to registered users \n' +
              'Please login or signup');
      }

      event.stopPropagation();
    });

    // edit class submitButton clicked
    editor.element.find('.submitButton').on('click', function() {
      editor.comment.submit(function() {
        editor.hide();
        editor.comment.fetch();
      });
    });
    // edit class cancelButton clicked
    editor.element.find('.cancelButton').on('click', function() {
      editor.hide();
      editor.comment.fetch();
    });

    // edit class commentTextarea changed
    editor.element.find('.commentTextarea').on('input', function() {
      editor.render();
    });
  }

  /**
   * Hide editor
   */
  hide() {
    this.element.find('.editcomment').hide();
    this.element.find('.editButton').show();
  }

  /**
   * Show editor
   */
  show() {
    this.element.find('.editcomment').show();
    this.element.find('.editButton').hide();
  }

  /**
   * Render input text to html text
   */
  render() {
    // convert commentText to HTML for converion to Tex format
    this.element
        .find('.commentPreview')
        .html(Editor.commentText2html(this.text));
    MathJax.typesetPromise(this.element.find('.commentPreview'));
  }

  /**
   * Bulk render input text to html text
   * @param {Array<Editor>} editors
   */
  static bulk_render(editors) {
    editors.forEach((editor) => {
      editor.element
          .find('.commentPreview')
          .html(Editor.commentText2html(editor.text));
    });
    MathJax.typesetPromise();
  }

  /**
   * Convert commnet raw text to html string
   * @param {string} commentText
   * @return {string} HTML string of commentText
   */
  static commentText2html(commentText) {
    if (commentText === '') {
      return commentText;
    }
    const commentTextLines = commentText.split(/\r\n|\r|\n/);
    let html = '';
    for (let index = 0; index < commentTextLines.length; index++) {
      html += `<p>${commentTextLines[index]}</p>`;
    }
    return html;
  }
}
