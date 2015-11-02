#!/usr/bin/env python3

import os as _os
import numpy as _np
import optparse as _optparse
from guidata.qt import QtGui, QtCore
import matplotlib.pyplot as _plt

import sirius, pyaccel
import mathphys as _mp

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

    # The folder selection is also selecting its parent:
    sel_files = Fi.selectedFiles()
    sel_files2 = set(sel_files)
    for fi1 in sel_files:
        for fi2 in sel_files:
            if fi2 != fi1 and fi1 in fi2:
                sel_files2 -= {fi1}
                break

    return ok, list(sel_files2)

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
                file = _os.path.sep.join((path,file))
                if _os.path.isdir(file) and  not file.startswith(('.','..')):
                    paths2 += [file]
        if paths2: pathnames += find_right_folders(paths2)
    return pathnames

def trackcpp_load_dynap_xy(path, var_plane='x'):
    # Carrego os dados:
    nr_header_lines = 13
    fname = _os.path.sep.join([path, 'dynap_xy_out.txt'])
    turn,plane,x,y = _np.loadtxt(fname,skiprows=nr_header_lines,usecols=(1,3,5,6),unpack=True)

    # Identifico quantos x e y existem:
    nx = len(_np.unique(x))
    ny = x.shape[0]//nx

    # Redimensiono para que todos os x iguais fiquem na mesma coluna:
    # o flipud é usado porque y é decrescente:
    fun = lambda x: _np.flipud(x.reshape((nx,ny)).T)
    turn, plane, x, y = fun(turn), fun(plane), fun(x), fun(y)
    dados = dict(x=x,y=y,plane=plane,turn=turn)

    # E identifico a borda da DA:
    if var_plane =='y':
        lost = plane != 0
        ind = lost.argmax(axis=0)
        # Caso a abertura vertical seja maior que o espaço calculado:
        anyloss = lost.any(axis=0)
        ind = ind*anyloss + (~anyloss)*(y.shape[0]-1)

        # por fim, defino a DA:
        h = x[0]
        v = y[:,0][ind]
        aper = _np.vstack([h,v])
        area = _np.trapz(v,x=h)
    else:
        idx  = x > 0
        # para x negativo:
        x_mi     = _np.fliplr(x[~idx].reshape((ny,-1)))
        plane_mi = _np.fliplr(plane[~idx].reshape((ny,-1)))
        lost  = plane_mi != 0
        ind_neg = lost.argmax(axis=1)
        # Caso a abertura horizontal seja maior que o espaço calculado:
        anyloss = lost.any(axis=1)
        ind_neg = ind_neg*anyloss + (~anyloss)*(x_mi.shape[1]-1)

        h_neg = x_mi[0][ind_neg]
        v_neg = y[:,0]
        aper_neg = _np.vstack([h_neg,v_neg])
        area_neg = _np.trapz(h_neg,x=v_neg)

        #para x positivo
        x_ma = x[idx].reshape((ny,-1))
        plane_ma = plane[idx].reshape((ny,-1))
        lost    = plane_ma != 0
        ind_pos = lost.argmax(axis=1)
        # Caso a abertura horizontal seja maior que o espaço calculado:
        anyloss = lost.any(axis=1)
        ind_pos = ind_pos*anyloss + (~anyloss)*(x_ma.shape[1]-1)

        # por fim, defino a DA em x positivo:
        h_pos = x_ma[0][ind_pos]
        v_pos = y[:,0]
        aper_pos = _np.fliplr(_np.vstack([h_pos,v_pos]))
        area_pos = _np.trapz(h_pos,x=v_pos)

        aper = _np.hstack([aper_neg,aper_pos])
        area = -_np.trapz(aper[0],x=aper[1])

    return aper, area, dados

