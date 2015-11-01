#!/usr/bin/env python3

import os as _os
import numpy as _np
import optparse as _optparse
from guidata.qt import QtGui, QtCore

import sirius, pyaccel

def directories_dialog(name='Select Directories'):
    ok = True
    def _pressed_cancel():
        nonlocal ok
        Fi.close()
        ok &= False

    try:
        app = QtGui.QApplication([])
    except RuntimeError:
        pass

    Fi = QtGui.QFileDialog()
    Fi.setWindowTitle(name)
    Fi.setOption(Fi.DontUseNativeDialog, True)
    Fi.setFileMode(Fi.DirectoryOnly)
    for view in Fi.findChildren(QtGui.QListView):
        if isinstance(view.model(), QtGui.QFileSystemModel):
             view.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
    for view in Fi.findChildren(QtGui.QTreeView):
        if isinstance(view.model(), QtGui.QFileSystemModel):
             view.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
    for view in Fi.findChildren(QtGui.QPushButton):
        if view.text().lower().startswith('cancel'):
            view.clicked.connect(_pressed_cancel)

    Fi.show()
    QtCore.QCoreApplication.instance().exec_()

    return ok, Fi.selectedFiles()

def input_dialog(prompt,def_answer=None,name='Type Parameters'):
    ok = False
    def _pressed_ok():
        nonlocal ok
        w.close()
        ok |= True
    def _pressed_cancel():
        nonlocal ok
        w.close()
        ok &= False

    if isinstance(prompt,str): prompt = [prompt]
    if def_answer is None: def_answer = len(prompt)*['']
    if isinstance(def_answer,str): def_answer = [def_answer]
    if len(prompt) != len(def_answer):
        raise IndexError("'prompt' and 'def_answer' must be the same length.")

    try:
        app = QtGui.QApplication([])
    except RuntimeError:
        pass
    w = QtGui.QWidget()
    w.setWindowTitle(name)
    grid = QtGui.QGridLayout()
    grid.setSpacing(10)
    edit = []
    for i in range(len(prompt)):
        title  = QtGui.QLabel(prompt[i])
        edit  += [QtGui.QLineEdit()]
        if def_answer is not None: edit[i].setText(def_answer[i])
        grid.addWidget(title, 2*i,  0,1,2)
        grid.addWidget(edit[i], 2*i+1, 0,1,2)
    qbtn = QtGui.QPushButton('Ok', w)
    qbtn.clicked.connect(_pressed_ok)
    qbtn.resize(qbtn.sizeHint())
    grid.addWidget(qbtn, 2*(i+1), 0)
    qbtn = QtGui.QPushButton('Cancel', w)
    qbtn.clicked.connect(_pressed_cancel)
    qbtn.resize(qbtn.sizeHint())
    grid.addWidget(qbtn, 2*(i+1), 1)
    w.setLayout(grid)
    w.setGeometry(300, 300, i*50, 50)
    w.setWindowTitle('InputDialog')
    w.show()
    QtCore.QCoreApplication.instance().exec_()

    text = []
    for ed in edit:
        text += [ed.text()]
    return ok, text

def find_right_folders(paths):
    pathnames = []
    for path in paths:
        listing = _os.listdir(path)
        if any([i.startswith('rms') for i in listing]):
            pathnames += [path]
            continue
        paths2 = []
        for file in listing:
            if file.startswith(('dynap_xy_out.txt','dynap_ex_out.txt','dynap_ma_out.txt')):
                pathnames += [path]
            else:
                if _os.path.isdir(file) and  not file.startswith(('.','..')):
                    paths2 += [_os.path.sep.join((path,file))]
        if paths2: pathnames += [find_right_folders(paths2)]
    return pathnames

