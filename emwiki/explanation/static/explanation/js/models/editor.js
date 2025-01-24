/**
 * Handles keydown events on a textarea, providing custom behaviors such as
 * character pair completion (e.g., parentheses, quotes), tab insertion,
 * and undo functionality.
 *
 * @param {KeyboardEvent} event - The keydown event triggered by the user.
 * @param {HTMLTextAreaElement} object - The textarea element being edited.
 */
export function onTextAreaKeyDown(event, object) {
  // キーコードと入力された文字列
  const keyCode = event.keyCode;
  const keyVal = event.key;

  // カーソル位置
  const cursorPosition = object.selectionStart;
  const leftString = object.value.substr(0, cursorPosition);
  const rightString = object.value.substr(cursorPosition, object.value.length);

  // Undo用の履歴保存
  if (!object.undoStack) {
    object.undoStack = []; // 初期化
  }
  if (event.type === 'keydown' && !(event.ctrlKey && keyCode === 90)) {
    // Ctrl+Z以外のキーで記録
    object.undoStack.push(object.value);
    if (object.undoStack.length > 100) { // 保存履歴を制限
      object.undoStack.shift();
    }
  }

  // タブキーの場合
  if (keyCode === 9) {
    event.preventDefault(); // 元の挙動を止める
    object.value = leftString + '\t' + rightString;
    object.selectionEnd = cursorPosition + 1;
  } else if (keyVal === '$') {
    event.preventDefault();
    object.value = leftString + '$$' + rightString;
    object.selectionEnd = cursorPosition + 1;
  } else if (keyVal === '{') {
    event.preventDefault();
    object.value = leftString + '{}' + rightString;
    object.selectionEnd = cursorPosition + 1;
  } else if (keyVal === '[') {
    event.preventDefault();
    object.value = leftString + '[]' + rightString;
    object.selectionEnd = cursorPosition + 1;
  } else if (keyVal === '"') {
    event.preventDefault();
    object.value = leftString + '""' + rightString;
    object.selectionEnd = cursorPosition + 1;
  } else if (keyVal === '(') {
    event.preventDefault();
    object.value = leftString + '()' + rightString;
    object.selectionEnd = cursorPosition + 1;
  } else if (keyVal === '\u0027') { // シングルクォート補完
    event.preventDefault();
    object.value = leftString + '\u0027\u0027' + rightString;
    object.selectionEnd = cursorPosition + 1; // カーソルを最初の ' の後ろに移動
  }

  // Ctrl+Z（Undo）を処理
  if (event.ctrlKey && keyCode === 90) {
    event.preventDefault();
    if (object.undoStack && object.undoStack.length > 0) {
      object.value = object.undoStack.pop(); // 前の状態に戻す
      object.selectionStart = object.selectionEnd = cursorPosition; // カーソル位置を維持
    }
  }
}
