# Destination directory
DEST_DIR = /usr/local/etc

GENERALSCRIPTS = \
		fac-bashrc\

SCRIPTS = $(GENERALSCRIPTS)\

install: $(SCRIPTS)
	cp -f $(SCRIPTS) $(DEST_DIR)

uninstall:
	cd $(DEST_DIR); rm -rf $(SCRIPTS); cd -

develop: $(SCRIPTS) uninstall
	ln -srf $(SCRIPTS) $(DEST_DIR)
