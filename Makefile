# Destination directory
DEST_DIR=/usr/local/bin

# Scripts to install
SCRIPTS=gitall.py \
		hosts_update.py \
		pvs_bo.py \
		pvs_li.py \
		pvs_prefix.sh \
		pvs_si.py \
		pvs_ti.py \
		pytrack.py \
		update_ip_on_workstation.sh \
		va \
		vaca.py \
		wiki_backup \
		wiki_clean_backup

install: $(SCRIPTS)
	install $(SCRIPTS) $(DEST_DIR)
