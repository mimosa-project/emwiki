/**
 * escape function.
 * @param {html} html
 * @param {encode} encode
 * @return {html}
 */
export function escape(html, encode) {
  return html
      .replace(!encode ? /&(?!#?\w+;)/g : /&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
}

/**
 * partialDescape function.
 * @param {html} html
 * @return {out}
 */
export function partialDescape(html) {
  // 改行ごとにテキストを分割する
  const lines = html.split('\n');
  let out = '';
  let insideCode = false;

  // 分割されたテキストごとに処理を行う
  for (let i = 0; i < lines.length; i++) {
    // エスケープされた文字列を元に戻す
    if (lines[i].startsWith('&gt;')) {
      lines[i] = lines[i].replace(/&gt;/g, '>');
    }

    if (insideCode) {
      lines[i] = lines[i]
          .replace(/&lt;/g, '<')
          .replace(/&gt;/g, '>')
          .replace(/&quot;/g, '"')
          .replace(/&#39;/g, '\'');
    }
    if (lines[i].startsWith('```')) {
      insideCode = !insideCode;
    }
    // 分割されたテキストを元に戻す
    out += lines[i] + '\n';
  }
  return out;
}
