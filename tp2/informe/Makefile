BINDIR=bin
TRASH=informe.aux informe.log informe.out informe.toc informe.idx \
informe.fdb_latexmk informe.bbl informe.blg texput.log informe.dvi
LATEX=pdflatex
# El latex se compila dos veces seguidas, la primera es para que se arme bien el índice.
LATEX_PARAMS=-interaction=batchmode -file-line-error --shell-escape

.PHONY: all clean

all: $(BINDIR)/informe.pdf

$(BINDIR)/informe.pdf: informe.tex
		( $(LATEX) $(LATEX_PARAMS) informe.tex && clear &&\
		$(LATEX) $(LATEX_PARAMS) informe.tex ) || (echo 'ERROR.'&&rm informe.pdf)
		@mv informe.pdf $(BINDIR)
		@(evince $(BINDIR)/informe.pdf)||(xdg-open $(BINDIR)/informe.pdf)||\
		(xpdf $(BINDIR)/informe.pdf)||(echo "ERROR: Abrir el pdf manualmente")
	
clean:
		rm -f $(BINDIR)/informe.pdf
		rm -f $(TRASH)
