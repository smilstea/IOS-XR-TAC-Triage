The IOS XR Tac Triage set of scripts are an offbox utility written in python 3.x to automate triage and log collection for specific use cases. With minimal inputs from the user specific helpful information can be gleaned for consumption by the user or uploaded to TAC for further triage.



No installation is required or compiling of the scripts, only requirement is python 3 with following libraries:

pexpect

os

sys

getpass

re



Running the Script

To call the script make sure their permissions are set to executable then call them like so (telnet is default):

python3 [--file <filename>][--ipv4addr <ipv4 address>][--username <username>](--ssh)(--timeout <seconds>)"
  
python3 [--memcompare][--pre <filename>][--post <filename>]
  

Special Keywords
  

--timeout Specifies the timeout from commands, by default this is 10s for a few reasons.
  
Because some commands may not output immediately
  
Some commands pause mid-way through output
  
General delay in getting data output This allows for the collection of outputs properly as they are generated and a pause in case a command does not output immediately, pauses, or python catches up to the end of the available data Using this keyword and changing the timeout is NOT recommended. The downside is that after a command stops outputing data there will be a 10s delay before executing the next command, with 30 or 40 commands that means 300 or 400 extra seconds.

  
--memcompare Specifies to run a comparison for memory leak detection after the memory leak commands have been run twice.


Output
  
Some output will be displayed on the screen, but this is kept to a minimum, only displaying differences or a summary for each command. Outfiles will have the full outputs.

  
  
Bugs / Enhancements / etc
  
Contact smilstea@cisco.com for any issues, please include terminal logs and the output files for faster debugging.
  
Don't see a feature or command you want in this tool, contact smilstea@cisco.com preferably with examples.
