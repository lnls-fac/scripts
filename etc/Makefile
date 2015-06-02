# Destination directory
DEST_DIR = /usr/local/etc

GENERALSCRIPTS = \
		fac-bashrc

SCRIPTS = $(GENERALSCRIPTS)

FULLSCRIPTS = $(addprefix $(DEST_DIR)/, $(SCRIPTS))

install: uninstall $(SCRIPTS)
	cp $(SCRIPTS) $(DEST_DIR)

uninstall:
	-rm -rf $(FULLSCRIPTS)

develop: uninstall $(SCRIPTS)
	ln -srf $(SCRIPTS) $(DEST_DIR)
