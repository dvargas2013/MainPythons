# MainPythons
##__init__.py
just import everything from everywhere
##Number.py
**simplifyRadical** - simplifies radicals  
**pythagoreanTriplets** - gets pythagorean triplet integer (comes with helper function pyTrip)  
**isPrime** - returns True if n is prime  
**nextPrime** - returns prime >= to number given  
**primeFactorize** - prime factorizes a number  
**theFactorsOf** - human readable list of factors of a integer  
**changeBase** - convert to new base (comes with helper functions fromBaseTen and toBaseTen)  
**convergentSqrt** - yield numerator and denominator of closer approximations to the sqrt
**radToFrac** - converts the sqrt into a continued fraction (the period will always be the last n-1 terms and the last term is always 2x the first) 
**convergentsE** - yield numerator and denominator of closer approximations to the number e (comes with helper function convergents which can be used to emulate convergentsSqrt if used in conjunction with radToFrac)
**numToStr** - gives name of number  
**piecewiseMaker** - makes a piecewise function  
##List.py
**poisson** - finds poisson probability (mean rate & successes)  
**Dev** - finds sample or population Deviation  
**freqDev** - same as Dev but freq increases size  
**probDev** - same as freq Dev  
**hypergeometric** - stats stuff  
**median** - center of list when ordered  
**gcd** - finds gratest common factor of many numbers  
**lcm** - finds least common multiple of many numbers  
**show** - prints a line for every element of the list given - (move to done.File?)  
**cross** - combines 2 list (compressing 2d to 1d)  
**combine** - combines many lists (compression nd to 1d)  
**dct** - frequencies yay  
**idct** - amplitudal yay  
##Time.py
**Time Class** - internally has basically the time since midnight and will perform calculations based on that number.  
**bisectHrMnHands** - will bisect the hour and minute hands with the second hand (there are two solutions no matter where hr and mn are set so the sc parameter can't just always be set to 0)  
**DayOfTheWeek** - will give you Monday,Tuesday, ... etc, according to month, day, year given  
**timer** - context manager that will time how much the block runs  
*Usage:*  
```with timer("Message"):
   <block>```
##Solver.py
**solve** - using 4 basic operations {*-+/} makes numbers into lookup
**sudoku** - solves sudoku problems for you
**numRemainders** - finds number with divisor:remainder pairs
**respart** - finds how many of each in list to make num
**addOrSub** - adds +/- between #s to make num
##Math.py
**angle** - together with distance gives polar coord  
**angleForStar** - gets number of spokes and gives angle needed  
**polynom** - object representing algebraic functions in string form  
**nomial** - object representing algebraic functions in list form  
**BitString** - class that is a long. word = len(4bits). init to 0.  
**fact** - factorial (n!)  
**perm** - permutation (nPr)  
**comb** - combination (nCr)  
##File.py
**getHome** - returns the environment $HOME  
Desktop - path to Desktop = join(getHome(), 'Desktop')  

**files** - walks through place; yields relative path to files  
**folders** - walks through place; yields relative path to folders  
**listFormats** - walks through place; outputs extensions found  
**hideInMaze** - hides file in a directory maze  
**linkDirectory** - Copies directories, symlinks replace files  
**smartBackup** - Update files in backup  
**renamer** - using change function renames f in files  
**delPyCache** - deletes all pycache directories and pyc files.   
**getSizes** - make dictionary with file dimensions  
**resize** - scales down images with a dimension bigger than 1200   
**siteLook** - Give url and will try to save and open html file  
**siteRead** - Give it a http and you get a byte  string.  
**read** - reads file and returns string  
**write** - writes to a file return boolean saying is successful  
**reImport** - reimport a module for if you modify the module and dont want to close and reopen  
**dARename** - renames files in a special way  
**ZipGui** - creates a GUI to explore a Zipfile
**unzip** - Unzips files 1 at a time. (used for when you need to unzip a corrupted zip file)  
##Game.py
**matrix** - will randomly print numbers between nums  
**multgame** - will repeatedly ask you to multiply numbers  
**pattgame** - will make a pattern to figure out  
**physics** - Will ask motion physics question to answer.  
**thinker** - Will ask you which number has the divisor:remainder pairs  
**mindread** - Will guess a number between 1-25 if you tell it location  
**zombie** - Choose your own adventure time. (I'm very proud of this. Especially since it was first programmed in my calculator.)  
**ultrps** - Ultimate Rock Paper Scissors  
**murdergame** - Murder happens; figure out who did what  
##String.py
**Input** - Accept multiple lines of input until the end string is on it's own line  
**lisp** - make the string read like it has a lisp by swapping certain letters with 'TH'  
**switch** - swap the strings in the main string. almost like a simultaneous double replace statement.  
**findListInStr** - finds first item in list that occurs in string  
**reverse** - reverse a string's characters  
**charShift** - changes the character given by applying the character shift if its an alpha char  
**font** - changes all the alpha characters to full-width  
**backwards** - uses unicode characters for 'rotated-horizontally' characters and preforms reverse  
**updown** - uses the unicode characters for 'rotated-vertically' characters and preforms reverse  
**strShuffle** - shuffles the whole string  
**dyslexia** - shuffles the center portions of the words  
**wrapPrint** - Text Wrapper  
**removePrint** - deletes center of text  
**score** - compares the two strings giving a score between 0 and 1  
**findOccurance** - find the nth occurance of a substring  
**isRep** - figures out if a string is composed of the substring given  
**endRepFind** - finds repetitions at end of string  
**showInfo** - gives a bit of info on the thing  
**chain** - makes random pronounceable 'words'
**loremIpsum** - uses chain() to make sentences  
**chemistry** - will try to recreate sentence using only the symbols of the periodic table  
**anagram** - un-shuffles word to match a word in dictionary file  
**clues22** - plays that clues 22 game. given substrings that combine to make words will try to combine the substrings  
**tree** - created to parse Applescript's 'entire content' dictionaries  
**Markov Class** - sliding window over string to get triplets of words to markov chain with  
**pretty** - displays stars to the Terminal  
**SequenceAlignment** - aligns strings so that the most letters fall into the same place  
**DeBruijn** - gives a DeBruijn Sequence given an alphabet and the substring length  
##Codes.py
**binary** - changes letters to 8bitBinary  
**eggnog** - it sorta reverses the string in a special way  
**crosc** - subsitition: (a:y, b:z, c:x, d:w, e:u, ...)  
**crazyness** - subsition: also called option code  
**piglatin** - piglatin and its inverse  
**morse** & **antimorse** - morse code and its inverse using '.', '-', and ' ' (dot, dash, space)  
**numword** - (a:1, b:2, c:3,...) and its inverse  
**bobulate** & **unbobulate** - adds A&Bs and repeats letters. Informally uncoded by looking at every 3rd letter. Has other logic  
**cypher** - moves letters in a circle depending on num.  