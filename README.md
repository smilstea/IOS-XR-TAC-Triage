<b>Installation Notes</b>
<br>
The IOS XR Tac Triage set of scripts are an offbox utility written in python 3.x to automate triage and log collection for specific use cases. With minimal inputs from the user specific helpful information can be gleaned for consumption by the user or uploaded to TAC for further triage.
<br><br>
No installation is required or compiling of the scripts, only requirement is python 3 with following libraries:
- pexpect
- os
- sys
- getpass
- re

<br>
<br>
<b>Running the Script</b>
<br>
To call the script make sure their permissions are set to executable then call them like so (telnet is default):

	python3 [--file <filename>] [--ipv4addr <address>] [--username <username>] (--ssh) (--timeout <timeout>)
  
	python3 [--memcompare] [--pre <filename>] [--post <filename>] (--kb)
  
	python3 [--config] [--file <filename>]
<br>
<br>
<b>Special Keywords</b>

	--timeout Specifies the timeout from commands, by default this is 5s for a few reasons.
  
	Because some commands may not output immediately
  
	Some commands pause mid-way through output
  
	General delay in getting data output This allows for the collection of outputs properly as they are generated and a pause in case a command does not output immediately, pauses, or python catches up to the end of the available data Using this keyword and changing the timeout is NOT recommended.

<br/>
<br/>

	--memcompare Specifies to run a comparison for memory leak detection after the memory leak commands have been run twice.
	--kb specifies to use a KB difference in heap memory instead of the default MB difference.
<br>
<br>
<b>Output</b>
  
Some output will be displayed on the screen, but this is kept to a minimum, only displaying differences or a summary for each command. Outfiles will have the full outputs.

<br> 
<br> 
<b>Bugs / Enhancements / etc</b>
  
Contact smilstea@cisco.com for any issues, please include terminal logs and the output files for faster debugging.
  
Don't see a feature or command you want in this tool, contact smilstea@cisco.com preferably with examples.

 <br/>
Scale Configurator Syntax:
This script is designed to generate scale configurations.
		
		1. For numbers
		Ranges such as [10-50] will automatically increment by 1.
		For a different multiplier use a ',' such as [10-50,5].
		
		2. For hex
		Ranges such as {0-a} or {0-A} will automatically increment by 1.
		For a different multiplier use a ',' such as {0-A,5}.
		Case insensitive
		
		3. For letters
		Ranges such as (a-g) or (A-G) will automatically increment by 1.
		For a different multiplier use a ',' such as (a-g,5).
		Case sensitive
		
		Returns:
		- Scale config to terminal window.

		###Example###
		Example Times to Run: 3

		Example File:
		interface GigabitEthernet0/0/0/13.[1-200] l2transport
		 vrf vrf(a-e,3)
		 encapsulation dot1Q [1-200] second-dot1q [30-35,3] exact
		 ipv6 address 2001::{0-f,7}/26
		 no shut
		!

		Example Output:
		interface GigabitEthernet0/0/0/13.1 l2transport
		 vrf vrfa
		 encapsulation dot1Q 1 second-dot1q 30 exact
		 ipv6 address 2001::0/26
		 no shut
		!
		interface GigabitEthernet0/0/0/13.2 l2transport
		 vrf vrfd
		 encapsulation dot1Q 2 second-dot1q 33 exact
		 ipv6 address 2001::7/26
		 no shut
		!
		interface GigabitEthernet0/0/0/13.3 l2transport
		 vrf vrfb
		 encapsulation dot1Q 3 second-dot1q 30 exact
		 ipv6 address 2001::E/26
		 no shut
		!
