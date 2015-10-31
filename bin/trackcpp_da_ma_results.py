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
    esp_lin = 5
    size_font = 24
    limx = 12
    limy = 3.5
    limpe = 6
    limne = 6

    var_plane = 'x' #determinaçao da abertura dinâmica por varreduda no plano x

    leg_text = []

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
            leg_text += input_dialog('Digite a legenda',na[-3],'Legenda')

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
                        spos, aceit, *_ = trackcpp_load_ma_data(path)
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
                YatNegX = xy[0][2]
                area    = np.dstack(area)
            if ex:
                aper_ex = np.dstack(aper_ex)
            if ma:
                accep = np.dstack(accep)*100
                ltime = np.dstack(lifetime)
            if rms_mode:
                if xy:
                    rmsOnda = std(aper_xy,1)
                    rmsYatNegX = rmsOnda(1,3,1)
                    rmsArea = std(area)
                if ex:
                    rmsOffda = std(aper_ex.std(axis=),1)
                if ma:
                    rmsAccep = squeeze(std(accep,0,1))*100
                    rmsLT = std(lifetime)

            ########  exposição dos resultados ######

            color = color_vec[i % len(color_vec)]

            if not i:
                if xy && ma:
                    print('\n{0:-20s {1:-15s} {2:-15s} {3:-15s}\n'.format('Config',
                            'Dynap XY [mm^2]', 'Aper@y=0.2 [mm]', 'Lifetime [h]'))
                elif ma:
                    print('\n{0:-20s {1:-15s}\n'.format('Config', 'Lifetime [h]'))
                elif xy:
                    print('\n{0:-20s {1:-15s}\n'.format('Config', 'Dynap XY [mm^2]',
                                                        'Aper@y=0.2 [mm]'))
            if xy || ma:
                print('{0:-20s} '.format(leg_text[i].upper()))

            if xy:
                if not i:
                    f  = figure('Position',[1,1,896,750])
                    fa = axes('Parent',f,'YGrid','on','XGrid','on','FontSize',size_font)
                    box(fa,'on')
                    hold(fa,'all')
                    xlabel('x [mm]','FontSize',size_font)
                    ylabel('y [mm]','FontSize',size_font)
                    xlim(fa,[-limx limx]);  ylim(fa,[0 limy])
                    plot(fa, 1000*aveOnda(1,:,1), 1000*aveOnda(1,:,2),
                    'Marker','.','LineWidth',esp_lin,'Color',color, 'LineStyle','-');
                if rms_mode
                    fprintf('{0:5.2f} \x00B1 {1:-5.2f}   {2:5.1f} \x00B1 {-5.1f   ',
                            aveArea*1e6, rmsArea*1e6, aveYatNegX*1e3, rmsYatNegX*1e3)
                    plot(fa, 1000*(rmsOnda(1,:,1)+aveOnda(1,:,1)),1000*(rmsOnda(1,:,2)+aveOnda(1,:,2)),
                        'Marker','.','LineWidth',2,'LineStyle','--','Color', color)
                    plot(fa, 1000*(aveOnda(1,:,1)-rmsOnda(1,:,1)),1000*(aveOnda(1,:,2)-rmsOnda(1,:,2)),
                        'Marker','.','LineWidth',2,'LineStyle','--','Color', color)
                else
                    print('{0:5.2f}           {1:5.1f}           '.format(aveArea*1e6, aveYatNegX*1e3))

            if ex
                if i == 1:
                    fdp  = figure('Position',[1,1,896,750]);
                    fdpa = axes('Parent',fdp,'YGrid','on','XGrid','on','FontSize',size_font);
                    box(fdpa,'on'); hold(fdpa,'all');
                    xlabel('\delta [{]','FontSize',size_font);
                    ylabel('x [mm]','FontSize',size_font);
                    xlim(fdpa,[-limne limpe]);  ylim(fdpa,[-limx,0]);
                plot(fdpa, 100*aveOffda(1,:,1),1000*aveOffda(1,:,2),...
                    'Marker','.','LineWidth',esp_lin,'Color',color, 'LineStyle','-');
                if rms_mode
                    pldp(i,1) = plot(fdpa, 100*aveOffda(1,:,1), 1000*(rmsOffda(1,:,2)+aveOffda(1,:,2)),...
                        'Marker','.','LineWidth',2,'LineStyle','--','Color', color);
                    pldp(i,3) = plot(fdpa, 100*aveOffda(1,:,1),1000*(aveOffda(1,:,2)-rmsOffda(1,:,2)),...
                        'Marker','.','LineWidth',2,'LineStyle','--','Color', color);

            if ma
                #imprime o tempo de vida
                if rms_mode
                    fprintf('{5.2f \x00B1 {-5.2f ', aveLT, rmsLT);
                    if lt_prob,
                        fprintf(['   *{02d máquinas desprezadas no cálculo',...
                                ' por possuírem aceitancia nula.'],lt_prob);
                    end
                else
                    fprintf('{5.2f ', aveLT);
                end

                if i == 1
                    flt  = figure('Position',[1, 1, 1296, 553]);
                    falt = axes('Parent',flt,'YGrid','on','FontSize',size_font,...
                                'Position',[0.10 0.17 0.84 0.73],'XGrid','on',...
                                'yTickLabel',{'-5','-2.5','0','2.5','5'},...
                                'YTick',[-5 -2.5 0 2.5 5]);
                    box(falt,'on');  hold(falt,'all');
                    ylim(falt, [-limne-0.2,limpe+0.2]); xlim(falt, [0, 52]);
                    xlabel('Pos [m]','FontSize',size_font);
                    ylabel('\delta [{]','FontSize',size_font);
                end
                pllt(i,:) = plot(falt,spos,aveAccep, 'Marker','.','LineWidth',...
                    esp_lin,'Color',color, 'LineStyle','-');
                if rms_mode;
                    plot(falt,spos,aveAccep + rmsAccep, 'Marker','.','Color',...
                         color,'LineWidth',2,'LineStyle','--');
                    plot(falt,spos,aveAccep - rmsAccep, 'Marker','.','Color',...
                          color,'LineWidth',2,'LineStyle','--');
                end
            end
            if xy || ma, fprintf('\n'); end
            drawnow;


    title_text = input_dialog('Título',name='Digite um Título para os Gráficos')[0]

    if xy:
        legend(pl(:,2),'show',leg_text, 'Location','Best')
        title(fa,'DAXY - ' + title_text)
    if ex:
        legend(pldp(:,2),'show',leg_text, 'Location','Best')
        title(fdpa,['DAEX - ' + title_text)
    if ma:
        legend(pllt(:,1),'show',leg_text, 'Location','Best')
        lnls_drawlattice(the_ring,10, 0, true,0.2, false, falt)
        title(falt,'MA - ' + title_text)
    ########################################

    leg_text
    paths = []
    while i < n_calls:
        ok, dirs = directories_dialog(path,'Selecione pasta com os dados?')
        if if not ok: return
        paths += find_right_folders(dirs)

        for pat in paths:
            if i >= n_calls: break
            i+=1
            na = _os.path.abspath(pat).split('/')[1:]
            leg_text += input_dialog('Digite a legenda',na[-3],'Legenda')

    title_text = input_dialog('Título',name='Digite um Título para os Gráficos')[0]

    if xy:
        A, B = deal_xy(paths,leg_text,title_text)

        if xy && ma:
            print('\n{0:-20s {1:-15s} {2:-15s} {3:-15s}\n'.format('Config',
                    'Dynap XY [mm^2]', 'Aper@y=0.2 [mm]', 'Lifetime [h]'))
        elif ma:
            print('\n{0:-20s {1:-15s}\n'.format('Config', 'Lifetime [h]'))
        elif xy:
            print('\n{0:-20s {1:-15s}\n'.format('Config', 'Dynap XY [mm^2]',
                                                'Aper@y=0.2 [mm]'))
    if xy || ma:
        print('{0:-20s} '.format(leg_text[i].upper()))

    if xy || ma, fprintf('\n')


    def deal_xy(paths,leg_text,title_text):

        for ii,path in enumerate(paths):

            area, aper_xy, aper_ex, ltime, accep = [],[],[],[],[]

            result = [i for i in _os.listdir(path) if _os.path.isdir(i)]
            n_pastas = len(result)
            rms_mode = True
            if n_pastas == 0:
                rms_mode = false
                n_pastas = 1

            for k in range(n_pastas):
                if rms_mode: path += _os.path.sep + result[i]

                if _os.path.isfile(_os.path.sep.join([path,'dynap_xy_out.txt'])):
                    aper, a, *_ = trackcpp_load_dynap_xy(path,var_plane)
                    area += [a]
                    aper_xy += [aper]
                else:
                    print('{0:-2d}-{1:5s}: xy nao carregou\n'.format(i,result[k]))

            aper_xy = np.dstack(aper_xy)
            xy_ave  = aper_xy.mean(axis=2)
            YatNegX = xy[0][2]
            area    = np.dstack(area)
            if rms_mode:
                rmsOnda = std(aper_xy,1)
                rmsYatNegX = rmsOnda(1,3,1)
                rmsArea = std(area)

            ########  exposição dos resultados ######
            color = color_vec[i % len(color_vec)]

            if not i:
                f  = figure('Position',[1,1,896,750])
                fa = axes('Parent',f,'YGrid','on','XGrid','on','FontSize',size_font)
                box(fa,'on')
                hold(fa,'all')
                xlabel('x [mm]','FontSize',size_font)
                ylabel('y [mm]','FontSize',size_font)
                xlim(fa,[-limx limx]);  ylim(fa,[0 limy])
                plot(fa, 1000*aveOnda(1,:,1), 1000*aveOnda(1,:,2),
                'Marker','.','LineWidth',esp_lin,'Color',color, 'LineStyle','-');
            if rms_mode
                fprintf('{0:5.2f} \x00B1 {1:-5.2f}   {2:5.1f} \x00B1 {-5.1f   ',
                        aveArea*1e6, rmsArea*1e6, aveYatNegX*1e3, rmsYatNegX*1e3)
                plot(fa, 1000*(rmsOnda(1,:,1)+aveOnda(1,:,1)),1000*(rmsOnda(1,:,2)+aveOnda(1,:,2)),
                    'Marker','.','LineWidth',2,'LineStyle','--','Color', color)
                plot(fa, 1000*(aveOnda(1,:,1)-rmsOnda(1,:,1)),1000*(aveOnda(1,:,2)-rmsOnda(1,:,2)),
                    'Marker','.','LineWidth',2,'LineStyle','--','Color', color)
            else
                print('{0:5.2f}           {1:5.1f}           '.format(aveArea*1e6, aveYatNegX*1e3))

            if i == 1:
                fdp  = figure('Position',[1,1,896,750]);
                fdpa = axes('Parent',fdp,'YGrid','on','XGrid','on','FontSize',size_font);
                box(fdpa,'on'); hold(fdpa,'all');
                xlabel('\delta [{]','FontSize',size_font);
                ylabel('x [mm]','FontSize',size_font);
                xlim(fdpa,[-limne limpe]);  ylim(fdpa,[-limx,0]);
            plot(fdpa, 100*aveOffda(1,:,1),1000*aveOffda(1,:,2),...
                'Marker','.','LineWidth',esp_lin,'Color',color, 'LineStyle','-');
            if rms_mode
                pldp(i,1) = plot(fdpa, 100*aveOffda(1,:,1), 1000*(rmsOffda(1,:,2)+aveOffda(1,:,2)),...
                    'Marker','.','LineWidth',2,'LineStyle','--','Color', color);
                pldp(i,3) = plot(fdpa, 100*aveOffda(1,:,1),1000*(aveOffda(1,:,2)-rmsOffda(1,:,2)),...
                    'Marker','.','LineWidth',2,'LineStyle','--','Color', color);



        legend(pl(:,2),'show',leg_text, 'Location','Best')
        title(fa,'DAXY - ' + title_text)
