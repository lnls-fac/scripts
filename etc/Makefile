# Destination directory
DEST_DIR = /usr/local/etc

GENERALSCRIPTS = \
		bashrc-sirius \
                bashrc-facuser

SCRIPTS = $(GENERALSCRIPTS)

FULLSCRIPTS = $(addprefix $(DEST_DIR)/, $(SCRIPTS))

install: uninstall $(SCRIPTS)
	cp $(SCRIPTS) $(DEST_DIR)
	ln -sf $(DEST_DIR)/bashrc-facuser /home/fac/.bashrc; chown fac.fac /home/fac/.bashrc

uninstall:
	-rm -rf $(FULLSCRIPTS)

develop: uninstall $(SCRIPTS)
	ln -srf $(SCRIPTS) $(DEST_DIR)
	ln -sf $(DEST_DIR)/bashrc-facuser /home/fac/.bashrc; chown fac.fac /home/fac/.bashrc

hosts:
	ln -sf ./hosts-lnls350 /etc/hosts
