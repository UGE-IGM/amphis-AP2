$ENV{'TEXINPUTS'}='../../../latex//:';
$pdf_mode = 1;
$pdflatex = "lualatex -interaction=nonstopmode -synctex=1 -shell-escape %O %S";
