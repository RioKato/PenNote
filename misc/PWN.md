# PWN

---
## Basic

1. 入力値に着目すること
   1. 特に長さやカウントに関わる入力値に着目
   2. それら入力値が正常に検証されているかどうかに着目
2. 脆弱な関数に着目すること（型シグネチャ・関数内チェックなし）


### BOF

1. 入力値の検証がなされていない
   * 入力値の検証がなされないまま、ループの終了条件の変数として利用されている
   * 例えばパケットのlengthフィールドなどを無条件に信頼し、パケットをイテレートするループの終了条件でlengthが利用されている
2. 入力値の検証がバイパス可能
   * BOFをトリガー可能なパスが成立
3. 関数の型シグネチャが不正
   * (例1) 例えば、bufferをcopyする関数なのに、bufferの長さを引数に持たない
4. 関数の型シグネチャは正しいが、関数の内部で入力値の検証が十分になされていない。
   したがって、前記関数の呼び出し側で入力値の検証がなされる必要があるが、呼び出し側でも検証が行われていない
   * (例1) パケットをパースする関数の内部で、パケットのフィールドであるlengthやcountが検証されていない
     更には呼び出し側でも検証がなされていない


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
  
 ### Kernel
* userfaultfdでkernelの特定ページへの書き込みを監視することが可能
* modprobe_pathを書き換えることで、任意のスクリプトをrootで実行することが可能
  * 不明なmagic numberのバイナリをlinuxが実行(sytemcall : execve)しようとすると、前記magic numberと合致するバイナリフォーマットを探索する過程で、call_modprobeが呼ばれる。call_modeprobeは内部で、modeprobe_pathで指定したバイナリを実行する
  * modprobe_pathは、カーネルオプションによってはkallsymsには表示されないが、call_usermodehelper関数の第一引数をデバッガで調べることで求まる
* core_patternを書き換えることで、プログラムのクラッシュによるコアダンプの作成をトリガーとして、任意のスクリプトをrootで実行することが可能

### links
* [Kernel Exploitで使える構造体集](https://ptr-yudai.hatenablog.com/entry/2020/03/16/165628)
* [kernelpwn](https://github.com/smallkirby/kernelpwn)