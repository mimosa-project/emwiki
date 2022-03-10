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
    return this.element.getElementsByClassName('commentTextarea')[0]?.value;
  }

  /**
   * Setter of comment text
   * @param {string} text
   */
  set text(text) {
    const commentTextarea = this.element.getElementsByClassName('commentTextarea')[0];
    if (commentTextarea) {
      commentTextarea.value = text;
    }
  }

  /**
   * Create Elements and Events
   */
  create() {
    this.comment.element.insertAdjacentHTML('beforebegin', this.html);
    this.element = this.comment.element.previousElementSibling;
    const editButton = this.element.getElementsByClassName('editButton')[0];
    // edit class editButton clicked
    if (editButton) {
      editButton.addEventListener('click', (event) => {
        if (context['is_authenticated']) {
          const editcomment = this.element.getElementsByClassName('editcomment')[0];
          if (editcomment) {
            editcomment.style.display = 'block';
          }
          editButton.style.display = 'none';
        } else {
          alert('Editing is only allowed to registered users \n' +
                'Please login or signup');
        }
        event.stopPropagation();
      });
    }

    // edit class submitButton clicked
    const submitButton = this.element.getElementsByClassName('submitButton')[0];
    if (submitButton) {
      submitButton.addEventListener('click', () => {
        this.comment.submit(() => {
          this.hide();
          this.comment.fetch();
        });
      });
    }
    // edit class cancelButton clicked
    const cancelButton = this.element.getElementsByClassName('cancelButton')[0];
    if (cancelButton) {
      cancelButton.addEventListener('click', () => {
        this.hide();
        this.comment.fetch();
      });
    }

    // edit class commentTextarea changed
    const debounce = (func, wait = 500) => {
      let timerId;
      return (...args) => {
        if (timerId) {
          clearTimeout(timerId);
        }
        timerId = setTimeout(() => {
          func.apply(...args);
        }, wait);
      };
    };
    this.element.getElementsByClassName('commentTextarea')[0]?.addEventListener('input', debounce(async () => await this.render()));
  }

  /**
   * Hide editor
   */
  hide() {
    const editcomment = this.element.getElementsByClassName('editcomment')[0];
    if (editcomment) {
      editcomment.style.display = 'none';
    }
    const editButton = this.element.getElementsByClassName('editButton')[0];
    if (editButton) {
      editButton.style.display = 'block';
    }
  }

  /**
   * Show editor
   */
  show() {
    const editcomment = this.element.getElementsByClassName('editcomment')[0];
    if (editcomment) {
      editcomment.style.display = 'block';
    }
    const editButton = this.element.getElementsByClassName('editButton')[0];
    if (editButton) {
      editButton.style.display = 'none';
    }
  }

  /**
   * Render input text to html text
   */
  async render() {
    // convert commentText to HTML for conversion to Tex format
    const commentPreview = this.element.getElementsByClassName('commentPreview')[0];
    if (commentPreview) {
      commentPreview.innerHTML = Editor.commentText2html(this.text);
      // typesetPromise takes a HTMLCollection as an argument
      await MathJax.typesetPromise(this.element.getElementsByClassName('commentPreview'));
    }
  }

  /**
   * Bulk render input text to html text
   * @param {Array<Editor>} editors
   */
  static async bulk_render(editors) {
    editors.forEach((editor) => {
      const commentPreview = editor.element.getElementsByClassName('commentPreview')[0];
      if (commentPreview) {
        commentPreview.innerHTML = Editor.commentText2html(editor.text);
      }
    });
    await MathJax.typesetPromise();
  }

  /**
   * Convert comment raw text to html string
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
