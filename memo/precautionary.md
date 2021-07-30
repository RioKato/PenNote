# Precautionary
----

1. タイムスタンプに気をつけること
	* ファイルのタイムスタンプ
	* WebページのCopyRight
	* net user administratorのパスワード最終設定時間
	* uname -a のOSのタイムスタンプ
1. 珍しいもの/見覚えのないもの/違和感のあるものに気をつけること
	* 珍しいファイル名
	* 珍しいエラー出方 / ファジング出力
1. 脆弱性ではなく、予め備わっている正規の機能の悪用を最初に検討すること
	* Shell実行機能
	* Password Reset / Admin権限付与機能
	* PHPテンプレート編集機能
	* Package/ Pluginアップロード機能
1. 異常な入力値を試行する前に、正常な入力値をモディファイした/削ったものを試行すること
    * 正常な入力値がファイル名の場合、拡張子を削ったものを試行
    * 入力値をすべて削ったもの（空文字）を試行
1. URLに注目する/URLの意味解釈を行うこと
	* URLの中の数字
	* 1y、1m、1dなどのパラメータを思わせるキーワード
1. 所有者に気をつけること
	* 所有者とグループが違うファイル
	* ディレクトリの所有者と、ディレクトリ内のファイルの所有者が違うなど
1. suid/sgid/cron/sudoなど特権で実行されるプログラムが見覚えのあるものであっても、既知の脆弱性に気をつけること 
    * screenの脆弱性
    * sudoの脆弱性