def trackcpp_load_dynap_ex(path):
    # Carrego os dados:
    nr_header_lines = 13
    fname = _os.path.sep.join([path, 'dynap_ex_out.txt'])
    turn,plane,x,en = _np.loadtxt(fname,skiprows=nr_header_lines,usecols=(1,3,5,7),unpack=True)

    # Identifico quantos x e y existem:
    ne = len(_np.unique(x))
    nx = x.shape[0]//ne

    # Redimensiono para que todos os x iguais fiquem na mesma linha:
    fun = lambda x: x.reshape((nx,ne)).T
    turn, plane, x, en = fun(turn), fun(plane), fun(x), fun(en)
    dados = dict(x=x,en=en,plane=plane,turn=turn)

    lost = plane != 0
    ind = lost.argmax(axis=0)
    # Caso a abertura horizontal seja maior que o espaço calculado:
    anyloss = lost.any(axis=0)
    ind = ind*anyloss + (~anyloss)*(x.shape[0]-1)

    # por fim, defino a DA:
    h = en[0]
    v = x[:,0][ind]
    aper = _np.vstack([h,v])

    return aper, dados

def trackcpp_load_ma_data(path):

    # Carrego os dados:
    nr_header_lines = 13
    fname = _os.path.sep.join([path, 'dynap_ma_out.txt'])
    turn,el,pos,en = _np.loadtxt(fname,skiprows=nr_header_lines,usecols=(1,2,4,7),unpack=True)

    pos  = pos[::2]
    # the -abs is for cases where the momentum aperture is less than the tolerance
    accep = _np.vstack([ en[1::2], -_np.abs(en[0::2]) ])
    nLost = _np.vstack([turn[1::2],turn[0::2]])
    eLost = _np.vstack([el[1::2],  el[0::2]])

    return pos, accep, nLost, eLost

