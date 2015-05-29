# Destination directory
DEST_DIR = /usr/local/etc

GENERALSCRIPTS = \
		fac-bashrc\


SCRIPTS = $(GENERALSCRIPTS)\

install: $(SCRIPTS)
	install -m 0644 $(SCRIPTS) $(DEST_DIR)

uninstall:
	cd $(DEST_DIR); rm -rf $(SCRIPTS); cd -

develop: $(SCRIPTS) uninstall
	ln -srf $(SCRIPTS) $(DEST_DIR)
