# Forensic - Inspector Edgar's challenges

## Distracted user 
> Inspector Edgar is one of the heads of the London police force. He’s caught many criminals, though he’s never quite understood how he managed to do it. In truth, he’s a bit clumsy and naïve, but not malicious in the slightest.
Right before going on vacation, he jotted down his password on a scrap of paper. Upon returning, he tried to log in but, being a bit absent-minded, he forgot his username. Not the best situation for logging in, is it?
Come on, give him a hand and look at the snapshot!
________________________________________
flag format : HACKDAY{username}
> https://challenges.s3.rbx.io.cloud.ovh.net/challenges/vm-106-disk-0.qcow2
mirrors: https://drive.google.com/file/d/17LdSobRYKmvMDcrGr1SzdE2AoZLUNM8-/view

## A mistake 
> It turns out that before leaving on vacation, he had actually tried to manualy falsify his username... Could he be less innocent than he seems?
Try to uncover his old username (old modification) !
________________________________________
flag format : HACKDAY{username}


## What was I doing 
> Edgar would like you to determine what he was doing just before leaving. According to his memory, he was conducting research, but on what...? Checkout what the user was researching before he left.

The three challenges all use the same file.
.qcow2 is a file format for disk image files used by QEMU, a VM.

While I was doing some research, I stumbled open this writeup : https://ctftime.org/writeup/4974, some parts are similar.

I converted the qcow2 file to a .raw file, which is easier to deal with, using qemu.
`$qemu-img convert vm-106-disk-0.qcow2 disk.raw`

Actually, one flag can already be found with a little grep.
`$grep -a "HACKDAY" vm-106-disk-0.qcow2`
`$grep -a "HACKDAY" disk.raw`

[third flag](../Attachments/Edgar/WhatwasIdoing.png)

`HACKDAY{htTPs://hAckD@y.fR/CHaL13nG3}`
This was the flag for "**What was I doing ?**"

We need to mount the first device. We can use fdisk to check which partition is useful and if there is an offset.

[fdisk](../Attachments/Edgar/fdisk.png)
The offset is 2048*512 bytes = 1048576
`$sudo mount -t ext4 -o ro,offset=1048576 disk.raw mnt/`
`cd /mnt`
We now have the contents of Edgar's VM.
The usernames are stored in etc/passwd, Edgar's username is at the very end.

[username](../Attachments/Edgar/username.png)
This was the flag for **Distracted User**

Edgar has tried to change his username once.
If we check `/etc/group `and `/etc/group-` (backup of the previous copy of the file), there have been changes between the two files. An username change, for example.

`HACKDAY{u$Erh4cKdAYF0rENsiCnIV1}`

/etc/group : 
[group file](../Attachments/Edgar/etcgroup.png)
/etc/group-
[group file backup](../Attachments/Edgar/etcgroupminus.png)

Or diff can also be used to see the username change
[diff](../Attachments/Edgar/comparison.png)
 
`HACKDAY{4nc1eNI0gin}`

This was the flag for **A mistake **