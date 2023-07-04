# Test
## SimpleTestCase
https://docs.djangoproject.com/ja/3.2/topics/testing/tools/#simpletestcase

unittest.TestCaseのサブクラス
## TransactionTestCase
https://docs.djangoproject.com/ja/3.2/topics/testing/tools/#transactiontestcase

SimpleTestCaseを継承している。
テスト前にデータベースがロールバックされる。
## TestCase
TransactionTestCaseを継承している。

[atomic](https://docs.djangoproject.com/ja/3.2/topics/db/transactions/#django.db.transaction.atomic)ブロックでテストをラップしているので、
初期データの投入などを高速化できる
## LiveServerTestCase
TransactionTestCaseを継承している。

LiveServerでテストできる