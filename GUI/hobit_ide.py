#!/usr/bin/env python3

from tkinter import *

from opg.grammar import grammar, grammar_elements
from rpn.translator import Translator
from tokenizer.tokenizer import Tokenizer
from hobbit_lib.opg.analyzer import OPGAnalyzer


class HobbitGUI(Tk):
    class Text2(Frame):
        def __init__(self, master, width=0, height=0, **kwargs):
            self.width = width
            self.height = height

            Frame.__init__(self, master, width=self.width, height=self.height)
            self.text_widget = Text(self, **kwargs)
            self.text_widget.pack(expand=YES, fill=BOTH)

        def pack(self, *args, **kwargs):
            Frame.pack(self, *args, **kwargs)
            self.pack_propagate(False)

        def grid(self, *args, **kwargs):
            Frame.grid(self, *args, **kwargs)
            self.grid_propagate(False)

    def __init__(self, parent=None):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        self.title("Hobbit IDE")
        self.tz = None
        self.log = []

    def initialize(self):
        self.grid()

        spaceTTIF = Label(self)
        spaceTTIF.grid(column=15)
        self.inputField = Text(self)
        self.inputField.grid(column=0, row=0,
                             columnspan=1, rowspan=8, sticky='EW')

        self.inputParamField = Text(self, width=20, height=10)
        self.inputParamField.grid(column=1, row=5,
                                  columnspan=2, rowspan=4, sticky='EW')

        self.tokensTable = Listbox(self, width=10, height=15, font='Courier')
        self.tokensTable.grid(column=3, row=0,
                              columnspan=10, rowspan=4, sticky='EW')
        self.variableTable = Listbox(self, width=10, height=5, font='Courier')
        self.variableTable.grid(column=3, row=5,
                                columnspan=10, rowspan=1, sticky='EW')
        self.constantTable = Listbox(self, width=10, height=5, font='Courier')
        self.constantTable.grid(column=3, row=7,
                                columnspan=10, rowspan=1, sticky='EW')

        self.errorsTable = Listbox(self, width=100, height=10, font='Courier')
        self.errorsTable.grid(column=0, row=9, columnspan=4, sticky="EW")
        self.errorsTable1 = Listbox(self, width=100, height=10, font='Courier')
        self.errorsTable1.grid(column=0, row=10, columnspan=4, sticky="EW")
        self.errorsTable2 = Listbox(self, width=100, height=10, font='Courier')
        self.errorsTable2.grid(column=0, row=11, columnspan=4, sticky="EW")
        self.inputField.focus_set()

        btnParse = Button(self, text="Parse",
                          command=self.on_button_parse)
        btnParse.grid(column=2, row=0)

        btnAnalyze = Button(self, text='Analyze',
                            command=self.analyze)
        btnAnalyze.grid(column=2, row=1)
        btnRun = Button(self, text='POLIZ',
                        command=self.on_button_translate)
        btnRun.grid(column=2, row=2)
        btnRun = Button(self, text='RUN',
                        command=self.run)
        btnRun.grid(column=2, row=3)

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
            self.log = [i for i in a.analyze()]
            for i in self.log:
                print(i)
                self.errorsTable1.insert(END, '| {iteration:3} | {stack:30.30} | {relation:1.1} | {input:20.20} | '
                                              '{rpn:30.30} |'
                                         .format(iteration=i['iteration'],
                                                 stack=str(i['stack']),
                                                 relation=i['relation'],
                                                 input=str(i['input']),
                                                 rpn=str(i['rpn'])))
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

    def on_button_translate(self):
        self.source = Translator().translate(self.tz['tokens'])
        self.errorsTable2.insert(END, self.source)

    def run(self):
        from hobbit_lib.rpn.executor import execute

        print(self.source)
        execute(self.source)


if __name__ == '__main__':
    app = HobbitGUI()
    app.mainloop()
