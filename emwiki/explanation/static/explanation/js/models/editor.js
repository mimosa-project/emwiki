export function onTextAreaKeyDown(event, object) {
    // キーコードと入力された文字列
    var keyCode = event.keyCode;
    var keyVal = event.key;

    // カーソル位置
    var cursorPosition = object.selectionStart;
    // カーソルの左右の文字列値
    var leftString = object.value.substr(0, cursorPosition);
    var rightString = object.value.substr(cursorPosition, object.value.length);

    // タブキーの場合
    if (keyCode === 9) {
        event.preventDefault();  // 元の挙動を止める
        // textareaの値をカーソル左の文字列 + タブスペース + カーソル右の文字列にする
        object.value = leftString + "\t" + rightString;
        // カーソル位置をタブスペースの後ろにする
        object.selectionEnd = cursorPosition + 1;
    }
    // '$'マークの場合
    if (keyCode === 52) {
        event.preventDefault();
        object.value = leftString + "$$" + rightString;
        object.selectionEnd = cursorPosition + 1;
    }
    // かぎかっこの場合
    else if (keyVal === "{") {
        event.preventDefault();
        object.value = leftString + "{}" + rightString;
        object.selectionEnd = cursorPosition + 1;
    }
    // かっこの場合
    else if (keyVal === "[") {
        event.preventDefault();
        object.value = leftString + "[]" + rightString;
        object.selectionEnd = cursorPosition + 1;
    }
    // ダブルクオートの場合
    else if (keyCode === 50) {
        event.preventDefault();
        object.value = leftString + '""' + rightString;
        object.selectionEnd = cursorPosition + 1;
    }
    // シングルクオートの場合
    else if (keyCode === 55) {
        event.preventDefault();
        object.value = leftString + "''" + rightString;
        object.selectionEnd = cursorPosition + 1;
    }
}