# PC5AtmosphericExtinction
Repository for SRM Key Project PC5 (Atmospheric Extinction)



Small tutorial on git to start
================================
(sylvielsstfr, October 28th 2016)


Here is a list of commands I can issue on my computer:

- 1) get the remote directory on your laptop:
-------------------------------------------------
git clone https://github.com/DarkEnergyScienceCollaboration/PC5AtmosphericExtinction.git

- 2) add all the modified files and the new created file
--------------------------------------------------------
git add [filenames]

or

git add *

- 3) Validate the modification locally on your computer by issuing:
--------------------------------------------------------------------
git commit -m"This is a comment line"

-4) Check what you have done:
-------------------------------
git status

5) Defines where is the remote repository
-----------------------------------------

git remote set-url origin git@github.com:/DarkEnergyScienceCollaboration/PC5AtmosphericExtinction.git 

6) Import modifications of other users
------------------------------------

git pull


7) Send your modifications to the remote repository
----------------------------------------------------
git push origin master


To be able to push it may be necessary to provide an SSH Key to GitHub.

The documentation is there:

https://help.github.com/articles/generating-an-ssh-key/
I can push from my mac
Try to push from my lab linux server !
