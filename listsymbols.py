#!/bin/env python
import re

class TableWrite:
    """Write tables with correct header and footer"""
    
    def __init__(self,file):
        self.f = file
        self.columncount = 0
        self.tableopen= False
        self.tablebegin = r'\begin{tabular*}{\linewidth}{@{\extracolsep{\fill}}l@{\extracolsep{0.5cm}}l@{\extracolsep{\fill}}l@{\extracolsep{0.5cm}}l@{\extracolsep{\fill}}l@{\extracolsep{0.5cm}}l}'+'\n'
        self.tableend=r'\end{tabular*}'+'\n'

    def item(self,text):
        if not self.tableopen:
            self.f.write(self.tablebegin)
            self.tableopen=True
            self.columncount = 0
        self.f.write(text)
        if self.columncount<2:
            self.f.write(' & ')
            self.columncount+=1
        else:
            self.f.write(r' \\'+'\n')
            self.columncount=0

    def finish(self):
        if self.tableopen:
            if self.columncount>0:
                self.f.write(r' \\'+'\n')
            self.f.write(self.tableend+'\n')
            self.tableopen=False

    def header(self,text):
        self.finish()
        self.f.write(text+'\n')

fin = open('lhcb-symbols-def.tex')
outname = 'lhcb-symbols-list.tex'
fout = open(outname,'w')
print("All symbols are now available in the file {0}".format(outname))

fout.write("""% This is an automatically generated appendix to template.tex. 
% When included it will show all the symbols defined in lhcb-symbols-def.tex.
%
% To regenerate with the latest definitions run the script python listsymbols.py

\\section{List of all symbols}
\\label{sec:listofsymbols}
""")

psection = re.compile(r'(%+)\s*(.*)')
pdef = re.compile(r'^\\def(\\.+?)[\s{]+[^%]*(%\s.+)*')
pnew = re.compile(r'^\\newcommand\{(\\\w+?)\}(\[\d\])*[\s\{]+[^%]*(%\s.+)*')
parg = re.compile(r'.+(#\d)+.*')

writer=TableWrite(fout)

for l in fin.readlines():

    # Match on section headers
    m = psection.match(l)
    if m:
        length = len(m.group(1))
        if length<=2:
            if length==1:
                writer.header('\\subsection{%s}' % m.group(2))
            else:
                writer.header('\\subsubsection{%s}' % m.group(2))

    # Match on the \def lines
    m = pdef.match(l)
    if m:
        marg = parg.match(m.group(1))
        if not marg:
            writer.item('\\texttt{\\textbackslash %s} & %s' 
                        % (m.group(1)[1:],m.group(1)))
        else:
            if m.group(2):
                pat1 = re.compile(r'#')
                pat2 = re.compile(r'(#\d)+')
                generic = re.sub(pat1,r'\#',m.group(1))
                example = re.sub(pat2,m.group(2)[2:],m.group(1))
                writer.item('\\texttt{\\textbackslash %s ' % generic[1:] +
                            '\\textbackslash %s} & %s' 
                            % (example[1:],example))
            else:
                print('Ignoring line: {0}'.format(l[:-1]))

    # Match on the \newcommand lines
    m = pnew.match(l)
    if m:
        if not m.group(2):
            writer.item('\\texttt{\\textbackslash %s} & %s' 
                        % (m.group(1)[1:],m.group(1)))
        elif m.group(3):
            generic = str(m.group(3)[2:]).replace('{',r'\{').replace('}',r'\}')
            writer.item('\\texttt{\\textbackslash %s%s ' % 
                       (m.group(1)[1:],m.group(2)) +
                        '\\textbackslash %s%s} & %s%s' 
                        % (m.group(1)[1:],generic,
                           m.group(1),m.group(3)[2:]))
        else:
            print('Ignoring line: {0}'.format(l[:-1]))
            
writer.finish()

fin.close()
fout.close()
