#      IPP 2 (interpret.py)
#  Ivan Tsiareshkin (xtsiar00)
#  19.04.2022
#

import sys, argparse, re
import xml.etree.ElementTree as ET

# class Frame is used for simple work with frames(GF, LF, TF) and to simplify implementation of necessary instructions
class Frame:
    @staticmethod
    def get_fr(value, flag):
        fr = frame.get(value[:2])
        if fr is None:
            print("55 - frame does not exist (eg read from empty frame stack)", file = sys.stderr)
            sys.exit(55)
        if flag == 0:
            if value[3:] not in fr:
                print("54 - access to non-existent variable (frame exists)", file = sys.stderr)
                sys.exit(54)
        elif flag == 1:
            if value[3:] in fr:
                print("52 - access to non-existent variable (frame exists)", file = sys.stderr)
                sys.exit(52)
        return fr

    @staticmethod
    def get_value(value, type):
        if type == "var":
            fr = Frame.get_fr(value, 0)
            tmp = fr[value[3:]]["value"]
            if tmp is None:
                print("56 - missing value (in variable, on data stack or in the call stack)", file = sys.stderr)
                sys.exit(56)
            return tmp
        elif type == "string" or type == "type":
            if value is None:
                return ""
            else:
                return str(value)
        elif type == "nil":
            return "nil"
        elif type == "int":
            return int(value)
        elif type == "bool":
            if value == "true":
                return True
            elif value == "false":
                return False

    @staticmethod
    def get_type(value, type):
        if type == "var":
            fr = Frame.get_fr(value, 0)
            tmp = fr[value[3:]]["type"]
            if tmp is None:
                print("56 - missing value (in variable, on data stack or in the call stack)", file = sys.stderr)
                sys.exit(56)
            return tmp
        else:
            return type

    @staticmethod
    def set_val(value, set_value, set_type):
        fr = Frame.get_fr(value, 0)
        fr[value[3:]] = { "value" : set_value, "type" : set_type }

# class Stack is used for simple work with stack operations
class Stack:
    def __init__(self):
        self.stack = []

    def s_push(self, data):
        self.stack.append(data)

    def s_pop(self):
        s_lenght = len(self.stack)
        if s_lenght == 0:
            print("56 - missing value (in variable, on data stack or in the call stack)", file = sys.stderr)
            sys.exit(56)
        return self.stack.pop()

