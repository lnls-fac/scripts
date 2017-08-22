#!/bin/bash


function services_ps_cmd {
	sudo systemctl $1 ioc-as-ps-test > /dev/null 2>&1
}

function services_vaca_cmd {
	sudo systemctl $1 ioc-as-vaca.service > /dev/null 2>&1
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
	#sudo systemctl $1 ioc-as-pm # Need improvement so that service does not trigger error without ps ioc.
}

function services_posang_cmd {
	sudo systemctl $1 ioc-tb-ap-posang
	sudo systemctl $1 ioc-ts-ap-posang
}

function services_ti_cmd {
  sudo systemctl $1 ioc-as-ti-bo-mags.service
  sudo systemctl $1 ioc-as-ti-clocks.service
  sudo systemctl $1 ioc-as-ti-events.service
  sudo systemctl $1 ioc-as-ti-li-all.service
  sudo systemctl $1 ioc-as-ti-others.service
  sudo systemctl $1 ioc-as-ti-si-bo-bpms.service
  sudo systemctl $1 ioc-as-ti-si-corrs.service
  sudo systemctl $1 ioc-as-ti-si-dig.service
  sudo systemctl $1 ioc-as-ti-si-dip-quads.service
  sudo systemctl $1 ioc-as-ti-si-sexts-skews.service
}

function services_sofb_cmd {
	sudo systemctl $1 ioc-si-ap-orbit.service
	sudo systemctl $1 ioc-si-ap-sofb.service
}

ps_server=vaca
if [ "$2" = "ps-test" ]; then
	ps_server=ps-test
fi

if [ "$1" = "start" ]; then
	sudo systemctl daemon-reload
	if [ "$ps_server" = "vaca" ]; then
		services_vaca_cmd start
		echo "waiting for VACA..."
		sleep 65.0
	else
		services_ps_cmd start
	fi
	services_ma_cmd start
	services_ti_cmd start
	services_posang_cmd start
	services_sofb_cmd start
elif [ "$1" = "stop" ]; then
	services_vaca_cmd stop 
	services_ps_cmd stop 
	services_ma_cmd stop
	services_ti_cmd stop
	services_posang_cmd stop
	services_sofb_cmd stop
	sudo systemctl reset-failed
elif [ "$1" = "status" ]; then
	sudo systemctl status ioc-*
fi
