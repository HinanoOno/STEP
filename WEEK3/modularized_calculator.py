import time

#! /usr/bin/python3
WORD_LIST = ["abs", "round", "int"]


def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == ".":
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {"type": "NUMBER", "number": number}
    return token, index


def read_plus(line, index):
    token = {"type": "PLUS"}
    return token, index + 1


def read_minus(line, index):
    token = {"type": "MINUS"}
    return token, index + 1


def read_multiply(line, index):
    token = {"type": "MULTIPLY"}
    return token, index + 1


def read_divided(line, index):
    token = {"type": "DIVIDED"}
    return token, index + 1


def read_start_bracket(line, index):
    token = {"type": "START_BRACKET"}
    return token, index + 1


def read_end_bracket(line, index):
    token = {"type": "END_BRACKET"}
    return token, index + 1


def read_word(line, index):
    word = ""
    while index < len(line) and line[index].isalpha():
        word += line[index]
        index += 1
    if word in WORD_LIST:
        token = {"type": "WORD", "word": word}
    else:
        raise ValueError("Invalid word found: " + word)
    return token, index


# Tokenize a string.
# ex) "12 + 34" -> [{'type': 'NUMBER', 'number': 12}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 34}]
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == "+":
            (token, index) = read_plus(line, index)
        elif line[index] == "-":
            (token, index) = read_minus(line, index)
        elif line[index] == "*":
            (token, index) = read_multiply(line, index)
        elif line[index] == "/":
            (token, index) = read_divided(line, index)
        elif line[index] == "(":
            (token, index) = read_start_bracket(line, index)
        elif line[index] == ")":
            (token, index) = read_end_bracket(line, index)
        elif line[index].isalpha():
            (token, index) = read_word(line, index)
        elif line[index] == " ":
            index += 1
            continue
        else:
            raise ValueError("Invalid character found: " + line[index])
        tokens.append(token)
    return tokens


# additon and subtraction
def evaluate_plus_and_minus(tokens):
    answer = 0
    tokens.insert(0, {"type": "PLUS"})
    index = 1
    while index < len(tokens):
        if tokens[index]["type"] == "NUMBER":
            if tokens[index - 1]["type"] == "PLUS":
                answer += tokens[index]["number"]
            elif tokens[index - 1]["type"] == "MINUS":
                answer -= tokens[index]["number"]
            else:
                raise ValueError("Invalid syntax")
        index += 1
    return answer


# multiplication and division
def evaluate_multiply_and_divided(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index]["type"] == "NUMBER":
            if tokens[index - 1]["type"] == "MULTIPLY":
                if tokens[index-2]['type'] != "NUMBER":
                    raise ValueError("Invalid syntax")
                tokens[index]["number"] *= tokens[index - 2]["number"]
                del tokens[index - 2 : index]
                index -= 2
            elif tokens[index - 1]["type"] == "DIVIDED":
                if tokens[index-2]['type'] != "NUMBER":
                    raise ValueError("Invalid syntax")
                if tokens[index]["number"] == 0:
                    raise ZeroDivisionError("Division by zero")
                tokens[index]["number"] = (
                    tokens[index - 2]["number"] / tokens[index]["number"]
                )
                del tokens[index - 2 : index]
                index -= 2
        index += 1
    return tokens


# calculate the value in the brackets and replace tokens with the value
def evaluate_brackets(tokens):
    stack = []
    index = 0
    while index < len(tokens):
        if tokens[index]["type"] == "START_BRACKET":
            stack.append(index)
        elif tokens[index]["type"] == "END_BRACKET":
            start = stack.pop()
            answer = evaluate_part(tokens[start + 1 : index])
            tokens[start] = {"type": "NUMBER", "number": answer}
            del tokens[start + 1 : index + 1]
            index = start
        index += 1
    return tokens


# caluculate the value of abs, round, int functions
def calculate_function(function_name,number):
    if function_name == "abs":
        return abs(number)
    elif function_name == "round":
        return round(number)
    elif function_name == "int":
        return int(number)

# evaluate abs, round, int functions
def evaluate_word(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index]["type"] == "WORD":
            tokens[index+1]['number'] = calculate_function(tokens[index]["word"],tokens[index+1]['number'])
            del tokens[index]
        index += 1
    return tokens

# evaluate a part of tokens
def evaluate_part(tokens):
    tokens = evaluate_word(tokens)
    tokens = evaluate_multiply_and_divided(tokens)
    answer = evaluate_plus_and_minus(tokens)
    return answer
    

def evaluate(tokens):
    #tokens.insert(0, {"type": "PLUS"})
    tokens = evaluate_brackets(tokens)
    answer = evaluate_part(tokens)
    return answer


# Todo : Add test for error handling
def test(line):
    try:
        tokens = tokenize(line)
        actualAnswer = evaluate(tokens)
        expectedAnswer = eval(line)
        if abs(actualAnswer - expectedAnswer) < 1e-8:
            print("PASS! (%s = %f)" % (line, expectedAnswer))
        else:
            print(
                "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)
            )
    except ZeroDivisionError as e:
        print("ZeroDivisionError: %s" % e)
    except ValueError as e:
        print("ValueError: %s" % e)
  


def run_test():
    print("==== Test started! ====")
    # only plus and minus
    test("1+2")
    test("1.0+2.1-3")
    # multiply and divide
    test("3+4*2")
    test("6.5-3*4/2+5/2")
    test("4*3/0")
    test("3*0/5+2")
    # brackets
    test(" 3 + 4 * 2 ")
    # big_number
    test("1000324459687978*34285748-2348574/234")
    test("2449589890/5342-2348574/234+423*313214")
    # invalid syntax
    test("3+*2")
    # only one number
    test("3")
    # invalid word
    test("hello")
    # bracekts
    test("3+(12*3)")
    test("(5-2+(3-2)*(3+2))*2")
    test("3+(4*3-((3+2)*2))")
    # word
    test("abs(3)")
    test("int(3.5)+abs(-3)")
    test("round(3.5)+int(3.5*3-2)")
    test("12 + abs(int(round(-1.55) + abs(int(-2.3 + 4))))")

    print("==== Test finished! ====\n")


run_test()

# while True:
#     print('> ', end="")
#     line = input()
#     tokens = tokenize(line)
#     answer = evaluate(tokens)
#     print("answer = %f\n" % answer)


# check the calculation time
start_time = time.time()
try:
    line = "3+*2"
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f" % answer)

except ZeroDivisionError as e:
    print("ZeroDivisionError: %s" % e)
except ValueError as e:
    print("ValueError: %s" % e)

end_time = time.time()
print("Calculation time: %f seconds" % (end_time - start_time))