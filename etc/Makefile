# Destination directory
DEST_DIR = /usr/local/etc

GENERALSCRIPTS = \
		fac-bashrc\


SCRIPTS = $(GENERALSCRIPTS)\

install: $(SCRIPTS)
	install -m 0644 $(SCRIPTS) $(DEST_DIR)


develop: $(SCRIPTS)
	ln -srf $(SCRIPTS) $(DEST_DIR)
