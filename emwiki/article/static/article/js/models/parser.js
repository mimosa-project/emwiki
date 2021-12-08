import {Comment} from './comment.js';
/**
 * Parser
 */
export class Parser {
  /**
   * Constructor of Parser
   * @param {Element} $root
   */
  constructor($root) {
    this.root = $root;
    this.targetBlockNames = [
      'definition',
      'theorem',
      'registration',
      'scheme',
      'notation',
    ];
    this.targetCssSelector = 'span.kw';
  }

  /**
   * List commnets of article
   * @param {Article} article article
   * @param {String} commentsUri
   * @return {Array<Comment>} comments
   */
  list_comments(article, commentsUri) {
    const comments = [];
    const counter = {};
    this.targetBlockNames.forEach((value) => {
      counter[value] = 0;
    });
    for (const target of this.root.find(this.targetCssSelector)) {
      // sometimes $(target).text() return string like "theorem " so trim()
      const blockName = $(target).text().trim();
      if (this.targetBlockNames.includes(blockName)) {
        const comment = new Comment(
            article,
            $(target),
            blockName,
            ++counter[blockName],
            commentsUri,
        );
        comments.push(comment);
      }
    };
    return comments;
  }
}
