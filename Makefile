develop:
	$(MAKE) develop -C bin/
	$(MAKE) develop -C etc/

install:
	$(MAKE) install -C bin/
	$(MAKE) install -C etc/

install-bbb:
	$(MAKE) install-bbb -C etc/
