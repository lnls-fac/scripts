#!/usr/bin/env python3

import subprocess
import sys
import os
from apsuite.trackcpp_utils import *

if __name__ == "__main__":

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

    # -- dynap_xy --
    try:
        dynap_xy_run
    except:
        dynap_xy_run = False
    if dynap_xy_run:
        dynap_xy(track_version   = default_track_version,
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
                 y_max           = dynap_xy_y_max,
                 nr_threads      = dynap_xy_nr_threads)

    # -- dynap_ex --
    try:
        dynap_ex_run
    except:
        dynap_ex_run = False
    if dynap_ex_run:
        dynap_ex(track_version   = default_track_version,
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
                 x_max           = dynap_ex_x_max,
                 nr_threads      = dynap_ex_nr_threads)

    # -- dynap_ma --
    try:
        dynap_ma_run
    except:
        dynap_ma_run = False
    if dynap_ma_run:
        dynap_ma(track_version   = default_track_version,
                 flat_filename   = dynap_ma_flatfilename,
                 energy          = ebeam_energy,
                 harmonic_number = harmonic_number,
                 cavity_state    = cavity_state,
                 radiation_state = radiation_state,
                 vchamber_state  = vchamber_state,
                 nr_turns        = dynap_ma_nr_turns,
                 y0              = dynap_ma_y0,
                 e_init          = dynap_ma_e_init,
                 e_delta         = dynap_ma_e_delta,
                 nr_steps_back   = dynap_ma_nr_steps_back,
                 rescale         = dynap_ma_rescale,
                 nr_iterations   = dynap_ma_nr_iterations,
                 s_min           = dynap_ma_s_min,
                 s_max           = dynap_ma_s_max,
                 nr_threads      = dynap_ma_nr_threads,
                 fam_names       = dynap_ma_fam_names)


    # -- dynap_pxa --
    try:
        dynap_pxa_run
    except:
        dynap_pxa_run = False
    if dynap_pxa_run:
        dynap_pxa(track_version   = default_track_version,
                  flat_filename   = dynap_pxa_flatfilename,
                  energy          = ebeam_energy,
                  harmonic_number = harmonic_number,
                  cavity_state    = cavity_state,
                  radiation_state = radiation_state,
                  vchamber_state  = vchamber_state,
                  nr_turns        = dynap_pxa_nr_turns,
                  y0              = dynap_pxa_y0,
                  e_init          = dynap_pxa_px_init,
                  e_delta         = dynap_pxa_px_delta,
                  nr_steps_back   = dynap_pxa_nr_steps_back,
                  rescale         = dynap_pxa_rescale,
                  nr_iterations   = dynap_pxa_nr_iterations,
                  s_min           = dynap_pxa_s_min,
                  s_max           = dynap_pxa_s_max,
                  nr_threads      = dynap_pxa_nr_threads,
                  fam_names       = dynap_pxa_fam_names)

    # -- dynap_pya --
    try:
        dynap_pya_run
    except:
        dynap_pya_run = False
    if dynap_pya_run:
        dynap_pya(track_version   = default_track_version,
                      flat_filename   = dynap_pya_flatfilename,
                      energy          = ebeam_energy,
                      harmonic_number = harmonic_number,
                      cavity_state    = cavity_state,
                      radiation_state = radiation_state,
                      vchamber_state  = vchamber_state,
                      nr_turns        = dynap_pya_nr_turns,
                      y0              = dynap_pya_y0,
                      e_init          = dynap_pya_py_init,
                      e_delta         = dynap_pya_py_delta,
                      nr_steps_back   = dynap_pya_nr_steps_back,
                      rescale         = dynap_pya_rescale,
                      nr_iterations   = dynap_pya_nr_iterations,
                      s_min           = dynap_pya_s_min,
                      s_max           = dynap_pya_s_max,
                      nr_threads      = dynap_pya_nr_threads,
                      fam_names       = dynap_pya_fam_names)

    # -- dynap_xyfmap --
    try:
        dynap_xyfmap_run
    except:
        dynap_xyfmap_run = False
    if dynap_xyfmap_run:
        dynap_xyfmap(track_version   = default_track_version,
                         flat_filename   = dynap_xyfmap_flatfilename,
                         energy          = ebeam_energy,
                         harmonic_number = harmonic_number,
                         cavity_state    = cavity_state,
                         radiation_state = radiation_state,
                         vchamber_state  = vchamber_state,
                         de              = dynap_xyfmap_de,
                         nr_turns        = dynap_xyfmap_nr_turns,
                         x_nrpts         = dynap_xyfmap_x_nrpts,
                         x_min           = dynap_xyfmap_x_min,
                         x_max           = dynap_xyfmap_x_max,
                         y_nrpts         = dynap_xyfmap_y_nrpts,
                         y_min           = dynap_xyfmap_y_min,
                         y_max           = dynap_xyfmap_y_max,
                         nr_threads      = dynap_xyfmap_nr_threads)

    # -- dynap_exfmap --
    try:
        dynap_exfmap_run
    except:
        dynap_exfmap_run = False
    if dynap_exfmap_run:
        dynap_exfmap(track_version   = default_track_version,
                         flat_filename   = dynap_exfmap_flatfilename,
                         energy          = ebeam_energy,
                         harmonic_number = harmonic_number,
                         cavity_state    = cavity_state,
                         radiation_state = radiation_state,
                         vchamber_state  = vchamber_state,
                         y               = dynap_exfmap_y,
                         nr_turns        = dynap_exfmap_nr_turns,
                         e_nrpts         = dynap_exfmap_e_nrpts,
                         e_min           = dynap_exfmap_e_min,
                         e_max           = dynap_exfmap_e_max,
                         x_nrpts         = dynap_exfmap_x_nrpts,
                         x_min           = dynap_exfmap_x_min,
                         x_max           = dynap_exfmap_x_max,
                         nr_threads      = dynap_exfmap_nr_threads)

    # -- track_linepass --
    try:
        track_linepass_run
    except:
        track_linepass_run = False
    if track_linepass_run:
        track_linepass(track_version   = default_track_version,
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
                       dl0             = track_linepass_dl0)
