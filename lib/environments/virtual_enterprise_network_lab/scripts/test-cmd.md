SMB:                                                                   
                                                                         
  smbclient -L //192.168.10.5 -N                                         
  smbclient //192.168.10.5/public -N -c "ls"                             
  smbclient //192.168.10.5/finance -U asmith%Password123! -c "ls"
  smbclient //192.168.10.5/it -U bjones%Password123! -c "ls"             
                                                                         
  LDAP:                                                                  
                                                                         
  ldapsearch -x -H ldap://192.168.10.5 -b "dc=lab,dc=local" dn           
  ldapsearch -x -H ldap://192.168.10.5 -b "ou=Users,dc=lab,dc=local"     
 