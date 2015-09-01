# Destination directory
DEST_DIR = /usr/local/bin

GENERALSCRIPTS = \
		compilacao_epics.sh\
		delete_dups.py\
		elegant2OPA.py\
        elegant2AT.py\
		hosts_update.py\
		pytrack.py\
		run_in_clients.sh\
		savestate_vbox.sh\
		start_vbox.sh\
		update_ip_on_workstation.sh

FACSCRIPTS = $(shell ls fac-*)

SIRIUSSCRIPTS= $(shell ls sirius-*)

WIKISCRIPTS = $(shell ls wiki-*)

SCRIPTS = $(GENERALSCRIPTS)\
		  $(FACSCRIPTS)\
		  $(SIRIUSSCRIPTS)\
		  $(WIKISCRIPTS)

FULLSCRIPTS = $(addprefix $(DEST_DIR)/, $(SCRIPTS))

install: uninstall $(SCRIPTS)
	cp $(SCRIPTS) $(DEST_DIR); cd $(DEST_DIR); chmod a+x $(SCRIPTS)

uninstall:
	-rm -rf $(FULLSCRIPTS)

develop: uninstall $(SCRIPTS)
	ln -srf $(SCRIPTS) $(DEST_DIR)

fac: $(FACSCRIPTS)
	install $(FACSCRIPTS) $(DEST_DIR)

sirius: $(SIRIUSSCRIPTS)
	install $(SIRIUSSCRIPTS) $(DEST_DIR)

wiki: $(WIKISCRIPTS)
	install $(WIKISCRIPTS) $(DEST_DIR)
