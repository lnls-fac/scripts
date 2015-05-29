# Destination directory
DEST_DIR = /usr/local/bin

FMASCRIPTS= $(shell ls fma-* 2> /dev/null)

SCRIPTS = $(FMASCRIPTS) 

install: $(SCRIPTS)
	install $(SCRIPTS) $(DEST_DIR)

develop: $(SCRIPTS)
	ln -srf $(SCRIPTS) $(DEST_DIR)