# class Instructions contains all necessary instructions
class Instructions:
    # Function MOVE copies the value of symb to var
    def MOVE(value_1, value_2, type_2):
        Frame.set_val(value_1, Frame.get_value(value_2, type_2), Frame.get_type(value_2, type_2))

    # Function CREATEFRAME creates new TF
    def CREATEFRAME():
    	frame["TF"] = {}

    # Function PUSHFRAME moves TF to the frame_stack.  Frame will be available via LF
    def PUSHFRAME():
    	if frame["TF"] is None:
            print("55 - frame does not exist (eg read from empty frame stack)", file = sys.stderr)
            sys.exit(55)

    	frame_stack.s_push(frame["LF"])
    	frame["LF"] = frame["TF"]
    	frame["TF"] = None

    # Function POPFRAME moves the top LF from frame_stack to the TF
    def POPFRAME():
    	if frame["LF"] is None:
    		print("55 - frame does not exist (eg read from empty frame stack)", file = sys.stderr)
    		sys.exit(55)

    	frame["TF"] = frame["LF"]
    	frame["LF"] = frame_stack.s_pop()

    # Function DEFVAR defines a variable in specified frame according to given var
    def DEFVAR(value_1):
        fr = Frame.get_fr(value_1, 1)
        fr[value_1[3:]] = {"value": None, "type": None}

    # Function CALL saves current position to the calls_stack and executes JUMP() to the specified label
    def CALL(value_1):
        global position
        calls_stack.s_push(position)
        Instructions.JUMP(value_1)

    # Function RETURN removes position from the calls_stack and jumps to that position
    def RETURN():
        global position
        tmp = calls_stack.s_pop()
        if tmp is None:
        	print("56 - missing value (in variable, on data stack or in the call stack)", file = sys.stderr)
        	sys.exit(56)
        position = tmp

    # Function PUSHS saves the symb value to the data_stack
    def PUSHS(value_1, type_1):
        data_stack.s_push({"value": Frame.get_value(value_1, type_1), "type": Frame.get_type(value_1, type_1)})

    # Function POPS extracts the value from the data_stack and stores it to var
    def POPS(value_1):
        tmp = data_stack.s_pop()
        if tmp is None:
            print("56 - missing value (in variable, on data stack or in the call stack)", file = sys.stderr)
            sys.exit(56)
        Frame.set_val(value_1, tmp["value"], tmp["type"])

    # Function ADD adds symb1 and symb2 and stores result value to var
    def ADD(value_1, value_2, type_2, value_3, type_3):
        if Frame.get_type(value_2, type_2) != Frame.get_type(value_3, type_3) or Frame.get_type(value_3, type_3) not in ["int"]:
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        Frame.set_val(value_1, Frame.get_value(value_2, type_2) + Frame.get_value(value_3, type_3), Frame.get_type(value_3, type_3))

    # Function SUB subtracts symb2 from symb1 and stores result value to var
    def SUB(value_1, value_2, type_2, value_3, type_3):
        if Frame.get_type(value_2, type_2) != Frame.get_type(value_3, type_3) or Frame.get_type(value_3, type_3) not in ["int"]:
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        Frame.set_val(value_1, Frame.get_value(value_2, type_2) - Frame.get_value(value_3, type_3), Frame.get_type(value_3, type_3))

    # Function MUL multiplies symb1 and symb2 and stores result value to var
    def MUL(value_1, value_2, type_2, value_3, type_3):
        if Frame.get_type(value_2, type_2) != Frame.get_type(value_3, type_3) or Frame.get_type(value_3, type_3) not in ["int"]:
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        Frame.set_val(value_1, Frame.get_value(value_2, type_2) * Frame.get_value(value_3, type_3), Frame.get_type(value_3, type_3))

    # Function IDIV devides int value from symb1 by second int value from symb2 and stores result value to var
    def IDIV(value_1, value_2, type_2, value_3, type_3):
        if Frame.get_value(value_3, type_3) == 0:
            print("57 - wrong operand value (eg division by zero)", file = sys.stderr)
            sys.exit(57)
        if Frame.get_type(value_2, type_2) != Frame.get_type(value_3, type_3) or Frame.get_type(value_3, type_3) != "int":
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        Frame.set_val(value_1, Frame.get_value(value_2, type_2) // Frame.get_value(value_3, type_3), "int")

    # Function LT evaluates the relational operator < between symb1 and symb2 and stores bool value to var
    def LT(value_1, value_2, type_2, value_3, type_3):
        if Frame.get_type(value_2, type_2) != Frame.get_type(value_3, type_3) or Frame.get_type(value_3, type_3) not in ["int", "string", "bool"]:
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        Frame.set_val(value_1, Frame.get_value(value_2, type_2) < Frame.get_value(value_3, type_3), "bool")

    # Function GT evaluates the relational operator > between symb1 and symb2 and stores bool value to var
    def GT(value_1, value_2, type_2, value_3, type_3):
        if Frame.get_type(value_2, type_2) != Frame.get_type(value_3, type_3) or Frame.get_type(value_3, type_3) not in ["int", "string", "bool"]:
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        Frame.set_val(value_1, Frame.get_value(value_2, type_2) > Frame.get_value(value_3, type_3), "bool")

    # Function EQ evaluates the relational operator == between symb1 and symb2 and stores bool value to var
    def EQ(value_1, value_2, type_2, value_3, type_3):
        type2 = Frame.get_type(value_2, type_2)
        type3 = Frame.get_type(value_3, type_3)

        if type2 == "nil" and type3 == "nil":
            Frame.set_val(value_1, 'true', "bool")
        elif type2 == "nil" or type3 == "nil":
            Frame.set_val(value_1, 'false', "bool")
        elif type2 != type3 or type3 not in ["int", "string", "bool"]:
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        else:
            Frame.set_val(value_1, Frame.get_value(value_2, type_2) == Frame.get_value(value_3, type_3), "bool")

    # Function AND applies conjunction to 2 oparands of type bool and stores bool result to var
    def AND(value_1, value_2, type_2, value_3, type_3):
        if Frame.get_type(value_2, type_2) != Frame.get_type(value_3, type_3) or Frame.get_type(value_3, type_3) != "bool":
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        Frame.set_val(value_1, Frame.get_value(value_2, type_2) and Frame.get_value(value_3, type_3), "bool")

    # Function OR applies disjunction to 2 oparands of type bool and stores bool result to var
    def OR(value_1, value_2, type_2, value_3, type_3):
        if Frame.get_type(value_2, type_2) != Frame.get_type(value_3, type_3) or Frame.get_type(value_3, type_3) != "bool":
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        Frame.set_val(value_1, Frame.get_value(value_2, type_2) or Frame.get_value(value_3, type_3), "bool")

    # Function NOT applies negation to 1 operand of type bool and stores bool result to var
    def NOT(value_1, value_2, type_2):
        if Frame.get_type(value_2, type_2) != "bool":
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        Frame.set_val(value_1, not Frame.get_value(value_2, type_2), "bool")

    # Function INT2CHAR converts int value to char string and stores it to var
    def INT2CHAR(value_1, value_2, type_2):
        if Frame.get_type(value_2, type_2) != "int":
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        value = Frame.get_value(value_2, type_2)
        try:
            value = chr(value)
        except:
            print("58 - incorrect string operation", file = sys.stderr)
            sys.exit(58)
        Frame.set_val(value_1, value, "string")

    # Function STRI2INT converts char string to int value
    def STRI2INT(value_1, value_2, type_2, value_3, type_3):
        if Frame.get_type(value_2, type_2) != "string" or Frame.get_type(value_3, type_3) != "int":
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        string = Frame.get_value(value_2, type_2)
        k = Frame.get_value(value_3, type_3)
        if k >= len(string) or k < 0:
            print("58 - incorrect string operation", file = sys.stderr)
            sys.exit(58)
        try:
            string = ord(string[k])
        except:
            print("58 - incorrect string operation", file = sys.stderr)
            sys.exit(58)
        Frame.set_val(value_1, string, "int")

    # Function READ reads one value according to the specified type and stores this value to var
    def READ(value_1, value_2, type_2):
        type = Frame.get_value(value_2, type_2)
        if type not in ["int", "string", "bool"]:
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        input_text = input.readline()
        new_line = '\n' in input_text
        read_in = input_text.rstrip('\n')
        if type == "int":
            try:
                Frame.set_val(value_1, int(input_text), "int")
            except:
                Frame.set_val(value_1, "nil", "nil")
        elif type == "string" and (new_line or (len(read_in) > 0)):
                Frame.set_val(value_1, read_in, "string")
        elif type == "bool":
            if 'true' == read_in.lower():
                Frame.set_val(value_1, True, "bool")
            else:
                if len(read_in) == 0:
                    Frame.set_val(value_1, "nil", "nil")
                else:
                    Frame.set_val(value_1, False, "bool")
        elif len(read_in) == 0:
            Frame.set_val(value_1, "nil", "nil")
        else:
            sys.exit(99)

    # Function WRITE prints the value of symb to stdout
    def WRITE(value_1, type_1):
        string = Frame.get_value(value_1, type_1)
        if Frame.get_type(value_1, type_1) == "nil":
            print("", end='')
        elif Frame.get_type(value_1, type_1) == "bool":
            print(str(string).lower(), end='')
        else:
            print(string, end='')

    # Function CONCAT applies concatenation of 2 string and stores result to var
    def CONCAT(value_1, value_2, type_2, value_3, type_3):
        if Frame.get_type(value_2, type_2) != Frame.get_type(value_3, type_3) or Frame.get_type(value_3, type_3) != "string":
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        Frame.set_val(value_1, Frame.get_value(value_2, type_2) + Frame.get_value(value_3, type_3), "string")

    # Function STRLEN returns length of a string in symb and stores int value of length to var
    def STRLEN(value_1, value_2, type_2):
        if Frame.get_type(value_2, type_2) != "string":
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        length = len(Frame.get_value(value_2, type_2))
        Frame.set_val(value_1, length, "int")

    # Function GETCHAR stores to val a string from one char in the string symb1 in the position symb2
    def GETCHAR(value_1, value_2, type_2, value_3, type_3):
        if Frame.get_type(value_2, type_2) != "string" or Frame.get_type(value_3, type_3) != "int":
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        string = Frame.get_value(value_2, type_2)
        k = Frame.get_value(value_3, type_3)
        if k >= len(string) or k < 0:
            print("58 - incorrect string operation", file = sys.stderr)
            sys.exit(58)
        Frame.set_val(value_1, string[k], "string")

    # Function SETCHAR modifies the character of the string stored in the var at position symb1
    def SETCHAR(value_1, type_1, value_2, type_2, value_3, type_3):
        if Frame.get_type(value_2, type_2) != "int" or Frame.get_type(value_3, type_3) != "string" or Frame.get_type(value_1, type_1) != "string":
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        string = Frame.get_value(value_1, type_1)
        k = Frame.get_value(value_2, type_2)
        if k >= len(string) or k < 0 or len(Frame.get_value(value_3, type_3)) < 1:
            print("58 - incorrect string operation", file = sys.stderr)
            sys.exit(58)
        Frame.set_val(value_1, string[:k] + Frame.get_value(value_3, type_3)[0] + string[k+1:], "string")

    # Function TYPE detects the type of the symbol symb and writes to var
    def TYPE(value_1, value_2, type_2):
        if type_2 == "var":
            fr = Frame.get_fr(value_2, 0)
            tmp = fr[value_2[3:]]["type"]
            if tmp is None:
                tmp_type = ""
            else:
                tmp_type = tmp
        else:
            tmp_type = type_2
        Frame.set_val(value_1, tmp_type, "string")

    def LABEL():
        pass

    # Function JUMP performs an unconditional jump to the specified label
    def JUMP(value_1):
        global position
        tmp = labels.get(value_1)
        if tmp is None:
            print("52 - error during semantic checks (eg use of undefined label, redefinition of variable)", file = sys.stderr)
            sys.exit(52)
        position = tmp

    # Fucntion performs jump to the specified label if types and values of symb1 and symb2 are equal
    def JUMPIFEQ(value_1, value_2, type_2, value_3, type_3):
        global position
        tmp = labels.get(value_1)
        if tmp is None:
            print("52 - error during semantic checks (eg use of undefined label, redefinition of variable)", file = sys.stderr)
            sys.exit(52)

        type2 = Frame.get_type(value_2, type_2)
        type3 = Frame.get_type(value_3, type_3)

        if type2 == "nil" and type3 == "nil":
            position = tmp
        elif type2 == "nil" or type3 == "nil":
            return
        elif type2 != type3 or type3 not in ["int", "string", "bool"]:
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        elif Frame.get_value(value_2, type_2) == Frame.get_value(value_3, type_3):
            position = tmp

    # Fucntion performs jump to the specified label if types of symb1 and symb2 are equal, but values not
    def JUMPIFNEQ(value_1, value_2, type_2, value_3, type_3):
        global position
        tmp = labels.get(value_1)
        if tmp is None:
            print("52 - error during semantic checks (eg use of undefined label, redefinition of variable)", file = sys.stderr)
            sys.exit(52)

        type2 = Frame.get_type(value_2, type_2)
        type3 = Frame.get_type(value_3, type_3)

        if type2 == "nil" and type3 == "nil":
            return
        elif type2 == "nil" or type3 == "nil":
            position = tmp
        elif type2 != type3 or type3 not in ["int", "string", "bool"]:
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        elif Frame.get_value(value_2, type_2) != Frame.get_value(value_3, type_3):
            position = tmp

    # Function EXIT terminates program execution with given return code
    def EXIT(value_1, type_1):
        if Frame.get_type(value_1, type_1) != "int":
            print("53 - wrong operand types", file = sys.stderr)
            sys.exit(53)
        tmp = Frame.get_value(value_1, type_1)
        if tmp < 0 or tmp > 49:
            print("57 - wrong operand value (bad return value of EXIT instruction)", file = sys.stderr)
            sys.exit(57)
        sys.exit(tmp)

    # Function DPRINT prints the specified value symb to standard error output
    def DPRINT(value_1, type_1):
        print(Frame.get_value(value_1, type_1), file = sys.stderr)

    # Function BREAK prints the state of the interpreter
    def BREAK():
        print("Interpret state:", "\nNumber of executed instructions:", position)

# class Interpretator firstly gets values and types from arguments of given instruction and then loads that instruction
class Interpretator:
    def interpret(opcode, line):
        try:
            type_1 = line.find('arg1').get("type")
            value_1 = line.find('arg1').text
            type_2 = line.find('arg2').get("type")
            value_2 = line.find('arg2').text
            type_3 = line.find('arg3').get("type")
            value_3 = line.find('arg3').text
        except:
            pass

        if opcode == "MOVE":
            Instructions.MOVE(value_1, value_2, type_2)
        elif opcode == "CREATEFRAME":
            Instructions.CREATEFRAME()
        elif opcode == "PUSHFRAME":
            Instructions.PUSHFRAME()
        elif opcode == "POPFRAME":
            Instructions.POPFRAME()
        elif opcode == "DEFVAR":
            Instructions.DEFVAR(value_1)
        elif opcode == "CALL":
            Instructions.CALL(value_1)
        elif opcode == "RETURN":
            Instructions.RETURN()
        elif opcode == "PUSHS":
            Instructions.PUSHS(value_1, type_1)
        elif opcode == "POPS":
            Instructions.POPS(value_1)
        elif opcode == "ADD":
            Instructions.ADD(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "SUB":
            Instructions.SUB(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "MUL":
            Instructions.MUL(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "DIV":
            Instructions.DIV(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "IDIV":
            Instructions.IDIV(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "LT":
            Instructions.LT(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "GT":
            Instructions.GT(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "EQ":
            Instructions.EQ(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "AND":
            Instructions.AND(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "OR":
            Instructions.OR(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "NOT":
            Instructions.NOT(value_1, value_2, type_2)
        elif opcode == "INT2CHAR":
            Instructions.INT2CHAR(value_1, value_2, type_2)
        elif opcode == "STRI2INT":
            Instructions.STRI2INT(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "READ":
            Instructions.READ(value_1, value_2, type_2)
        elif opcode == "WRITE":
            Instructions.WRITE(value_1, type_1)
        elif opcode == "CONCAT":
            Instructions.CONCAT(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "STRLEN":
            Instructions.STRLEN(value_1, value_2, type_2)
        elif opcode == "GETCHAR":
            Instructions.GETCHAR(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "SETCHAR":
            Instructions.SETCHAR(value_1, type_1, value_2, type_2, value_3, type_3)
        elif opcode == "TYPE":
            Instructions.TYPE(value_1, value_2, type_2)
        elif opcode == "LABEL":
            Instructions.LABEL()
        elif opcode == "JUMP":
            Instructions.JUMP(value_1)
        elif opcode == "JUMPIFEQ":
            Instructions.JUMPIFEQ(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "JUMPIFNEQ":
            Instructions.JUMPIFNEQ(value_1, value_2, type_2, value_3, type_3)
        elif opcode == "EXIT":
            Instructions.EXIT(value_1, type_1)
        elif opcode == "DPRINT":
            Instructions.DPRINT(value_1, type_1)
        elif opcode == "BREAK":
            Instructions.BREAK()

# Dictionary for storing frame data values
frame = {
	"GF": {},
	"LF": None,
	"TF": None,
}

# Necessary stacks
frame_stack = Stack()
calls_stack = Stack()
data_stack = Stack()

# main function
if __name__ == "__main__":
    # Arguments parsing with argparse
    in_arg = argparse.ArgumentParser(description="IPP 2nd project: interpret of the IPPcode22")
    in_arg.add_argument("--source", help="input file with XML representation of the source code, if don't given, --input is required")
    in_arg.add_argument("--input", help="input file for the interpretation of the specified source code, if don't given --source is required\n")
    args = in_arg.parse_args()

    if args.source != None:
        try:
            source = open(args.source, "r")
        except:
            print("11 - error when opening input files (eg non-existence, insufficient permissions)", file = sys.stderr)
            sys.exit(11)
    else:
        source = sys.stdin

    if args.input != None:
        try:
            input = open(args.input, "r")
        except:
            print("11 - error when opening input files (eg non-existence, insufficient permissions)", file = sys.stderr)
            sys.exit(11)
    else:
        input = sys.stdin

    # Loading XML
    try:
        root = ET.parse(source).getroot()
    except:
        print("31 - wrong XML format in input file (file is not well formatted)", file = sys.stderr)
        sys.exit(31)

    # Sorting by instruction order
    root[:] = sorted(root, key=lambda child: int(child.get("order")))

    # Order array for order validity checks
    order = []
    instructions = []
    labels = {}
    for inst in root:
        try:
            order.append(int(inst.get("order")))
        except:
            print("32 - unexpected XML structure", file = sys.stderr)
            sys.exit(32)

        for arg in inst:
            # Convert all escape sequence to string
            if arg.get("type").lower() == "string":
                reg = re.compile('\\\\(\d{3})')
                def replace(match):
                    return chr(int(match.group(1)))
                def xstr(s):
                    return '' if s is None else str(s)
                arg.text = reg.sub(replace, xstr(arg.text))

        if int(inst.get('order')) < 1 or len(order) != len(set(order)):
            print("32 - unexpected XML structure", file = sys.stderr)
            sys.exit(32)
        instructions.append(inst.get('opcode'))
        # Fill lables dictionary with values
        # If label name already exists in labels dict, returns error 52
        if inst.get('opcode') == "LABEL":
            if inst[0].text in labels:
                print("52 - error during semantic checks (eg use of undefined label, redefinition of variable)", file = sys.stderr)
                sys.exit(52)
            labels[inst[0].text] = list(root).index(inst)

    position = 0
    # Main loop to handle and interpet whole XML
    while position < len(root):
        Interpretator.interpret(instructions[position], root[position])
        position+=1
