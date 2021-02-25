# HTTP Strict Transport Security(HSTS)
## 概要
サイトへのHTTPを用いた接続を禁止し、HTTPS(TLS, SSL)を用いた接続のみを許可する。

通常、クライアントがHTTPSを用いているサイトにHTTPを用いて接続しようとした場合、サイトはHTTPSのURIにリダイレクトするようにレスポンスする。
この際に、改ざん検知機能のないHTTPを用いていることが脆弱性となる。
また、お気に入り等で毎回HTTPを用いて接続しようとするユーザーは、リダイレクトの回数が増え、危険が高まる。

HSTSは、この危険を初回のみ(または0回)に限定する。
サイトは、HTTPSリクエストが一度でも行われた場合、レスポンスヘッダに`Strict-Transport-Security`ヘッダを追加する。
ブラウザは、`Strict-Transport-Security`ヘッダを受け取った場合、`Strict-Transport-Security`ヘッダに指定された期間(秒数)の間そのドメインへのアクセスをHTTPSのみに限定する。
この期間はブラウザによってそのホストへのHTTP通信がブロックされるため、サイトにHTTPリクエストが発生することはなく、リダイレクトを改ざんされることもない。

最大1年間指定することができ、通常1年間(31536000)指定する。
しかし、将来的に2年間が推奨される事が目標になっている。

Wikipediaが分かり易かった

注意点として、ブラウザに保存されるデータとなる(以後変更が困難)ので、長期間の使用は慎重にしなければならない

## 仕様
+ settings.pyに`SECURE_HSTS_SECONDS = 3600`を追記する
+ settings.pyに`SECURE_HSTS_INCLUDE_SUBDOMAINS = True`を追記する
+ 1時間からテストし、問題がなければ徐々に期間を伸ばしていく
## 参考
+ https://docs.djangoproject.com/en/3.1/ref/middleware/#http-strict-transport-security
+ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
+ https://tools.ietf.org/html/rfc6797
+ https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security

# HTTP Strict Transport Security Preloading
## 概要
HSTSを用いているサイトをブラウザに事前に登録することで、HSTSの初回の危険性を減らす。
ブラウザレベルのサポートであり、まだ標準化されてはいないみたい(要調査)
## 仕様
+ settings.pyに`SECURE_HSTS_PRELOAD = True`を追記する
## 参考
+ https://hstspreload.org/
+ https://docs.djangoproject.com/en/3.1/ref/settings/#secure-hsts-preload
+ https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/Strict-Transport-Security#preloading_strict_transport_security
# Content sniffing
## 概要
## 仕様
+ settings.pyに`SECURE_CONTENT_TYPE_NOSNIFF = True`を追記する
## 参考
+ https://en.wikipedia.org/wiki/Content_sniffing
+ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
+ https://docs.djangoproject.com/en/3.1/ref/middleware/#x-content-type-options-nosniff
+ https://docs.djangoproject.com/en/3.1/ref/settings/#secure-content-type-nosniff
# Man-in-the-middle attack