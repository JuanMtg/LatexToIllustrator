# -*- coding: utf-8 -*-
import wx
import os
import subprocess


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        # Creating a timer to change labels of buttons
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.oncompile, self.timer)

        # TextCtrl sizer to enter LaTeX input
        self.latexbox = wx.TextCtrl(self, -1, value=r"$ $", size=(-1, -1))
        mainsizer.Add(self.latexbox, -1, wx.EXPAND)

        # Buttons to perform different actions
        sizerbut = wx.BoxSizer(wx.HORIZONTAL)
        mainsizer.Add(sizerbut, -1, wx.TOP | wx.CENTER)

        self.compilebutton = wx.Button(self, label='Compilar a LaTeX')
        sizerbut.Add(self.compilebutton, -1, wx.TOP | wx.CENTER)

        self.illustbutton = wx.Button(self, label='Mandar a Illustrator')
        sizerbut.Add(self.illustbutton, -1, wx.TOP | wx.CENTER)

        # TextCtrl holding last info entered
        sizerlabel = wx.BoxSizer(wx.HORIZONTAL)
        lastelabel = wx.StaticText(self, -1, u'Última compilación:')
        sizerlabel.Add(lastelabel, -1, wx.ALL | wx.CENTER)
        mainsizer.Add(sizerlabel, -1, wx.TOP | wx.CENTER)

        histr = open('history.txt', 'r')
        line = histr.readline().rstrip('\n')
        self.lastentered = wx.TextCtrl(self, -1, value=line, size=(-1, -1))
        histr.close()
        self.lastentered.SetEditable(False)
        self.lastentered.SetBackgroundColour((200, 200, 200))
        mainsizer.Add(self.lastentered, -1, wx.EXPAND)

        # Button bindings
        self.Bind(wx.EVT_BUTTON, self.oncompile, self.compilebutton)
        self.Bind(wx.EVT_BUTTON, self.onillust, self.illustbutton)

        self.SetSizer(mainsizer)
        self.SetAutoLayout(1)
        mainsizer.Fit(self)
        self.Show(True)

    def oncompile(self, event):
        """Compiles user input via pdflatex"""
        filename = "illustex.tex"
        hist = open('history.txt', 'w')
        hist.write(self.latexbox.GetValue())
        hist.close()

        if self.timer.IsRunning():
            self.timer.Stop()
            self.compilebutton.SetLabel("Compilar a LaTeX")
        else:
            self.timer.Start(1000)
            self.compilebutton.SetLabel("Compilando")
            # Modifying tex file
            targ = open(filename, "w")
            targ.write("\documentclass[12pt, a4paper]{article}" + "\n")
            targ.write(r"\input{preamble.sty}" + "\n")
            targ.write(r"\begin{document}" + "\n")
            targ.write(r'{}'.format(self.latexbox.GetValue()) + "\n")
            targ.write(r"\end{document}" + "\n")
            targ.close()
            # Compiling with pdflatex
            p0 = subprocess.Popen(["pdflatex", filename])
            p0.communicate()
            # Removing extra files
            removelist = ["illustex.aux", "illustex.log", "illustex.synctex.gz"]
            for i in removelist:
                try:
                    os.unlink(i)
                except WindowsError:
                    pass
        histr = open('history.txt', 'r')
        line = histr.readline().rstrip('\n')
        self.lastentered.SetValue(line)
        histr.close()

    def onillust(self, event):
        """Opens pdf file on Illustrator"""
        pdfname = 'illustex.pdf'
        subprocess.Popen([r"C:/Program Files/Adobe/Adobe Illustrator CS6 (64 Bit)/Support Files/Contents/Windows/Illustrator.exe",
                          pdfname])
if __name__ == '__main__':
    app = wx.App(False)
    frame = MainWindow(None, "LaTeX to Illustrator")
    app.MainLoop()