def trackcpp_da_ma_lt(path=None):

    # users selects submachine
    prompt = ['Submachine (bo/si)', 'energy [GeV]', 'Number of plots','Types of plots']
    defaultanswer = ['si', '3.0', '2','ma xy ex']
    answer = []
    ok, answer = input_dialog(prompt,defaultanswer, 'Main Parameters')
    if not ok: return
    energy = float(answer[1]) * 1e9
    n_calls = round(float(answer[2]))

    xy = True if answer[3].find('xy') >= 0 else False
    ex = True if answer[3].find('ex') >= 0 else False
    ma = True if answer[3].find('ma') >= 0 else False

    if answer[0].find('bo') >= 0:
        if path is None: path = _os.path.sep.join(['home','fac_files','data',
                                                'sirius','bo','beam_dynamics'])
        acc = getattr(sirius,'bo')
        acc = acc.create_accelerator()
        acc.energy = energy
        if energy == 0.15 * 1e9:
            # BOOSTER (equillibirum parameters from LINAC)
            emit0   = 170e-9  # linac
            sigE    = 5.0e-3  # linac
            sigS    = 11.2e-3 # linac
            accepRF = 0.033
            K       = 0.0002
            I       = 0.6
            nrBun   = 1
        else:
            eqpar = pyaccel.optics.get_equilibrium_parameters(acc)
            emit0 = eqpar['natural_emittance']
            sigE  = eqpar['natural_energy_spread']
            sigS  = eqpar['bunch_length']
            K     = 0.0002
            I     = 0.6
            nrBun = 1
            accepRF = eqpar['rf_energy_acceptance']
    else:
        if path is None: path = _os.path.sep.join(['home','fac_files','data',
                                                'sirius','si','beam_dynamics'])
        acc = getattr(sirius,'si')
        acc = acc.create_accelerator()
        acc.energy = energy

        eqpar = pyaccel.optics.get_equilibrium_parameters(acc)
        # Data given by Natalia
        emit0   = 0.240e-9 #eqpar['natural_emittance']
        sigE    = 9.4e-4   #eqpar['natural_energy_spread']
        sigS    = 3.0e-3   #3.5e-3 # takes IBS into account #sigS  = eqpar['bunch_length']
        K       = 0.01
        I       = 100
        nrBun   = 864
        accepRF = eqpar['rf_energy_acceptance']


    # users selects beam lifetime parameters
    prompt = ['Emitance[nm.rad]', 'Energy spread', 'Bunch length (with IBS) [mm]',
        'Coupling [{]', 'Current [mA]', 'Nr bunches', 'RF Energy Acceptance [{]']
    defaultanswer = [str(emit0/1e-9), str(sigE), str(sigS*1000), str(100*K),
                     str(I), str(nrBun), str(accepRF*100)]
    ok, answer = input_dialog(prompt, defaultanswer, 'Lifetime Parameters')
    if not ok: return
    emit0   = float(answer[0])*1e-9
    sigE    = float(answer[1])
    sigS    = float(answer[2])/1000
    K       = float(answer[3])/100
    I       = float(answer[4])/1000
    nrBun   = int(answer[5])
    accepRF = float(answer[6])/100
    N       = I/nrBun/1.601e-19*ats.revTime

    twi, *_ = pyaccel.optics.calc_twiss(acc,indices='open')

    # parâmetros para a geração das figuras
    color_vec = ['b','r','g','m','c','k','y']
    esp_lin, size_font = 5, 24
    limx, limy, limpe, limne = 12, 3.5, 6, 6

    var_plane = 'x' #determinaçao da abertura dinâmica por varreduda no plano x

    i=0
    while i < n_calls:
        ok, paths = directories_dialog(path,'Selecione pasta com os dados?')
        if if not ok: return
        paths = find_right_folders(paths)

        for path in paths:
            if i >= n_calls: break
            i+=1

            area, aper_xy, aper_ex, ltime, accep = [],[],[],[],[]

            result = [i for i in _os.listdir(path) if _os.path.isdir(i)]
            n_pastas = len(result)
            rms_mode = True
            if n_pastas == 0:
                rms_mode = false
                n_pastas = 1

            na = _os.path.abspath(path).split('/')[1:]
            leg_text = input_dialog('Digite a legenda',na[-3],'Legenda')[1][0]

            lt_prob = 0
            for k in range(n_pastas):
                if rms_mode: path += _os.path.sep + result[i]

                if xy:
                    if _os.path.isfile(_os.path.sep.join([path,'dynap_xy_out.txt'])):
                        aper, a, *_ = trackcpp_load_dynap_xy(path,var_plane)
                        area += [a]
                        aper_xy += [aper]
                    else:
                        print('{0:-2d}-{1:5s}: xynao carregou\n'.format(i,result[k]))
                if ex:
                    if _os.path.isfile(_os.path.sep.join([path,'dynap_ex_out.txt'])):
                        aper, *_ = trackcpp_load_dynap_ex(path)
                        aper_ex += [aper]
                    else:
                        print('{0:-2d}-{1:5s}: ex nao carregou\n'.format(i,result[k]))

                if ma:
                    if _os.path.isfile(_os.path.sep.join([path,'dynap_ma_out.txt'])):
                        pos, aceit, *_ = trackcpp_load_ma_data(path)
                        if _np.isclose(aceit,0).any():
                            lt_prob += 1
                        else:
                            accep += [aceit]
                            Accep['s']   = spos
                            Accep['pos'] = np.mininum(aceit[0], accepRF)
                            Accep['neg'] = np.maximum(aceit[1], -accepRF)
                            # não estou usando alguns outputs
                            LT = lnls_tau_touschek_inverso(params,Accep,twi)
                            ltime += [1/LT['AveRate']/60/60] # em horas
                    else:
                        print('{0:-2d}-{1:5s}: ma nao carregou\n'.format(i,result[k]))

            if xy:
                aper_xy = np.dstack(aper_xy)
                xy_ave  = aper_xy.mean(axis=2)
                neg_ave = xy_ave[0][2]
                area    = np.dstack(area)
                area_ave= area.mean()
            if ex:
                aper_ex = np.dstack(aper_ex)
                ex_ave  = aper_ex.mean(axis=2)
            if ma:
                accep   = np.dstack(accep)*100
                ma_ave  = accep.mean(axis=2)
                ltime   = np.dstack(lifetime)
                lt_ave  = ltime.mean()
            if rms_mode:
                if xy:
                    xy_rms  = aper_xy.std(axis=2,dof=1)
                    neg_rms = xy_rms[0][2]
                    area_rms= area.std(axis=2,dof=1)
                if ex:
                    ex_rms  = aper_ex.std(axis=2,dof=1)
                if ma:
                    rmsAccep = squeeze(std(accep,0,1))*100
                    rmsLT = std(lifetime)

            ########  exposição dos resultados ######

            color = color_vec[i % len(color_vec)]
            ave_conf = dict(linewidth=esp_lin,color=color,linestyle='-',label=leg_text)
            rms_conf = dict(linewidth=2,color=color,linestyle='--')
            if not i:
                if xy and ma:
                    print('\n{0:-20s {1:-15s} {2:-15s} {3:-15s}\n'.format('Config',
                            'Dynap XY [mm^2]', 'Aper@y=0.2 [mm]', 'Lifetime [h]'))
                elif ma:
                    print('\n{0:-20s {1:-15s}\n'.format('Config', 'Lifetime [h]'))
                elif xy:
                    print('\n{0:-20s {1:-15s}\n'.format('Config', 'Dynap XY [mm^2]',
                                                        'Aper@y=0.2 [mm]'))
            if xy or ma:
                print('{0:-20s} '.format(leg_text.upper()))

            if xy:
                if not i:
                    fxy, axy = _plt.subplots()
                    fxy.set_figsize((5,4))
                    axy.grid(True)
                    axy.hold(True)
                    axy.set_xlabel('x [mm]',font_size=size_font)
                    axy.set_ylabel('y [mm]',font_size=size_font)
                    axy.set_xlim([-limx limx])
                    axy.set_ylim([0 limy])
                axy.plot(1000*xy_ave[0,:,0], 1000*xy_ave[0,:,1],**ave_conf)
                if rms_mode:
                    print('{0:5.2f} \x00B1 {1:-5.2f}   {2:5.1f} \x00B1 {-5.1f}   '.format(
                            area_ave*1e6, area_rms*1e6, neg_ave*1e3, neg_rms*1e3),end='')
                    axy.plot(1000*(xy_rms[0,:,0]+xy_ave[0,:,0]),
                             1000*(xy_rms[0,:,1]+xy_ave[0,:,1]),**rms_conf)
                    axy.plot(1000*(xy_rms[0,:,0]-xy_ave[0,:,0]),
                             1000*(xy_rms[0,:,1]-xy_ave[0,:,1]),**rms_conf)
                else:
                    print('{0:5.2f}           {1:5.1f}           '.format(area_ave*1e6, neg_ave*1e3),end='')

            if ex:
                if not i:
                    fex, aex = _plt.subplots()
                    fex.set_figsize((5,4))
                    aex.grid(True)
                    aex.hold(True)
                    aex.set_xlabel(r'$\delta$ [%]',font_size=size_font)
                    aex.set_ylabel('x [mm]',font_size=size_font)
                    aex.set_xlim([-limne limpe])
                    aex.set_ylim([-limx 0])
                aex.plot(1000*ex_ave[0,:,0], 1000*ex_ave[0,:,1],**ave_conf)
                if rms_mode:
                    aex.plot(1000*(ex_rms[0,:,0]+ex_ave[0,:,0]),
                             1000*(ex_rms[0,:,1]+ex_ave[0,:,1]),**rms_conf)
                    aex.plot(1000*(ex_rms[0,:,0]-ex_ave[0,:,0]),
                             1000*(ex_rms[0,:,1]-ex_ave[0,:,1]),**rms_conf)
            if ma:
                #imprime o tempo de vida
                if rms_mode:
                    print('{5.2f} \x00B1 {-5.2f} '.format(aveLT, rmsLT),end='')
                    if lt_prob:
                        print('   *{0:02d) máquinas desprezadas'.format(lt_prob)+
                              ' no cálculo por possuírem aceitancia nula.',end='')
                else:
                    print('{5.2f} ', aveLT)
                if not i:
                    fma, ama = _plt.subplots()
                    fma.set_figsize((7,3.5))
                    ama.grid(True)
                    ama.hold(True)
                    ama.set_xlabel('Pos [m]',font_size=size_font)
                    ama.set_ylabel(r'$\delta$ [%]',font_size=size_font)
                    ama.set_xlim([-limne-0.2,limpe+0.2])
                    ama.set_ylim([0, 52])
                    ama.set(yticklabels=['-5','-2.5','0','2.5','5'],
                            yticks=[-5,-2.5,0,2.5,5], position=[0.10,0.17,0.84,0.73])
                ama.plot(pos,ma_ave,**ave_conf)
                if rms_mode:
                    ama.plot(pos,ma_ave+ma_rms,**rms_conf)
                    ama.plot(pos,ma_ave-ma_rms,**rms_conf)

            if xy or ma: print()


    title_text = input_dialog('Título',name='Digite um Título para os Gráficos')[1][0]

    if xy:
        axy.legend(loc='best')
        axy.set_title('DAXY - ' + title_text)
    if ex:
        aex.legend(loc='best')
        aex.set_title('DAEX - ' + title_text)
    if ma:
        ama.legend(loc='best')
        lnls_drawlattice(the_ring,10, 0, true,0.2, false, falt)
        ama.set_title('MA - ' + title_text)
