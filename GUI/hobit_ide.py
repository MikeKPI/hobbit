#!/usr/bin/env python3

from tkinter import *

from opg.grammar import grammar, grammar_elements
from tokenizer.tokenizer import Tokenizer
from hobbit_lib.opg.analyzer import OPGAnalyzer


class HobbitGUI(Tk):
    def __init__(self, parent=None):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        self.title("Hobbit IDE")
        self.tz = None

    def initialize(self):
        self.grid()

        spaceTTIF = Label(self)
        spaceTTIF.grid(column=5)
        self.inputField = Text(self)
        self.inputField.grid(column=0, row=0,
                             columnspan=10, rowspan=14, sticky='EW')

        self.tokensTable = Listbox(self, width=10, height=15, font='Courier')
        self.tokensTable.grid(column=6, row=0,
                              columnspan=10, rowspan=10, sticky='EW')
        self.variableTable = Listbox(self, width=10, height=10, font='Courier')
        self.variableTable.grid(column=6, row=10,
                                columnspan=10, rowspan=7, sticky='EW')
        self.constantTable = Listbox(self, width=10, height=10, font='Courier')
        self.constantTable.grid(column=6, row=17,
                                columnspan=10, rowspan=7, sticky='EW')

        self.errorsTable = Listbox(self, width=100, height=10, font='Courier')
        self.errorsTable.grid(column=0, row=18, columnspan=4, sticky="EW")
        self.errorsTable1 = Listbox(self, width=100, height=10, font='Courier')
        self.errorsTable1.grid(column=0, row=27, columnspan=4, sticky="EW")
        self.inputField.focus_set()

        btnParse = Button(self, text="Parse",
                          command=self.on_button_parse)
        btnParse.grid(column=3, row=17)

        btnAnalyze = Button(self, text='Analyze',
                            command=self.analyze)
        btnAnalyze.grid(column=2, row=17)

    def test(self):
        source_code = self.inputField.get('1.0', 'end').split('\n')
        for i in source_code:
            print(i)

    def analyze(self):
        self.errorsTable1.delete(0, END)
        if self.tz is None:
            self.errorsTable.insert(END, "No data to analyze.")
        try:
            a = OPGAnalyzer(self.tz['tokens'][:-2], grammar=grammar, grammar_elements=grammar_elements)
            for i in a.analyze():
                self.errorsTable1.insert(END, i)
            self.errorsTable.insert(END, 'OK')
        except Exception as e:
            self.errorsTable.insert(END, 'At line {!s} you have an error in symbol {}'.format(e.args[0].line_number + 1,
                                                                                              e.args[0].name))

    def on_button_parse(self):
        self.tz = None
        self.tokensTable.delete(0, END)
        self.variableTable.delete(0, END)
        self.constantTable.delete(0, END)
        self.errorsTable.delete(0, END)
        source_code = self.inputField.get('1.0', 'end').split('\n')

        for i in range(len(source_code)):
            source_code[i] += '\n'

        # analyzing of input file
        self.tz = Tokenizer(source_to_analyze=source_code)
        try:
            self.tz = self.tz.analyze()
            self.errorsTable.insert(END, "OK")
        except Exception as e:
            self.errorsTable.insert(END, e)

        for token in self.tz['tokens'][:-2]:
            self.tokensTable.insert(END, token)

        for i in self.tz['variables']:
            self.variableTable.insert(END, i)

        for i in self.tz['constants']:
            self.constantTable.insert(END, i)


if __name__ == '__main__':
    app = HobbitGUI()
    app.mainloop()
