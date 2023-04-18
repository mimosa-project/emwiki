export function Escape(html, encode) {
    return html
        .replace(!encode ? /&(?!#?\w+;)/g : /&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

export function PartialDescape(html) {
    //改行ごとにテキストを分割する
    var lines = html.split('\n');
    var out = '';
    var inside_code = false;

    //分割されたテキストごとに処理を行う
    for (var i = 0; i < lines.length; i++) {
        //エスケープされた文字列を元に戻す
        if (lines[i].startsWith('&gt;')) {
            lines[i] = lines[i].replace(/&gt;/g, '>');
        }

        if (inside_code) {
            lines[i] = lines[i]
                .replace(/&lt;/g, '<')
                .replace(/&gt;/g, '>')
                .replace(/&quot;/g, '"')
                .replace(/&#39;/g, '\'');
        }
        if (lines[i].startsWith('```')) {
            inside_code = !inside_code;
        }
        //分割されたテキストを元に戻す
        out += lines[i] + '\n';
    }
    return out;
}