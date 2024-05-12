You are given a file called win10.elf

from the description of the challenge you can deduce that the file is a memory dump of a computer.

To analyze memory dumps a popular tool called volatility 2 can be used. using this tool a list of running programs can be made and a program called UHCTF.exe is shown running on the computer.
using vol2 you can extract the exe or create a memory dump of the process running uhctf.exe 
Doing strings on the uhctf.exe file two base64 encoded strings appear. one of these strings is the flag
