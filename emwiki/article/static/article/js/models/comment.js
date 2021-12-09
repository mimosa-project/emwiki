import {Editor} from '../models/editor.js';
import {context} from '../../../js/context.js';

/**
 * Comment
 */
export class Comment {
  /**
   * Constructor of Comment
   * @param {Article} article
   * @param {Element} element
   * @param {string} block
   * @param {number} blockOrder
   * @param {string} commentUrl
   */
  constructor(article, element, block, blockOrder, commentUrl) {
    this.article = article;
    this.block = block;
    this.blockOrder = blockOrder;
    this.commentUrl = commentUrl;
    if (block == 'proof') {
      this.element = element.closest('a');
    } else {
      this.element = element;
    }
    this.editor = new Editor(this);
  }

  /** Getter of editor.text */
  get text() {
    return this.editor.text;
  };

  /**
  * Submit comment
  * @param {function} callback
  */
  submit(callback = () => { }) {
    const csrftoken = Cookies.get('csrftoken');
    /**
     * Returns a Boolean value that indicates
     * whether or not a pattern exists in the method.
     * @param {stirng} method
     * @return {Boolean} whether or not a pattern exists in a searched string.
     */
    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
      },
    });
    $.post({
      url: this.commentUrl,
      dataType: 'text',
      data: {
        'article_name': this.article.name,
        'block': this.block,
        'blockOrder': this.blockOrder,
        'comment': this.text,
      },
    }).done(function(data) {
      callback();
    }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
      console.log(XMLHttpRequest, textStatus, errorThrown);
      if (errorThrown === 'Forbidden') {
        alert('Editing is only allowed to registered users\n' +
              'Please login or signup');
      } else {
        alert(`Error: ${textStatus}`);
      }
    });
  }

  /**
   * Bulk fetch
   * @param {Article} article
   * @param {Array} comments
   * @param {string} commentUrl
   */
  static bulkFetch(article, comments, commentUrl = context['comments_uri']) {
    $.get({
      url: commentUrl,
      data: {article_name: article.name},
    }).done((data) => {
      data.forEach((commentFetched) => {
        try {
          // TODO 線形探索をやめる
          const comment = comments.find((comment) => {
            return (
              comment.block === commentFetched.fields.block &&
              comment.blockOrder === commentFetched.fields.blockOrder
            );
          });
          if (comment) {
            comment.editor.text = commentFetched.fields.text;
          }
        } catch (e) {
          console.log(e);
        }
      });
      const editors = comments.map((comment) => comment.editor);
      Editor.bulk_render(editors);
    }).fail((XMLHttpRequest, textStatus, errorThrown) => {
      alert('Failed to get some comment\n' + textStatus);
    });
  }

  /**
   * Fetch a comment
   * @param {string} commentUrl
   */
  fetch(commentUrl = context['comments_uri']) {
    // declarate decause `this` reserved by jQuery in $.get
    const comment = this;
    $.get({
      url: `${commentUrl}`,
      data: {
        article_name: comment.article.name,
        block: comment.block,
        blockOrder: comment.blockOrder,
      },
    }).done(function(data) {
      comment.editor.text = data[0]['fields']['text'];
      comment.editor.render();
    }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
      alert('Failed to get some comment\n' + textStatus);
    });
  }
}
