#!/bin/bash


function services_ps_cmd {
	sudo systemctl $1 ioc-as-ps-test
}

function services_ma_cmd {
	# tb
	sudo systemctl $1 ioc-tb-ma-dipole-fam
	sudo systemctl $1 ioc-tb-ma-corrector
	sudo systemctl $1 ioc-tb-ma-multipole
	# bo
	sudo systemctl $1 ioc-bo-ma-dipole-fam
	sudo systemctl $1 ioc-bo-ma-corrector
	sudo systemctl $1 ioc-bo-ma-multipole-fam
	# ts
	sudo systemctl $1 ioc-ts-ma-dipole-fam
	sudo systemctl $1 ioc-ts-ma-corrector
	sudo systemctl $1 ioc-ts-ma-multipole
	# si
	sudo systemctl $1 ioc-si-ma-dipole-fam
	sudo systemctl $1 ioc-si-ma-corrector-slow
	sudo systemctl $1 ioc-si-ma-corrector-fast
	sudo systemctl $1 ioc-si-ma-multipole-fam
	sudo systemctl $1 ioc-si-ma-quadrupole-trim
	# pm
	sudo systemctl $1 ioc-as-pm
}

function services_posang_cmd {
	sudo systemctl $1 ioc-tb-ap-posang
	sudo systemctl $1 ioc-ts-ap-posang
}


if [ "$1" = "start" ]; then
	services_ps_cmd start
	services_ma_cmd start
	services_posang_cmd start
elif [ "$1" = "stop" ]; then
	services_posang_cmd stop
	services_ma_cmd stop
	services_ps_cmd stop
elif [ "$1" = "status" ]; then
	sudo systemctl status ioc-*
fi

