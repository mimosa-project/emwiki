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
    const headers = {'X-CSRFToken': Cookies.get('csrftoken')};
    const params = new URLSearchParams();
    params.append('article_name', this.article.name);
    params.append('block', this.block);
    params.append('block_order', this.blockOrder);
    params.append('comment', this.text);
    axios.post(this.commentUrl, params, {headers: headers})
        .then(() => {
          callback();
        })
        .catch((error) => {
          alert('Failed to submit comment');
          console.log(error.response);
        });
  }

  /**
   * Bulk fetch
   * @param {Article} article
   * @param {Array} comments
   * @param {string} commentUrl
   */
  static bulkFetch(article, comments, commentUrl = context['comments_uri']) {
    axios.get(commentUrl, {
      params: {article_name: article.name},
    })
        .then((response) => {
          response.data.forEach((commentFetched) => {
            try {
              // TODO 線形探索をやめる
              const comment = comments.find((comment) => {
                return (
                  comment.block === commentFetched.fields.block &&
                  comment.blockOrder === commentFetched.fields.block_order
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
        })
        .catch((error) => {
          alert('Failed to get some comment');
          console.log(error.response);
        });
  }

  /**
   * Fetch a comment
   * @param {string} commentUrl
   */
  fetch(commentUrl = context['comments_uri']) {
    axios.get(commentUrl, {
      params: {
        article_name: this.article.name,
        block: this.block,
        block_order: this.blockOrder,
      },
    })
        .then((response) => {
          this.editor.text = response.data[0]['fields']['text'];
          this.editor.render();
        })
        .catch((error) => {
          alert('Failed to get some comment');
          console.log(error.response);
        });
  }
}
