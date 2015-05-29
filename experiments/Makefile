# Destination directory
DEST_DIR = /usr/local/bin

SIRIUSSCRIPTS= $(shell ls sirius-* 2> /dev/null)


SCRIPTS = $(SIRIUSSCRIPTS)

install: $(SCRIPTS)
	install $(SCRIPTS) $(DEST_DIR)

uninstall:
	cd $(DEST_DIR); rm -rf $(SCRIPTS); cd -

develop: $(SCRIPTS) uninstall
	ln -srf $(SCRIPTS) $(DEST_DIR)

sirius: $(SIRIUSSCRIPTS)
	install $(SIRIUSSCRIPTS) $(DEST_DIR)
