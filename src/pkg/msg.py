from pkg.msglib.greet import greet
from pkg.msglib.question import ask_question

def message():
    msg = greet() + ask_question()
    return msg
