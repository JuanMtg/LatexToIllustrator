# -*- coding: utf-8 -*-
import subprocess
import os
filename = "illustex.tex"
pdfname = "illustex.pdf"

# User LaTeX code
userimput = raw_input("Tex:")
# Creating or modifying the file
target = open(filename, "w")
target.write("\documentclass[12pt, a4paper]{article}" + "\n")
target.write(r"\input{preamble.sty}" + "\n")
target.write(r"\begin{document}" + "\n")
target.write(r'{}'.format(userimput) + "\n")
target.write(r"\end{document}" + "\n")
target.close()
p0 = subprocess.Popen(["pdflatex", filename])
p0.communicate()
# Removing useless files
removelist = ["illustex.aux", "illustex.log", "illustex.synctex.gz"]
for i in removelist:
    try:
        os.unlink(i)
    except WindowsError:
        pass
# Opening pdf in Illustrator
subprocess.Popen(["C:\Program Files\Adobe\Adobe Illustrator CS6 (64 Bit)\Support Files\Contents\Windows\Illustrator.exe",
                      pdfname])
