# MainPythons

**installation:**

- `pip install .` from same location as setup.py
- `pip install .[test]` if you want to run `pytest`
- `pip install -e .` if you're planning on editing the files

## List.py

**is_iterable** - determines if object is iterable  
**window** - gives sliding window iterator  
**batch** - gives a batch (const size chunks) iterator  
**diagonals** - used to get the list of diagonals (list of tuples) of 2D array  
**interleave** - gives a way to merge iterators, roundrobin style  
**product** - similar to the builtin sum but takes product instead   
**gcd** - finds the greatest common factor of many numbers  
**lcm** - finds the least common multiple of many numbers  
**cross** - combines many lists (compressing nd to 1d)  
**applyToGenerator** - creates a decorator for generators  
**Polynomial** - object representing algebraic functions  
**BitString** - class that is a long. word = len(4bits)  
**CollisionDict** - class that is essentially dict\<mutable-collection\>

## Stats.py

**poisson** - finds poisson probability (mean rate & successes)  
**Dev** - finds sample or population Deviation  
**freqDev** - same as Dev but freq increases size  
**probDev** - same as freq Dev  
**hypergeometric** - stats stuff  
**online_average** - computes average one at a time  
**median** - center of list when ordered

## Solver.py

**solve** - using 4 basic operations {*-+/} makes numbers into lookup  
**sudoku** - solves sudoku problems for you  
**numRemainders** - finds number with divisor:remainder pairs  
**linear_combination** - finds how many of each in list to make num  
**addOrSub** - adds +/- between #s to make num

## Time.py

**Time Class** - performs math based on the time since midnight  
**days_between** - tells you how many days between two dates  
**DayOfTheWeek** - will give you Monday,Tuesday, ... etc., according to month, day, year given  
**MoonPhase** - will tell you how much percent starting from new moon  
**timer** - context manager that will time how much the block runs  
**maxtime_computation** - using an infinite generator and an online calculation method will return around maxtime
seconds  
**function_time** - timeit.timeit wrapper. calculates iterations/second  
**QuickThread** - starts a thread with the function you pass on.

## File.py

**getHome** - returns the environment $HOME or $USERPROFILE   
**Desktop** - path to Desktop = join(getHome(), 'Desktop')  
**same** - compares 2 file paths and returns if they lead to same descriptor  
**cwd_as** - set the current working directory to specified location while within the context manager block  
**files** - walks through place; yields relative path to files  
**folders** - walks through place; yields relative path to folders  
**rename_files** - using change function renames f in files  
**read** - reads file and returns string  
**write** - writes to a file return boolean saying is successful  
**repeatUntilValid** - decorator that repeatedly executes wrapped function until the parameterized function returns True  

### File.directory

**listFormats** - walks through place; outputs extensions found  
**hideInMaze** - hides file in a directory maze  
**linkDirectory** - Copies directories, symlinks replace files  
**smartBackup** - Update files in backup  

### File.module

**reImport** - reimport a module for if you modify the module and don't want to close and reopen  
**add_to_all** - manually add to __all__ via decorator  
**submodules** - find names of the submodules. easy to __all__.extend  
**filter_off_modules_and_dunder** - find names in global that aren't __ nor modules  

### File.pretty

**TGF** - file format for graph networks  
**stringify** - prettyprint wannabe  

### File.site

**look** - Give url and will try to save and open html file  
**read** - Give it a http, and you get a byte string.  

### File.zip
**ZipGui** - creates a GUI to explore a Zipfile  
**unzip** - Unzips files 1 at a time. (used for when you need to unzip a corrupted zip file)  

## Game.py

**matrix** - will randomly print numbers between nums  
**multiplication** - will repeatedly ask you to multiply numbers  
**pattern** - will make a pattern to figure out  
**physics** - Will ask motion physics question to answer.  
**thinker** - Will ask you which number has the divisor:remainder pairs  
**number_guesser** (1, 2, and 3) - fun games to play where the computer guesses ur numbers . 3 versions numbered 1,2,
and 3  
**zombie** - Choose your own adventure time. (I'm very proud of this. Especially since it was first programmed in my
calculator.)  
**ultimate_rps** - Ultimate Rock Paper Scissors  
**murder** - Murder happens; figure out who did what

