/**
 * completion function.
 * @param {event} event
 * @param {object} object
 *
 */
export function onTextAreaKeyDown(event, object) {
  // キーコードと入力された文字列
  const keyCode = event.keyCode;
  const keyVal = event.key;

  // カーソル位置
  const cursorPosition = object.selectionStart;
  // カーソルの左右の文字列値
  const leftString = object.value.substr(0, cursorPosition);
  const rightString = object.value.substr(cursorPosition,
    object.value.length);

  // タブキーの場合
  if (keyCode === 9) {
    event.preventDefault();// 元の挙動を止める
    // textareaの値をカーソル左の文字列 + タブスペース + カーソル右の文字列にする
    object.value = leftString + '\t' + rightString;
    // カーソル位置をタブスペースの後ろにする
    object.selectionEnd = cursorPosition + 1;
  }
  // $マークの場合
  if (keyVal === '$') {
    event.preventDefault();
    object.value = leftString + '$$' + rightString;
    object.selectionEnd = cursorPosition + 1;
  }
  // {の場合 
  else if (keyVal === '{') {
    event.preventDefault();
    object.value = leftString + '{}' + rightString;
    object.selectionEnd = cursorPosition + 1;
  }
  // [の場合
  else if (keyVal === '[') {
    event.preventDefault();
    object.value = leftString + '[]' + rightString;
    object.selectionEnd = cursorPosition + 1;
  }
  // "の場合
  else if (keyVal === '"') {
    event.preventDefault();
    object.value = leftString + '""' + rightString;
    object.selectionEnd = cursorPosition + 1;
  }
}
