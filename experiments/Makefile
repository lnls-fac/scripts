# Destination directory
DEST_DIR = /usr/local/bin

SIRIUSSCRIPTS= $(shell ls sirius-* 2> /dev/null)

SCRIPTS = $(SIRIUSSCRIPTS)

FULLSCRIPTS = $(addprefix $(DEST_DIR)/, $(SCRIPTS))

install: uninstall $(SCRIPTS)
	cp $(SCRIPTS) $(DEST_DIR)

uninstall:
	-rm -rf $(FULLSCRIPTS)

develop: uninstall $(SCRIPTS)
	ln -srf $(SCRIPTS) $(DEST_DIR)
