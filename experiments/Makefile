# Destination directory
DEST_DIR = /usr/local/bin

SIRIUSSCRIPTS= $(shell ls sirius-* 2> /dev/null)


SCRIPTS = $(SIRIUSSCRIPTS) 

install: $(SCRIPTS)
	install $(SCRIPTS) $(DEST_DIR)

develop: $(SCRIPTS)
	ln -srf $(SCRIPTS) $(DEST_DIR)

sirius: $(SIRIUSSCRIPTS)
	install $(SIRIUSSCRIPTS) $(DEST_DIR)

