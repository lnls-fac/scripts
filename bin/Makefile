# Destination directory
DEST_DIR = /usr/local/bin

GENERALSCRIPTS = \
		compilacao_epics.sh\
		delete_dups.py\
		elegant2OPA\
		hosts_update.py\
		pytrack.py\
		run_in_clients.sh\
		savestate_vbox.sh\
		start_vbox.sh\
		update_ip_on_workstation.sh\

FACSCRIPTS = $(shell ls fac-*)

SIRIUSSCRIPTS= $(shell ls sirius-*)

WIKISCRIPTS = \
		updatewiki\
		wiki_backup\
		wiki_clean_backup\

SCRIPTS = $(GENERALSCRIPTS)\
		  $(FACSCRIPTS)\
		  $(SIRIUSSCRIPTS)\
		  $(WIKISCRIPTS)

install: $(SCRIPTS)
	install $(SCRIPTS) $(DEST_DIR)

fac: $(FACSCRIPTS)
	install $(FACSCRIPTS) $(DEST_DIR)

sirius: $(SIRIUSSCRIPTS)
	install $(SIRIUSSCRIPTS) $(DEST_DIR)

wiki: $(WIKISCRIPTS)
	install $(WIKISCRIPTS) $(DEST_DIR)
