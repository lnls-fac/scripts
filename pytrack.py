#!/usr/bin/python

import subprocess
import sys
import os

#default_track_version = './trackc++-release'
default_track_version = 'trackc++'

if len(sys.argv) == 1:
	subprocess.call([default_track_version])
	sys.exit()

if len(sys.argv) > 2:
	print(sys.argv[0] + ': invalid number of arguments!')
	sys.exit()

# loads config
input_file = sys.argv[1]
with open(input_file) as f:
    content = f.readlines()
for line in content:
    exec(line)


try:
	track_linepass_run
except:
	track_linepass_run = False
if track_linepass_run:
	def track_linepass(track_version   = default_track_version,
		     	   flat_filename   = track_linepass_flatfilename,
		     	   energy          = ebeam_energy,
       		     	   harmonic_number = harmonic_number,
	     	     	   cavity_state    = cavity_state,
	     	     	   radiation_state = radiation_state,
		     	   vchamber_state  = vchamber_state,
	    		   start_element   = track_linepass_start_element,
		     	   rx0             = track_linepass_rx0,
                     	   px0             = track_linepass_px0,
		     	   ry0             = track_linepass_ry0,
                     	   py0             = track_linepass_py0,
		     	   de0             = track_linepass_de0,
                     	   dl0             = track_linepass_dl0):
	
		args = [track_version, 'track_linepass', 
			str(flat_filename),
			str(energy), 
			str(harmonic_number), 
			str(cavity_state),
			str(radiation_state),
			str(vchamber_state),
			str(start_element),
			str(rx0), str(px0),
			str(ry0), str(py0),
			str(de0), str(dl0),
			]
		subprocess.call(args)


try:
	dynap_xy_run
except:
	dynap_xy_run = False
if dynap_xy_run:
	def dynap_xy(track_version   = default_track_version,
		     flat_filename   = dynap_xy_flatfilename,
		     energy          = ebeam_energy,
       		     harmonic_number = harmonic_number,
	     	     cavity_state    = cavity_state,
	     	     radiation_state = radiation_state,
		     vchamber_state  = vchamber_state,
	     	     de              = dynap_xy_de,
	     	     nr_turns        = dynap_xy_nr_turns,
	      	     x_nrpts         = dynap_xy_x_nrpts,
	     	     x_min           = dynap_xy_x_min,
	     	     x_max           = dynap_xy_x_max,
	     	     y_nrpts         = dynap_xy_y_nrpts,
	     	     y_min           = dynap_xy_y_min,
	     	     y_max           = dynap_xy_y_max):
	
		args = [track_version, 'dynap_xy', 
			str(flat_filename),
			str(energy), 
			str(harmonic_number), 
			str(cavity_state),
			str(radiation_state),
			str(vchamber_state),
			str(de),
			str(nr_turns),
			str(x_nrpts), str(x_min), str(x_max),
			str(y_nrpts), str(y_min), str(y_max),
			]
		subprocess.call(args)

try:
	dynap_ex_run
except:
	dynap_ex_run = False
if dynap_ex_run:
	def dynap_ex(track_version   = default_track_version,
		     flat_filename   = dynap_ex_flatfilename,
		     energy          = ebeam_energy,
       		     harmonic_number = harmonic_number,
	     	     cavity_state    = cavity_state,
	     	     radiation_state = radiation_state,
		     vchamber_state  = vchamber_state,
	     	     y               = dynap_ex_y,
	     	     nr_turns        = dynap_ex_nr_turns,
	      	     e_nrpts         = dynap_ex_e_nrpts,
	     	     e_min           = dynap_ex_e_min,
	     	     e_max           = dynap_ex_e_max,
	     	     x_nrpts         = dynap_ex_x_nrpts,
	     	     x_min           = dynap_ex_x_min,
	     	     x_max           = dynap_ex_x_max):
	
		subprocess.call([track_version, 'dynap_ex', 
			str(flat_filename),
			str(energy), 
			str(harmonic_number), 
			str(cavity_state),
			str(radiation_state),
			str(vchamber_state),
			str(y),
			str(nr_turns),
			str(e_nrpts), str(e_min), str(e_max),
			str(x_nrpts), str(x_min), str(x_max),
			]
		)	

try:
	dynap_ma_run
except:
	dynap_ma_run = False
if dynap_ma_run:
	def dynap_ma(track_version   = default_track_version,
		     flat_filename   = dynap_ma_flatfilename,
		     energy          = ebeam_energy,
       		     harmonic_number = harmonic_number,
	     	     cavity_state    = cavity_state,
	     	     radiation_state = radiation_state,
		     vchamber_state  = vchamber_state,
	     	     nr_turns        = dynap_ma_nr_turns,
		     y0              = 30e-6,
		     e_e0            = dynap_ma_e_e0,
		     e_tol           = dynap_ma_e_tol,
		     s_min           = dynap_ma_s_min,
		     s_max           = dynap_ma_s_max,
		     fam_names       = dynap_ma_fam_names):
	
		args = [track_version, 'dynap_ma', 
			str(flat_filename),
			str(energy), 
			str(harmonic_number), 
			str(cavity_state),
			str(radiation_state),
			str(vchamber_state),
			str(nr_turns),
			str(y0),
			str(e_e0), str(e_tol),
			str(s_min), str(s_max)]
		for famname in fam_names:
			args.append(famname)
		subprocess.call(args)


if __name__ == "__main__":
	
	''' DYNAP_XY '''	
	if dynap_xy_run:
		dynap_xy()

	''' DYNAP_EX '''	
	if dynap_ex_run:
		dynap_ex()

	''' DYNAP_MA '''
	if dynap_ma_run:
		dynap_ma()

	''' LINEPASS '''
	if track_linepass_run:
		track_linepass()


	