def lnls_tau_touschek_inverso(Accep,twispos,twiss,emit0,E,N,sigE,sigS,K):
    """ calcula o inverso do tempo de vida Touschek.

      Saídas:
          Resp = estrutura com campos:
              Rate = taxa de perda de elétrons ao longo do anel [1/s]
              AveRate = Taxa média de perda de elétrons [1/s]
              Pos  = Posição do anel onde foi calculada a taxa [m]
              Volume = Volume do feixe ao longo do anel [m^3]

      Entradas:
          params = estrutura com campos:
              emit0 = emitância natural [m rad]
              E     = energia das partículas [eV]
              N     = número de elétrons por bunch
              sigE  = dispersão de energia relativa sigE,
              sigS  = comprimento do bunch [m]
              K     = fator de acoplamento (emity = K*emitx)

          Accep = estrutura com campos:
              pos = aceitância positiva para uma seleção de pontos do anel;
              neg = aceitância negativa para uma seleção de pontos do anel;
                       (lembrar: min(accep_din, accep_rf))
              s   = posição longitudinal dos pontos para os quais a
                       aceitância foi calculada.

          Optics = estrutura com as funções óticas ao longo do trecho
                  para o qual setá calculado o tempo de vida:
                       pos,   betax,    betay,  etax,   etay,
                              alphax,   alphay, etaxl,  etayl

      CUIDADO: os limites de cálculo são definidos pelos pontos
         inicial e final da Aceitância e não das funções ópticas.
    """

    c   = _mp.constants.light_speed
    me  = _mp.constants.electron_mass
    Qe  = _mp.constants.elementary_charge
    mu0 = _mp.constants.vacuum_permeability
    ep0 = _mp.constants.vacuum_permitticity
    r0  = _mp.constants.electron_radius
    m0  = _mp.constants.electron_rest_energy * _mp.units.joule_2_eV

    gamma = E/m0

    # Tabela para interpolar d_touschek
    dic = _mp.utils.load_pickle('/home/fac_files/code/scripts/bin/TouschekDIntegralTable')
    x = dic['x']
    y = dic['y']

    s    = Accep['s']
    accp = Accep['pos']
    accn = Accep['neg']
    # calcular o tempo de vida a cada 10 cm do anel:
    npoints = int((s[-1] - s[0])/0.1)
    s_calc = _np.linspace(s[0], s[-1], npoints)

    d_accp  = _np.interp(s_calc,s, accp)
    d_accn  = _np.interp(s_calc,s,-accn)
    # if momentum aperture is 0, set it to 1e-4:
    d_accp[d_accp==0] = 1e-4
    d_accn[d_accn==0] = 1e-4

    _, ind = _np.unique(twispos,return_index=True)

    betax  = _np.interp(s_calc, twispos[ind], twiss.betax[ind])
    alphax = _np.interp(s_calc, twispos[ind], twiss.alphax[ind])
    etax   = _np.interp(s_calc, twispos[ind], twiss.etax[ind])
    etaxl  = _np.interp(s_calc, twispos[ind], twiss.etapx[ind])
    betay  = _np.interp(s_calc, twispos[ind], twiss.betay[ind])
    etay   = _np.interp(s_calc, twispos[ind], twiss.etay[ind])

    # Volume do bunch
    sigX = _np.sqrt(betay*(K/(1+K))*emit0 + etay**2*sigE**2)
    sigY = _np.sqrt(betax*(1/(1+K))*emit0 + etax**2*sigE**2)
    V = sigS * sigX * sigY


    # Tamanho betatron horizontal do bunch
    Sx2 = 1/(1+K) * emit0 * betax

    fator = betax*etaxl + alphax*etax
    A1 = 1/(4*sigE**2) + (etax**2 + fator**2)/(4*Sx2)
    B1 = betax*fator/(2*Sx2)
    C1 = betax**2/(4*Sx2) - B1**2/(4*A1)

    # Limite de integração inferior
    ksip = (2*_np.sqrt(C1)/gamma * d_accp)**2
    ksin = (2*_np.sqrt(C1)/gamma * d_accn)**2

    # Interpola d_touschek
    Dp = _np.interp(ksip,x,y,left=0.0,right=0.0)
    Dn = _np.interp(ksin,x,y,left=0.0,right=0.0)

    # Tempo de vida touschek inverso
    Ratep = (r0**2*c/8/_np.pi)*N/gamma**2 / d_accp**3 * Dp / V
    Raten = (r0**2*c/8/_np.pi)*N/gamma**2 / d_accn**3 * Dn / V
    rate = (Ratep + Raten) / 2

    # Tempo de vida touschek inverso médio
    ave_rate = _np.trapz(rate,x=s_calc) / ( s_calc[-1] - s_calc[0] )
    resp = dict(rate=rate,ave_rate=ave_rate,volume=V,pos=s_calc)

    return resp

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
        accepRF = eqpar[0]['rf_energy_acceptance']


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
    N       = I/nrBun/_mp.constants.elementary_charge*(acc.length/_mp.constants.light_speed)
    params  = dict(emit0=emit0, sigE=sigE, sigS=sigS, K=K, N=N, E=energy)

    twi, *_ = pyaccel.optics.calc_twiss(acc,indices='open')
    twispos = pyaccel.lattice.find_spos(acc,indices='open')

    # parâmetros para a geração das figuras
    color_vec = ['b','r','g','m','c','k','y']
    esp_lin, size_font = 5, 24
    limx, limy, limpe, limne = 12, 3.5, 6, 6

    var_plane = 'x' #determinaçao da abertura dinâmica por varreduda no plano x

    if n_calls == 1:
        pass
        # size_font = 16
        # type_colormap = 'Jet'
        #
        # mostra = 0 # 0 = porcentagem de part perdidas
        # # 1 = número medio de voltas
        # # 2 = posicao em que foram perdidas
        # # 3 = plano em que foram perdidas
        # ok, paths = directories_dialog('Selecione pasta com os dados?')
        # if not ok: return
        #
        # path = find_right_folders(paths)[0]
        #
        # area, aper_xy, aper_ex, ltime, accep = [],[],[],[],[]
        #
        # result = sorted([ii for ii in _os.listdir(path) if _os.path.isdir(_os.path.sep.join([path,ii]))])
        # n_pastas = len(result)
        #
        # lt_prob = 0
        # for k in range(n_pastas):
        #     pathn = _os.path.sep.join([path,result[k]])
        #
        #     if xy:
        #         if _os.path.isfile(_os.path.sep.join([pathn,'dynap_xy_out.txt'])):
        #             _, a, dados1 = trackcpp_load_dynap_xy(pathn,var_plane)
        #             if mostra == 0:
        #                 idx_daxy = idx_daxy + (dados1['plane'] == 0)
        #             elif mostra == 1:
        #                 idx_daxy = idx_daxy + dados1['turn']
        #             elif mostra == 2:
        #                 idx_daxy = idx_daxy + (dados1['pos'] % 51.8396)
        #             elif mostra == 3:
        #                 idx_daxy = idx_daxy + dados1['plane']
        #         else:
        #             print('{0:02d}-{1:5s}: xy nao carregou\n'.format(i,result[k]))
        #     if ex:
        #         if _os.path.isfile(_os.path.sep.join([pathn,'dynap_ex_out.txt'])):
        #             _, dados2 = trackcpp_load_dynap_ex(pathn)
        #             if mostra == 0:
        #                 idx_daxy = idx_daxy + (dados2['plane'] == 0)
        #             elif mostra == 1:
        #                 idx_daxy = idx_daxy + dados2['turn']
        #             elif mostra == 2:
        #                 idx_daxy = idx_daxy + (dados2['pos'] % 51.8396)
        #             elif mostra == 3:
        #                 idx_daxy = idx_daxy + dados2['plane']
        #         else:
        #             print('{0:02d}-{1:5s}: ex nao carregou\n'.format(i,result[k]))
        #
        #     if ma:
        #         if _os.path.isfile(_os.path.sep.join([pathn,'dynap_ma_out.txt'])):
        #             pos, aceit, *_ = trackcpp_load_ma_data(pathn)
        #             if _np.isclose(aceit,0).any():
        #                 lt_prob += 1
        #             else:
        #                 accep += [aceit]
        #                 Accep = dict(s=pos,pos=_np.minimum(aceit[0], accepRF),
        #                              neg= _np.maximum(aceit[1], -accepRF))
        #                 # não estou usando alguns outputs
        #                 LT = lnls_tau_touschek_inverso(Accep,twispos,twi,**params)
        #                 ltime += [1/LT['ave_rate']/60/60] # em horas
        #         else:
        #             print('{0:02d}-{1:5s}: ma nao carregou\n'.format(i,result[k]))
        # if xy and (mostra == 0):
        #     idx_daxy = (n_pastas-idx_daxy)/n_pastas*100
        #     idx_daxy[0,0] = 100
        #     idx_daxy[0,1] = 0
        # if ex and (mostra == 0):
        #     idx_daex = (n_pastas-idx_daex)/n_pastas*100
        #     idx_daex[0,0] = 100
        #     idx_daex[0,1] = 0
        # if ma:
        #     accep   = _np.dstack(accep)*100
        #     ma_ave  = accep.mean(axis=2)
        #     ltime   = _np.hstack(ltime)
        #     lt_ave  = ltime.mean()
        #     ma_rms = accep.std(axis=2,ddof=1)
        #     lt_rms = ltime.std(ddof=1)
        #
        # # make the figures
        # if xy:
        #     fxy, axy = _plt.subplots()
        #     fxy.set_size_inches((5,4))
        #     axy.grid(True)
        #     axy.hold(True)
        #     axy.set_xlabel('x [mm]',fontsize=size_font)
        #     axy.set_ylabel('y [mm]',fontsize=size_font)
        #     axy.set_xlim([-limx, limx])
        #     axy.set_ylim([0, limy])
        #     pc = axy.pcolormesh(1000*dados1['x'], 1000*dados1['y'], idx_daxy)
        #     axy.annotate('y = 1 mm',(0.01,0.95),fontsize=size_font,color='w',xycoords='axes fraction')
        #     fxy.colorbar(pc, ticks=[0,20,40,60,80,100],ticklabels=['100%','80%','60%','40%','20%','0%'])
        # if ex:
        #     fex, aex = _plt.subplots()
        #     fex.set_size_inches((5,4))
        #     aex.grid(True)
        #     aex.hold(True)
        #     aex.set_xlabel(r'$\delta$ [%]',fontsize=size_font)
        #     aex.set_ylabel('x [mm]',fontsize=size_font)
        #     aex.set_xlim([-limne, limpe])
        #     aex.set_ylim([-limx, 0])
        #     pc = aex.pcolormesh(100*dados2.en, 1000*dados2.x, idx_daex)
        #     aex.annotate(r'$\delta$ = 0',(0.01,0.95),fontsize=size_font,color='w',xycoords='axes fraction')
        #     fex.colorbar(pc, ticks=[0,20,40,60,80,100],ticklabels=['100%','80%','60%','40%','20%','0%'])
        # if ma
        #     f2=figure('Position',[3, 3, 956, 462]);
        #     falt = axes('Parent',f2,'YGrid','on','XGrid','on','yTickLabel',{'-5','-2.5','0','2.5','5'},...
        #         'YTick',[-5 -2.5 0 2.5 5],'Units','pixels','Position',[77 64 864, 385],'FontSize',size_font);
        #     box(falt,'on'); hold(falt,'all');
        #     xlabel('pos [m]','FontSize',size_font);
        #     ylabel('\delta [%]','FontSize',size_font);
        #     plot(falt,spos,squeeze(accep(:,1,:))*100,'Color',[0.6 0.6 1.0]);
        #     plot(falt,spos,squeeze(accep(:,2,:))*100,'Color',[0.6 0.6 1.0]);
        #     plot(falt,spos,aveAccep,'LineWidth',3,'Color',[0,0,1]);
        #     if plot_LR, plot(falt,LT.Pos,limeLT/2*LossRate/max(LossRate(:)),'Color',[0,0,0]); end
        #     lnls_drawlattice(the_ring,10, 0, true,0.2);
        #     xlim([0, limsLT]); ylim([-limeLT-0.3, limeLT+0.3]);
        #
        #     string = {sprintf('%-10s = %3.1f GeV','Energy',params.E/1e9),...
        #         sprintf('%-10s = %5.3f mA','I/bunch',params.N*1.601e-19/1.72e-6*1e3),...
        #         sprintf('%-10s = %3.1f %%','Coupling',params.K*100),...
        #         sprintf('%-10s = %5.3f nm.rad','\epsilon_0',params.emit0*1e9),...
        #         sprintf('%-10s = %5.3f %%','\sigma_{\delta}',params.sigE*100),...
        #         sprintf('%-9s = %5.3f mm','\sigma_L',params.sigS*1e3),...
        #         sprintf('Tousc LT = %5.1f \xb1 %3.1f h',aveLT,stdLT)};
        #     annotation(f2,'textbox','Units','pixels','Position',[390, 162, 220, 90],'String',string(1:3),...
        #         'FontSize',size_font,'FitBoxToText','on','LineStyle','none','Color',[0 0 0]);
        #     annotation(f2,'textbox','Units','pixels','Position',[420, 267, 192, 91],'String',string(4:6),...
        #         'FontSize',size_font,'FitBoxToText','on','LineStyle','none','Color',[0 0 0]);
        #     annotation(f2,'textbox','Units','pixels','Position',[632, 202, 253, 37],'String',string(7),...
        #         'FontSize',size_font,'FitBoxToText','on','LineStyle','none','Color',[0 0 0]);
        # _plt.show()
        # return


    i=0
    while i < n_calls:
        ok, paths = directories_dialog('Selecione pasta com os dados?')
        if not ok: return

        paths = find_right_folders(paths)

        for path in paths:
            if i >= n_calls: break

            area, aper_xy, aper_ex, ltime, accep = [],[],[],[],[]

            result = sorted([ii for ii in _os.listdir(path) if _os.path.isdir(_os.path.sep.join([path,ii]))])
            n_pastas = len(result)
            rms_mode = True
            if n_pastas == 0:
                rms_mode = False
                n_pastas = 1

            na = _os.path.abspath(path).split('/')[1:]
            leg_text = input_dialog('Digite a legenda',na[-3],'Legenda')[1][0]

            lt_prob = 0
            for k in range(n_pastas):
                pathn = path
                if rms_mode: pathn += _os.path.sep + result[k]

                if xy:
                    if _os.path.isfile(_os.path.sep.join([pathn,'dynap_xy_out.txt'])):
                        aper, a, *_ = trackcpp_load_dynap_xy(pathn,var_plane)
                        area += [a]
                        aper_xy += [aper]
                    else:
                        print('{0:02d}-{1:5s}: xy nao carregou\n'.format(i,result[k]))
                if ex:
                    if _os.path.isfile(_os.path.sep.join([pathn,'dynap_ex_out.txt'])):
                        aper, *_ = trackcpp_load_dynap_ex(pathn)
                        aper_ex += [aper]
                    else:
                        print('{0:02d}-{1:5s}: ex nao carregou\n'.format(i,result[k]))

                if ma:
                    if _os.path.isfile(_os.path.sep.join([pathn,'dynap_ma_out.txt'])):
                        pos, aceit, *_ = trackcpp_load_ma_data(pathn)
                        if _np.isclose(aceit,0).any():
                            lt_prob += 1
                        else:
                            accep += [aceit]
                            Accep = dict(s=pos,pos=_np.minimum(aceit[0], accepRF),
                                         neg= _np.maximum(aceit[1], -accepRF))
                            # não estou usando alguns outputs
                            LT = lnls_tau_touschek_inverso(Accep,twispos,twi,**params)
                            ltime += [1/LT['ave_rate']/60/60] # em horas
                    else:
                        print('{0:02d}-{1:5s}: ma nao carregou\n'.format(i,result[k]))

            if xy:
                aper_xy = _np.dstack(aper_xy)*1000
                xy_ave  = aper_xy.mean(axis=2)
                neg_ave = xy_ave[0][2]
                area    = _np.hstack(area)*1e6
                area_ave= area.mean()
            if ex:
                aper_ex = _np.dstack(aper_ex)
                ex_ave  = aper_ex.mean(axis=2)
            if ma:
                accep   = _np.dstack(accep)*100
                ma_ave  = accep.mean(axis=2)
                ltime   = _np.hstack(ltime)
                lt_ave  = ltime.mean()
            if rms_mode:
                if xy:
                    xy_rms  = aper_xy.std(axis=2,ddof=1)
                    neg_rms = xy_rms[0][2]
                    area_rms= area.std(ddof=1)
                if ex:
                    ex_rms  = aper_ex.std(axis=2,ddof=1)
                if ma:
                    ma_rms = accep.std(axis=2,ddof=1)
                    lt_rms = ltime.std(ddof=1)

            ########  exposição dos resultados ######

            color = color_vec[i % len(color_vec)]
            ave_conf = dict(linewidth=esp_lin,color=color,linestyle='-')
            rms_conf = dict(linewidth=2,color=color,linestyle='--')
            if not i:
                if xy and ma:
                    print('\n{0:20s} {1:15s} {2:15s} {3:15s}\n'.format('Config',
                            'Dynap XY [mm^2]', 'Aper@y=0.2 [mm]', 'Lifetime [h]'))
                elif ma:
                    print('\n{0:20s} {1:15s}\n'.format('Config', 'Lifetime [h]'))
                elif xy:
                    print('\n{0:20s} {1:15s} {2:15s}\n'.format('Config',
                                        'Dynap XY [mm^2]','Aper@y=0.2 [mm]'))
            if xy or ma:
                print('{0:20s} '.format(leg_text.upper()), end='')

            if xy:
                if not i:
                    fxy, axy = _plt.subplots()
                    fxy.set_size_inches((5,4))
                    axy.grid(True)
                    axy.hold(True)
                    axy.set_xlabel('x [mm]',fontsize=size_font)
                    axy.set_ylabel('y [mm]',fontsize=size_font)
                    axy.set_xlim([-limx, limx])
                    axy.set_ylim([0, limy])
                axy.plot(xy_ave[0], xy_ave[1],label=leg_text,**ave_conf)
                if rms_mode:
                    print('{0:>5.2f} \xB1 {1:5.2f}   {2:>5.1f} \xB1 {3:5.1f}   '.format(
                            area_ave, area_rms, neg_ave, neg_rms),end='')
                    axy.plot(xy_ave[0]+xy_rms[0], xy_ave[1]+xy_rms[1],**rms_conf)
                    axy.plot(xy_ave[0]-xy_rms[0], xy_ave[1]-xy_rms[1],**rms_conf)
                else:
                    print('{0:>5.2f}           {1:>5.1f}           '.format(area_ave, neg_ave),end='')

            if ex:
                if not i:
                    fex, aex = _plt.subplots()
                    fex.set_size_inches((5,4))
                    aex.grid(True)
                    aex.hold(True)
                    aex.set_xlabel(r'$\delta$ [%]',fontsize=size_font)
                    aex.set_ylabel('x [mm]',fontsize=size_font)
                    aex.set_xlim([-limne, limpe])
                    aex.set_ylim([-limx, 0])
                aex.plot(100*ex_ave[0], 1000*ex_ave[1],label=leg_text,**ave_conf)
                if rms_mode:
                    aex.plot(100*(ex_ave[0]+ex_rms[0]),
                             1000*(ex_ave[1]+ex_rms[1]),**rms_conf)
                    aex.plot(100*(ex_ave[0]-ex_rms[0]),
                             1000*(ex_ave[1]-ex_rms[1]),**rms_conf)
            if ma:
                #imprime o tempo de vida
                if rms_mode:
                    print('{0:>5.2f} \xB1 {1:5.2f} '.format(lt_ave, lt_rms),end='')
                    if lt_prob:
                        print('   *{0:02d) máquinas desprezadas'.format(lt_prob)+
                              ' no cálculo por possuírem aceitancia nula.',end='')
                else:
                    print('{5.2f} ', lt_ave)
                if not i:
                    fma, ama = _plt.subplots()
                    fma.set_size_inches((7,3.5))
                    ama.grid(True)
                    ama.hold(True)
                    ama.set_xlabel('Pos [m]',fontsize=size_font)
                    ama.set_ylabel(r'$\delta$ [%]',fontsize=size_font)
                    ama.set_xlim([0, 52])
                    ama.set_ylim([-limne-0.2,limpe+0.2])
                    ama.set(yticklabels=['-5','-2.5','0','2.5','5'],
                            yticks=[-5,-2.5,0,2.5,5], position=[0.10,0.17,0.84,0.73])
                ama.plot(pos,ma_ave[0],label=leg_text,**ave_conf)
                ama.plot(pos,ma_ave[1],**ave_conf)
                if rms_mode:
                    ama.plot(pos,ma_ave[0]+ma_rms[0],**rms_conf)
                    ama.plot(pos,ma_ave[1]-ma_rms[1],**rms_conf)

            if xy or ma: print()

            i+=1


    title_text = input_dialog('Título',name='Digite um Título para os Gráficos')[1][0]

    if xy:
        axy.legend(loc='best')
        axy.set_title('DAXY - ' + title_text)
    if ex:
        aex.legend(loc='best')
        aex.set_title('DAEX - ' + title_text)
    if ma:
        ama.legend(loc='best')
        pyaccel.graphics.draw_lattice(acc,symmetry=10, offset=0, gca=True,height=0.4)
        ama.set_title('MA - ' + title_text)

    _plt.show()

if __name__ == '__main__':
    trackcpp_da_ma_lt(_os.path.abspath(_os.path.curdir))