## Number.py

**angle** - together with distance gives polar coord  
**parse_number** - convert to int or float (prefers ints)  
**pythagoreanTriplets** - gets pythagorean triplet integer (comes with helper function pyTrip)  
**RangedNumber** - imagine if ordered pairs could be operated on mathematically

### Number.display

**simplifyRadical** - simplifies radicals  
**theFactorsOf** - human-readable version of `Number.primes.factorsOf` lists the factors of an integer  
**primeFactorize** - human-readable version of `Number.primes.primify` prime factorizes a number  
**BaseChanger** - used to convert integers to a list representation of a base  
**NumToStr** - gives name of number

### Number.division

**nth_remainder** - the nth remainder in the process of long division  
**decimal_length** - gives the location and length of the repeating portion of the decimal expansion  
**get_repeat** - application of the previous two functions to get the repeating portion of the decimal expansion
**rounds_to** - finds the fraction that outputs the given string/float   

### Number.primes

**isPrime** - returns True if n is prime  
**nextPrime** - returns prime >= to number given  
**distinctPrimeFactorsOf** - list of prime factors  
**totient** - Evaluates Euler's totient function as best I know  
**PrimalNatural** - intended for Numbers between 1 and infinity. optimized for multiplication and divisor checking

### Number.accuracy

**radToFrac** - converts the sqrt into a continued fraction  
**convergentSqrt** - yield numerator and denominator of closer approximations to the sqrt  
**convergentsE** - yield numerator and denominator of closer approximations to the number e  
**PI** - given a decimal precision will return pi to that precision
**SigFig** - does the math and rounding as defined by sigfig in school  

## String.py

**multiple_replace** - replaces multiple times using [(from, to),..]  
**createTranslationTable** - basically just a helper for codes  
**switch** - swap the strings in the main string. almost like a simultaneous double replace statement.  
**reverse** - reverse a string's characters  
**score** - compares the two strings giving a score between 0 and 1  
**upper_and_lower** - upper and lower cases chars in string according to the bool iterable given
**Markov** - sliding window over string to get triplets of words to markov chain with  
**SequenceAlignment** - aligns strings so that the most letters fall into the same place

### String.Generators

**MarkovStars** - use .generate() to make random nonsense  
**random_char** - returns a char using the ChainData matrix and the previous letter in string  
**random_word** - makes a random string of given length using ChainData matrix  
**chain** - makes random pronounceable 'words' using ChainData matrix  
**loremIpsum** - uses chain() to make sentences  
**DeBruijn** - gives a DeBruijn Sequence given an alphabet and the substring length

### String.printing

**pretty** - displays stars to the Terminal  
**print_iterable** - for i in iterable: print(i)  
**wrapPrint**/**smartPrint** - Text Wrapper  
**safePrint**/**removePrint** - deletes center of text  
**tree** - created to parse Applescript's 'entire content' dictionaries

### String.Solver

**chemistry** - will try to recreate sentence using only the symbols of the periodic table  
**anagram** - un-shuffles word to match a word  
**clues22** - plays that clues 22 game. given substrings combine to make words  
**oneLetterFromEach** - an anagram-like solver. given a list of strings will take a letter from each string  
**connectWords** - a Word Ladder solver. given two words it finds how they're connected by changing 1 letter at a time.
each step also being a word

### String.Codes

**binary** & **unbinary**- changes letters to 8bitBinary  
**eggnog** - it sorta reverses the string in a special way  
**crosc** - subsitition: (a:y, b:z, c:x, d:w, e:u, ...)  
**craziness** - substitution: also called option code  
**morse** & **anti_morse** - morse code and its inverse using '.', '-', and ' ' (dot, dash, space)  
**num_letters**/**numword** - abc becomes 1.2.3 etc. (inverse is also allowed)  
**cypher** - moves letters in a circle depending on num.  
**updown** & **downup** - uses the unicode characters for 'rotated-vertically' characters and preforms reverse  
**lisp** - make the string read like it has a lisp by swapping certain letters with 'TH'  
