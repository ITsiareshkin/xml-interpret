## Implementation documentation for the 2nd task in IPP 2021/2022
### Name and surname: Ivan Tsaireshkin
### Login: xtsiar00
<br />
<br />

### Task description (XML code representation interpret)

The main task is to make python3.8 program interpret.py, that loads the XML representation of the program and this program interprets and generates output using input according to command line parameters.
<br />

### Usage

```
interpret.py [-help] 

or 

interpret.py [--source SOURCE] [--input INPUT]
```
<br /> 

### Return codes and errors
* 0 - success
* 11 - error when opening input files (eg non-existence, insufficient permissions
* 31 - wrong XML format in input file (file is not well formatted
* 32 - unexpected XML structure
* 52 - error during semantic checks (eg use of undefined label, redefinition of variable
* 53 - wrong operand types
* 54 - access to non-existent variable (frame exists)
* 55 - frame does not exist (eg read from empty frame stack)
* 56 - missing value (in variable, on data stack or in the call stack)
* 57 - wrong operand value (eg division by zero)
* 58 - incorrect string operation
<br />

### Solution description
* Main function: <br />
Program firstly parses the command line arguments (using argparse module). With the --help flag, brief information about program and usage method will be written out. <br />
After parsing the command line arguments program loads source XML using xml.etree.ElementTree module and loads root node into variable root. Interpret  then sorts nods by the attribute "order". <br />
Loop, that goes through all instructions in source XML, fills order list with order values to make it easier to check if the order is correct. Also, for each instruction, all it's string arguments are processed and all escape sequences are converted to a string (chars). Important part of this loop is detecting and working with labels, whose values and names are stored in specific dictionary. <br />
After this loop, another, main one begins. It calls interpret() function and essentially starts the interpretation. <br />
* Auxiliary class: Interpretator <br />
This class contains interpret() function, which takes values and types from the arguments of the given instruction and loads it. <br />
* Auxiliary class: Instructions <br />
This class contains all necessary instructions. <br />
Those instructions are implemented using Frame and Stack classes.
* Auxiliary class: Frame <br />
This class contains 4 important functions: get_fr, get_type, get_value, set_val. <br />
get_fr returns requested frame, which contains types and values of variables. <br />
get_value returns value of variable in specifed frame using the data stored in the "frame" dictionary. <br />
get_type returns type of variable in specifed frame using the data stored in the "frame" dictionary. <br /> 
set_val sets given value and type to specifed frame. <br />
* Auxiliary class: Stack <br />
This class is used for simple stack operations such as push and pop
<br />
<br />

### Task description (Testing framework)

The main task is to make php8.1 script test.php, which will be used for automatic testing of parse.php and interpret.py.
<br />

### Usage

```
test.php [options] 
```
Where options are:<br /> 
--help              : Print help<br /> 
--directory=path    : Test path. The default is './'<br /> 
--recursive         : Test search will be recursive<br /> 
--parse-script=file : Path to the IPPcode22 parser file. The default is './parse.php'<br /> 
--int-script=file   : Path to the IPPcode22 interpret. The default is './interpret.py'<br /> 
--parse-only        : Run tests on the parser only. It can't be combined with the --int-script and --int-only options.<br /> 
--int-only          : Run tests on the interpret only. It can't be combined with the --parse-script, --parse-only options and --jexampath.<br /> 
  (If both parse-only and int-only parameters are not set, parser and interpreter tests will be run sequentially)<br /> 
--jexampath=path    : Path to the directory containing the jexamxml.jar file and a configuration file named options. The default is '/pub/courses/ipp/jexamxml/'<br /> 
--noclean           : Auxiliary files with interim results will not be deleted during test.php work<br /> 
<br />

### Return codes and errors
* 0 - success
* 10 - missing script parameter (if needed) or use of disabled parameter combination
* 41 - the specified directory or the specified file does not exist or is not accessible
<br />

### Solution description
* Main function <br />
Firstly script sets default values, parses the command line arguments using getopt() function. <br />
It then generates header of HTML summary, including title, heading and header of table, which represents information about each test. <br />
In main loop, script finds .src files and creates necessary files.<br />
The test is based on the specified parameters, whether it is checking only parser/interpret, or both at once<br />
Script works with 2 comparisons, firstly checks return codes (reference is .rc file).<br />
Depends on return codes and program status,script outputs all the necessary information line by line to the HTML table. <br />
When options int-only and parse-only are not set, script firstly checks parser. If return code is 0, interpret will be executed, otherwise script will not execute interpret.<br />
* Auxiliary functions: create_(in/out/rc) <br />
These functions create the necessary files if they are missing.
* Auxiliary functions: f_clean, f_open, f_write <br />
Functions for convenient work with files.
* Auxiliary functions: print_head, print_body, print_summary, print_end <br />
Functions, that generate an HTML summary of processed tests.








