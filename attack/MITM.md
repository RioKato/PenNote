# Man in the middle attack

----

## History
* **2008/11/12** MS08-068により同一ホストでのSMBからSMBへのNTLMリレーが修正される
* **2016/06/15** MS16-075により同一ホストでの他プロトコルからSMBへのNTLMリレーが修正される
* **2018/10/05** MS-RPRNRPCを介してあるホストに他ホストへのSYSTEM権限でのNTLM認証を強制することが可能なPrinter Bugが発見されるものの、仕様であるという理由で**Microsoftに修正されない**
* **2019/03/28** Windows 10 1809、Windows Server 2019へのアップデートにより、DCOMがローカルリスナーと通信しないよう、仕様の変更が行われ、DCOMを利用した同一ホストでのNTLMリレーが動作しなくなる 
* **2019/02/12** Exchangeサーバに他ホストへのDCSyncの権限を含む特権でのNTLM認証を強制することが可能なCVE-2018-8581（PrivExchange）が修正される
* **2019/06/11** SMBからLDAPへのNTLMリレーを禁止するNTLMパケット中のフラグをクリア可能な、CVE-2019-1040（DropTheMIC）が修正される

## Protocols
| from \ to (another host) | SMB    | LDAP | HTTP   | RPC    |
| ------------------------ | ------ | ---- | ------ | ------ |
| **SMB**                  | OK     | NG   | 未確認 | OK     |
| **LDAP**                 | 未確認 | OK   | 未確認 | 未確認 |
| **HTTP**                 | 未確認 | OK   | OK     | OK     |
| **RPC**                  | NG     | NG   | 未確認 | OK     |

* SMBからLDAPへのNTLMリレーはCVE-2019-1040が存在すればntlmrelayxのdrop-micオプションで可能
* ldapへのリレーを行う際はntlmrelayxのescalate-userオプションが
* [Relaying NTLM authentication over RPC](https://blog.compass-security.com/2020/05/relaying-ntlm-authentication-over-rpc/)

## Exploit

| Exploit                                                    | Affected Version                              | Description                                              |
| ---------------------------------------------------------- | --------------------------------------------- | -------------------------------------------------------- |
| [Juicy Potato](https://github.com/ohpe/juicy-potato)       | < Windows 10 1809, < Windows Server 2019      | SeImpersonatePrivilegeもしくはSeAssignPrimaryTokenが必要 |
| [Rogue Potato](https://github.com/antonioCoco/RoguePotato) | >= Windows 10 1809, >= Windows Server 2019    | SeImpersonatePrivilegeもしくはSeAssignPrimaryTokenが必要 |
| [PrintSpoofer](https://github.com/itm4n/PrintSpoofer)      | >= Windows 10, >= Windows Server 2016/2019    | SeImpersonatePrivilegeが必要。Printer Bugを利用          |
| [printer bug](https://github.com/dirkjanm/krbrelayx)       | 不明                                          |                                                          |
| [privexchange](https://github.com/dirkjanm/krbrelayx)      | Microsoft Exchange Server 2010/2013/2016/2019 |                                                          |


## Reference
* [NTLM Relay is dead, Long live NTLM Relay](https://conference.hitb.org/hitbsecconf2018dxb/materials/D2T2%20-%20NTLM%20Relay%20Is%20Dead%20Long%20Live%20NTLM%20Relay%20-%20Jianing%20Wang%20and%20Junyu%20Zhou.pdf)
* [Potatoes - Windows Privilege Escalation](https://jlajara.gitlab.io/others/2020/11/22/Potatoes_Windows_Privesc.html)
* [NTLM Relay](https://en.hackndo.com/ntlm-relay/)
* [Abusing Exchange: One API call away from Domain Admin](https://dirkjanm.io/abusing-exchange-one-api-call-away-from-domain-admin/)