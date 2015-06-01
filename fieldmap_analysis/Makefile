# Destination directory
DEST_DIR = /usr/local/bin

FMASCRIPTS= $(shell ls fma-* 2> /dev/null)

SCRIPTS = $(FMASCRIPTS)

install: $(SCRIPTS)
	install $(SCRIPTS) $(DEST_DIR)

uninstall:
	cd $(DEST_DIR); rm -rf $(SCRIPTS); cd -

develop: $(SCRIPTS) uninstall
	ln -srf $(SCRIPTS) $(DEST_DIR)
