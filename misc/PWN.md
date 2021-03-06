# PWN

---
## 脆弱性の探し方
* 複雑なロジックを調べる
* 異常系ではなく、正常系において、あまり通らないパスを調べる
  * よく通るパスに脆弱性はない
  * 異常系は、プログラマに異常と認識され、フォローされているが故に問題はない
* 目的の処理の”ついで”に条件判定も行うような関数を調べる
  * ”AのついでにBもする関数”
  * ProcessEphemeronsは、エフェメロンをマーキングし、関数終了時点でまだ処理可能なエフェメロンが存在する場合、trueを返す
  * 存在しない場合、falseを返す関数
  * バグの原因は、処理可能なエフェメロンが存在するのにfalseを返したこと
  * SetPropertyは、プロパティが存在するかどうかを調べて、存在するときにはプロパティをセットし、trueを返す
  * 存在しないときはfalseを返す関数
  * バグの原因は、プロパティが存在するのに、falseを返したこと
* 組み合わせを調べる
  * Turbofanの最適化周りのバグ
* Data構造からソースコードを読む

## Basic

1. 入力値に着目すること
   1. 特に長さやカウントに関わる入力値に着目
   2. それら入力値が正常に検証されているかどうかに着目
2. 脆弱な関数に着目すること（型シグネチャ・関数内チェックなし）
3. 正常な動作を把握すること。そのためには入力と出力と副作用に注目し、コードの裏側の意味を考えること
   1. 動作としてではなく、意味として捉える
   2. 何が期待された出力で、何が異常な出力なのか、それによって何が引き起こされるのかは二の次
   3. 関数の出力（戻り値以外にもポインタや副作用で存在する可能性あり）を整理する
4. 脆弱性の原因と、発火の場所を個別に捉えること


### BOF

1. あるべき変数（入力値）が存在しない
   * 関数の型シグネチャが不正
   * (例1) 例えば、bufferをcopyする関数なのに、bufferの長さを引数に持たない
2. あるべき変数（入力値）が存在する
   1. 入力値の検証がなされていない
      * 入力値の検証がなされないまま、ループの終了条件の変数として利用されている
      * 例えばパケットのlengthフィールドなどを無条件に信頼し、パケットをイテレートするループの終了条件でlengthが利用されている
   2. 入力値の検証がバイパス可能
      * BOFをトリガー可能なパスが成立


### UAF

1. freeを複数回可能な不正なパスが存在
2. 同一のオブジェクトを指す２以上のポインタが存在
3. 特定の領域をfreeした後も、前記領域を指すポインタが残留



## Technics

### User
* アドレスの下位2byteを書き換えることで、アドレスのリークが不可でもエクスプロイトが可能
* Got Overwriteの場合、脆弱性のある関数が呼び出している関数からのROPを考慮に入れる
  putsを書き換え、buf内のROPへ移行

  ```c
  int vuln() {
      char buf[64];
      scanf("%64s", buf);
      printf(buf);
      puts("end");
  }
  ```

* targetのアドレスをレジスタ上に作り出すパターンと、メモリ上に作り出し、csu gadgetでトリガーするパターンがある
* libcの関数を呼び出したのち、スタック上に残留しているアドレスを書き換え、csu gadgetでトリガー
* libcの関数を呼び出したのち、残留しているレジスタを任意の領域に書き込み、書き換え、トリガー
* gadgetはmovだけではなくaddなどもmovの代用としてつかえる
* gadgetはraxだけではなく、eaxなども選択に入れる。aslrは下位4byteが判明すれば、現実的な確率でエクスプロイト可能なため
* aslrでは上位4byteは8bitほどのエントロピー、下位4byteは20bitほどのエントロピー
	* libc: 0x00007fxx xxxxxXXX
	* 下位4byteが推定できれば、上位4byteは1/255の確率であるため現実的
* mmapでallocateしたチャンクのアドレスと、他のdynamic libのアドレスの、相対オフセットは固定

 ### Kernel
* userfaultfdでkernelの特定ページへの書き込みを監視することが可能
* modprobe\_pathを書き換えることで、任意のスクリプトをrootで実行することが可能
  * 不明なmagic numberのバイナリをlinuxが実行(sytemcall : execve)しようとすると、前記magic numberと合致するバイナリフォーマットを探索する過程で、call\_modprobeが呼ばれる。call\_modeprobeは内部で、modeprobe\_pathで指定したバイナリを実行する
  * modprobe\_pathは、カーネルオプションによってはkallsymsには表示されないが、call\_usermodehelper関数の第一引数をデバッガで調べることで求まる
* core\_patternを書き換えることで、プログラムのクラッシュによるコアダンプの作成をトリガーとして、任意のスクリプトをrootで実行することが可能
* syscallでkernelに入ると、swapgsでgsが交換され、交換されたgsからkernel stackのアドレスが取得され、rspにセットされる。のち、レジスタが対比される
* kernelではcr4にSMEP, SMAPのフラグが存在する
* task\_structに、ユーザのクレデンシャルへのポインタが存在する。クレデンシャルはUIDなどを含む。UIDを書き換える、もしくはcommit\_creds(0)を発行することで、rootになれる
* thread\_structに、seccompのフラグが存在する

### links
* [Kernel Exploitで使える構造体集](https://ptr-yudai.hatenablog.com/entry/2020/03/16/165628)
* [kernelpwn](https://github.com/smallkirby/kernelpwn)
