cd /D "%~dp0"

SET dir=%cd%\
SET aim="C:\Program Files (x86)\Python37-32\Lib\done\"

if EXIST %aim% (
	echo Directory Already Exists: Clearing and Refreshing Links
	rmdir %aim%
) ELSE (
	echo Creating Directory from Scratch
)

mklink /D %aim% %dir%done

pause