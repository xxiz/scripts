REM Reset IP
netsh int ip reset

REM Reset IP to DHCP
netsh interface ip set address "Local Area Connection" dhcp

REM Reset DNS to DHCP
netsh interface ip set dns "Local Area Connection" dhcp

REM Reset WinSock
netsh winsock reset

REM Clean ARP Cache
netsh interface ip delete arpcache

REM Clean DNC Cache
ipconfig /flushdns
