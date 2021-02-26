# XSS
## 概要
Webアプリケーションの脆弱性。
攻撃者の作成したスクリプトを、脆弱性のある標的サイトのドメイン権限において閲覧者のブラウザで実行させる攻撃。
リクエストにあるデータをそのまま表示している(エコーバック)があるときに注意。

## 参考
+ https://ja.wikipedia.org/wiki/%E3%82%AF%E3%83%AD%E3%82%B9%E3%82%B5%E3%82%A4%E3%83%88%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%97%E3%83%86%E3%82%A3%E3%83%B3%E3%82%B0

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

## 対策
+ settings.pyに`SECURE_HSTS_SECONDS = 3600`を追記する
+ settings.pyに`SECURE_HSTS_INCLUDE_SUBDOMAINS = True`を追記する
+ settings.pyに`SECURE_SSL_REDIRECT = True`を追記する
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
## 対策
+ settings.pyに`SECURE_HSTS_PRELOAD = True`を追記する
## 参考
+ https://hstspreload.org/
+ https://docs.djangoproject.com/en/3.1/ref/settings/#secure-hsts-preload
+ https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/Strict-Transport-Security#preloading_strict_transport_security
# Content sniffing
## 概要
ユーザーがアップロードしたファイルをブラウザで表示する際に、ブラウザが自動的にファイル形式を判断する時がある。これはつまり、悪意のあるユーザーによってアップロードファイルが悪意のある形式で表示されてしまう時がある。
HTTPのレスポンスにX-Content-Type-Optionsヘッダをつけることで、MIME(Multipurpose Internet Mail Extensions)タイプを変更せずに従うべきであることをブラウザに伝えることができる。
## 対策
+ settings.pyに`SECURE_CONTENT_TYPE_NOSNIFF = True`を追記する
## 参考
+ https://en.wikipedia.org/wiki/Content_sniffing
+ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
+ https://docs.djangoproject.com/en/3.1/ref/middleware/#x-content-type-options-nosniff
+ https://docs.djangoproject.com/en/3.1/ref/settings/#secure-content-type-nosniff
+ https://developer.mozilla.org/ja/docs/Web/HTTP/Basics_of_HTTP/MIME_types
# Cookie関連
## 概要
ブラウザは、セッションクッキーとCSRFクッキーをHTTPS接続時のみに限定する
## 対策
+ settings.pyに`SESSION_COOKIE_SECURE = True`を追記する
+ settings.pyに`CSRF_COOKIE_SECURE = True`を追記する
## 参考
+ https://docs.djangoproject.com/en/3.1/ref/settings/#session-cookie-secure
+ https://docs.djangoproject.com/en/3.1/ref/settings/#csrf-cookie-secure
# X-XSS-Protection
## 概要
HTTPのX-XSS-Protectionヘッダは、IE, Chrome, Safariの機能で、XSSを検出した際にページ読み込みを停止するためのもの。
インラインJavaScriptの使用を無効にしていれば、現在のブラウザいおいては不要
[Content-Security-Policy](#Content-Security-Policy)に対応していない古いブラウザであれば有効
## 対策
+ settings.pyに`SECURE_BROWSER_XSS_FILTER = True`を追記する
## 参考
+ https://docs.djangoproject.com/en/3.1/ref/settings/#secure-browser-xss-filter
+ https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/X-XSS-Protection
# Content-Security-Policy
## 概要
XSSからの保護に役立つ。
サイトは、クライアントが特定のページにロードできるリソースを制御することができるようになる。
[unsafe-inline](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy#unsafe_keyword_values)を適用することで、X-XSS-Protectionと同じ効果を適用することができる。
Django標準機能ではないが、インラインJSは削除されているらしい。[release 1.10](https://docs.djangoproject.com/en/3.1/releases/1.10/#minor-features)
ライブラリも存在する[django-csp](https://django-csp.readthedocs.io/en/latest/)
## 参考
+ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
# X-Frame-Options
## 概要
クリックジャギング攻撃を防ぐために使用する事ができる。
## 対策
+ settings.pyの`MIDDLEWARE`に` 'django.middleware.clickjacking.XFrameOptionsMiddleware'`を追加する
+ settings.pyに`X_FRAME_OPTIONS = "DENY"`を追記する
  + `"DENY"`: サイトはページをフレームに表示することができない
  + `"SAMEORIGIN"`: 同じORIGIN(ブラウザ毎に判断している)のページであれば表示可能、それ以外不可能
## 参考
+ https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/X-Frame-Options
# クリックジャッキング
## 概要
悪意のあるサイトが、ユーザーに誤った操作を生じさせる攻撃。
iframe等のフレーム内にボタンを設定し、iframeであることが分からないようにStyleし、元々あるボタンにかぶせて表示させる事で、ユーザーが元々あるボタンを押したつもりでも、実際にはiframe内のボタンを押したことになり、悪意のあるリクエストが送られる。
## 対策
+ [X-Frame-Options](#X-Frame-Options)を設定する
## 参考
+ https://docs.djangoproject.com/ja/2.1/ref/clickjacking/#module-django.middleware.clickjacking
+ https://ja.wikipedia.org/wiki/%E3%82%AF%E3%83%AA%E3%83%83%E3%82%AF%E3%82%B8%E3%83%A3%E3%83%83%E3%82%AD%E3%83%B3%E3%82%B0
# Man-in-the-middle attack