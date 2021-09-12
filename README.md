# MainPythons
**installation** - just `pip install .` from same location as setup.py couldn't be easier  
if you want to keep the py files in a specific location preform `pip install -e .` instead  

## __init__.py
just imports everything into the namespace  
**TEST** - run the hidden done.test module

## Number.py
**nth_remainder** - the nth remainder in the process of long division  
**decimal_length** - gives the location and length of the repeating portion of the decimal expansion  
**get_repeat** - application of the previous two functions to get the repeating portion of the decimal expansion  
**parse_number** - convert to int or float (prefers ints)  
**simplifyRadical** - simplifies radicals  
**pythagoreanTriplets** - gets pythagorean triplet integer (comes with helper function pyTrip)  
**isPrime** - returns True if n is prime  
**nextPrime** - returns prime >= to number given  
**primeFactorize** - prime factorizes a number  
**theFactorsOf** - human readable version of (factorsOf) lists the factors of a integer  
**distinctPrimeFactorsOf** - list of prime factors  
**totient** - Evaluates Euler's totient function as best I know  
**BaseChanger** - used to convert integers to a list representation of a base  
**RangedNumber** - imagine if ordered pairs could be operated on mathematically  
**PrimalNatural** - intended for Numbers between 1 and infinity. optimized for multiplication and divisor checking  
**convergentSqrt** - yield numerator and denominator of closer approximations to the sqrt  
**radToFrac** - converts the sqrt into a continued fraction  
**convergentsE** - yield numerator and denominator of closer approximations to the number e  
**PI** - given a decimal precision will return pi to that precision  
**NumToStr** - gives name of number  
## List.py
**is_iterable** - determines if object is iterable  
**window** - gives sliding window iterator  
**batch** - gives a batch (const size chunks) iterator  
**poisson** - finds poisson probability (mean rate & successes)  
**Dev** - finds sample or population Deviation  
**freqDev** - same as Dev but freq increases size  
**probDev** - same as freq Dev  
**hypergeometric** - stats stuff  
**online_average** - computes average one at a time  
**median** - center of list when ordered  
**gcd** - finds greatest common factor of many numbers  
**lcm** - finds least common multiple of many numbers  
**cross** - combines many lists (compressing nd to 1d)  
**applyToGenerator** - creates a decorator for generators  
**CollisionDict** - class that is essentially dict\<mutable-collection\>  
## Time.py
**Time Class** - performs math based on the time since midnight  
**days_between** - tells you how many days between two dates  
**DayOfTheWeek** - will give you Monday,Tuesday, ... etc, according to month, day, year given  
**MoonPhase** - will tell you how much percent starting from new moon  
**timer** - context manager that will time how much the block runs  
**maxtime_computation** - using an infinate generator and a online calculation method will return around maxtime seconds  
**function_time** - timeit.timeit wrapper. calculates iterations/second  
**QuickThread** - starts a thread with the function you pass on.  
## Solver.py
**solve** - using 4 basic operations {*-+/} makes numbers into lookup  
**sudoku** - solves sudoku problems for you  
**numRemainders** - finds number with divisor:remainder pairs  
**linear_combination** - finds how many of each in list to make num  
**addOrSub** - adds +/- between #s to make num  
## Math.py
**angle** - together with distance gives polar coord  
**angleForStar** - gets number of spokes and gives angle needed  
**Polynom** - object representing algebraic functions in string form  
**Nomial** - object representing algebraic functions in list form  
**BitString** - class that is a long. word = len(4bits)  
**fact** - factorial (n!)  
**perm** - permutation (nPr)  
**comb** - combination (nCr)  
## File.py
**getHome** - returns the environment $HOME or $USERPROFILE   
Desktop - path to Desktop = join(getHome(), 'Desktop')  
**same** - compares 2 file paths and returns if they lead to same descriptor  
**files** - walks through place; yields relative path to files  
**folders** - walks through place; yields relative path to folders  
**listFormats** - walks through place; outputs extensions found  
**hideInMaze** - hides file in a directory maze  
**linkDirectory** - Copies directories, symlinks replace files  
**smartBackup** - Update files in backup  
**rename_file** - using change function renames f in files  
**site_look** - Give url and will try to save and open html file  
**site_read** - Give it a http and you get a byte  string.  
**read** - reads file and returns string  
**write** - writes to a file return boolean saying is successful  
**repeatUntilValid** - decorator that repeatedly executes wrapped function until the parameterized function returns True  
**reImport** - reimport a module for if you modify the module and don't want to close and reopen  
**ZipGui** - creates a GUI to explore a Zipfile  
**unzip** - Unzips files 1 at a time. (used for when you need to unzip a corrupted zip file)  
## Game.py
**matrix** - will randomly print numbers between nums  
**multiplication** - will repeatedly ask you to multiply numbers  
**pattern** - will make a pattern to figure out  
**physics** - Will ask motion physics question to answer.  
**thinker** - Will ask you which number has the divisor:remainder pairs  
**number_guesser** - fun games to play where the computer guesses ur numbers . 3 versions numbered 1,2, and 3  
**zombie** - Choose your own adventure time. (I'm very proud of this. Especially since it was first programmed in my calculator.)  
**ultimate_rps** - Ultimate Rock Paper Scissors  
**murder** - Murder happens; figure out who did what  
## String.py
**multiple_replace** -  replaces multiple times using [(from, to),..]  
**createTranslationTable** -  basically just a helper for codes  
**print_iterable** - for i in iterable: print(i)  
**switch** - swap the strings in the main string. almost like a simultaneous double replace statement.  
**reverse** - reverse a string's characters  
**wrapPrint** - Text Wrapper  
**removePrint** - deletes center of text  
**score** - compares the two strings giving a score between 0 and 1  
**tree** - created to parse Applescript's 'entire content' dictionaries  
**Markov** - sliding window over string to get triplets of words to markov chain with  
**SequenceAlignment** - aligns strings so that the most letters fall into the same place  
## StringGenerators
**pretty** - displays stars to the Terminal  
**get_next** or **random_char** - returns a char using the ChainData matrix and the previous letter in string  
**random_word** - makes a random string of given length using ChainData matrix  
**chain** - makes random pronounceable 'words' using ChainData matrix  
**loremIpsum** - uses chain() to make sentences  
## StringSolver
**chemistry** - will try to recreate sentence using only the symbols of the periodic table  
**anagram** - un-shuffles word to match a word in dictionary file  
**clues22** - plays that clues 22 game. given substrings that combine to make words will try to combine the substrings  
**oneLetterFromEach** - an anagram solver with specific letters. given a list of strings will take a letter from each string  
**connectWords** - a Word Ladder solver. given two words it finds how they're connected by changing 1 letter at a time. each step also being a word  
**DeBruijn** - gives a DeBruijn Sequence given an alphabet and the substring length  
## Codes.py
**binary** - changes letters to 8bitBinary  
**eggnog** - it sorta reverses the string in a special way  
**crosc** - subsitition: (a:y, b:z, c:x, d:w, e:u, ...)  
**craziness** - substitution: also called option code  
**morse** & **anti_morse** - morse code and its inverse using '.', '-', and ' ' (dot, dash, space)  
**num_letters** - abc becomes 1.2.3 etc (inverse is also allowed)  
**cypher** - moves letters in a circle depending on num.  
**updown** - uses the unicode characters for 'rotated-vertically' characters and preforms reverse  
**lisp** - make the string read like it has a lisp by swapping certain letters with 'TH'  
