# Programming

## Lonely bot

> You wander through the deserted streets of the abandoned docks south
> of Dagenham, convinced they might serve as a hideout for criminals.
> After exploring ruined buildings and broken machinery, your attention
> is caught by a strange light shining from beneath a rusty door.
> Forcing it open, you are surprised to find a small robot that seems
> eager to communicate with you. Try to uncover the secrets it holds,
> though you’re beginning to realize this might take some time...
> 
> ----------
> 
> More instances of the challenge:
> 
> -   challenges.hackday.fr:41521
> -   challenges.hackday.fr:41522
> -   challenges.hackday.fr:41523
> -   challenges.hackday.fr:41524
> -   challenges.hackday.fr:41525
> 
> ----------
> 
> There's an currently issue with the trailing newlines handling in the
> buffer from the server side. The challenge can still be solved. You
> have to send your answers without any trailing newlines added in the
> buffer. We are looking for a hotfix.
> 
> ----------
> 
> The use of **socket** and **send()** method can help to solve the
> challenge.
> For the traduction, the server use the **deep-translator** python
> package with **Google Traduction** method.
> For the current date question, the server get it through a lib method
> that abstract the 0 in front of the day/month. For example, if the
> current date si the 17/07/2016, the server ask for 17/7/2016. The
> asked format have been updated in the bot



Ugly code but it worked.

Install deep translator : `pip install deep-translator`

Change the rockyou.txt location to yours if it's different.

Change the date to today's date.


Part 1 : `HACKDAY{Y3E4H_1ZY_R1GHT!}`

Part 2 : `HACKDAY{So0ooOOo0_KNOW|LED,GE4BLE}`

Part 3 : `HACKDAY{D4MN;YOU&HAD(A_L0T_oF_T1M3_T0_SP3ND}`
