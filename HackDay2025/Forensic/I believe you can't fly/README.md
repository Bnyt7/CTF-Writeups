# Forensic

## I believe you can't fly 
> In the world of Featherstone Airways, where airships dominate the skies and steam-powered engines hum in harmony with the winds, disaster strikes aboard Flight 404. A cacophony of alarms blares through the cabin, and an automated voice pierces the tension:
"Alert: Navigation systems compromised. Manual override unavailable."
The captain, drenched in sweat, confesses that the ship’s intricate steam-core systems have been infiltrated by rogue machinists. The autopilot is spewing erratic commands, and the controls have been rendered useless. Amid the chaos, your gaze falls upon a forgotten device—a mechanical tablet left behind by the ship’s chief engineer. Its dimly glowing screen is your only hope to uncover the secrets of this sabotage and reclaim control of the vessel.
The tablet appears to hold critical files containing traces of the hackers’ interference. To restore the autopilot and prevent the airship from plunging into the abyss, you must uncover the password hidden within these files. As the last passenger with a keen mind for cyber-steam security, it falls to you to analyze these files, piece together the password, and save the airship before it’s too late. Time is of the essence, and the lives of everyone aboard rest in your hands. Will you rise to the challenge and prove yourself the hero of the skies?

A system has been infiltrated by hackers, and one device (a log) is used to understand what the attackers have done.
There is a password (flag) in the recovered files. This flag is in several parts.

The zip file contains two images `say_hi.jpg, whoami.jpg` and one log `plane_logs.txt` which describes the system's status. Some data are more interesting than the others.

    [2025-01-22 14:00:07] MALICIOUS: Encoded word detected: ercbafr
    [2025-01-22 14:09:36] MALICIOUS: Encoded word detected: c29sdXRpb24=
    [2025-01-22 14:03:49] WARNING: Encoded word detected: 636c6566
    [2025-01-22 14:05:56] WARNING: Encoded word detected: 0110001011111011011000110110100001100101
    [2025-01-22 14:01:18] DEBUG: Encoded word detected: KDFNGD\~dPbCbiU6H
And two hints

        [2025-01-22 14:08:50] INFO: Sometimes the answer is just three steps ahead.
        [2025-01-22 14:03:25] INFO: The most secure password is often the simplest one.

The four first words decoded are not helpful.
1. Caesar cipher : "reponse" (answer in french)
2. Base64 : "solution" (answer in french)
3. Hex : "clef" (key in french)
4. Binary : "bûche" (log for a tree in french)

The fifth word is actually encoded in **Rot-3 with 94 printable ASCII characters from ! (33) to ~ (126**), it fits with the "three steps" in one of the hints.
I used [dcode](https://www.dcode.fr/rot-cipher "dcode") to find the word. 

First part of the flag : `HACKDAY{aM_@_fR3E`

For the next part, we have to analyze the images. The second hint is a nod to the fact that some files have hidden data with a password. Steghide, stegseek or any similar tool can be used to extract content from the images.
In our case, only say_hi has hidden data.

[stegseek](../Attachments/CantFly/stegseek.png)

And the second part of the flag is inside the output.
[flag part 2](../Attachments/CantFly/flag2.png)

`HACKDAY{aM_@_fR3E-@LbaRT0s5}`
