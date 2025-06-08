Project Summary:
This is a profanity checker built into a simulated 1:1 chat application. The idea behind a 1:1 chat format is to mimic real-life communication—one person sending messages to another—while applying profanity filtering logic in real-time.

A profanity checker in this context refers to a system that detects offensive words in user input and obscures a key character using censorship logic. Unlike traditional methods that replace entire words, this tool replaces only one character per detected offensive word, making it both subtle and effective.

The solution combines a React frontend that mimics a real chat UI, a Python backend powered by OpenAI to identify bad words, and a Brainfuck script that replaces a single character with an asterisk.


To run this application:

in one terminal window run:
python entryPoint.py

in another terminal window run:
npm start

Please note: in entryPoint.py... this uses an openAI API Key which was gitignored...
Please use your own openAI api key

Logic: 

The entryPoint file is a python wrapper that takes input from the user
and the profane word goes through the brainfuck file to replace the profane
letter with an asterisk

The brainfuck-chat client contains the necessary files such as App.js and App.css
to mimic the real life chat experience

sample.bf is the brainfuck file and this is the logic behind it:
given a string that looks like 'U|fUck'... the goal will be to return f*ck.
So, the file loads U into memory block c0 and loads | into c1. Following that,
the program starts a loop on the | and inputs the first char after the delimiter.
Next, the program needs to copy the contents of c0 and c1 into c3 and c4 respectively
in order to perform a subtraction and see if both blocks reach 0 at the same time, thus checking
for equality. Likewise, c5 is populated with an asterisk and in the event that both c3 and c4 have equal
contents, the asterisk will be outputed, else the actual char will be outputed. The memory blocks at c3, c4, and c5
clear out, and the loop continues with the next character. 

brainfuck.py and getch.py were used and imported from a preexisting repo to run the bf file as a built in interpreter.

To see example of please view the following image:
example-chat.png


