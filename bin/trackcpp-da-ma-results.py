#!/usr/bin/env python-sirius
"""Plot trackcpp tracking results."""

# import warnings
# warnings.filterwarnings('ignore')
import os as _os
import numpy as _np
import optparse as _optparse
import matplotlib.pyplot as _plt

import pymodels
import pyaccel
import mathphys as _mp
import lnls.dialog as _dialog

from apsuite.trackcpp_utils import load_dynap_ma, load_dynap_xy, load_dynap_ex

_input_dialog = _dialog.input_dialog
_directories_dialog = _dialog.directories_dialog
_radio_dialog = _dialog.radio_dialog

# parâmetros para a geração das figuras
color_vec = ['b', 'r', 'g', 'm', 'c', 'k', 'y']
esp_lin, size_font = 5, 24
limx, limy, limpe, limne = 12, 3.5, 6, 6
var_plane = 'x'  # determinaçao da abertura dinâmica por varreduda no plano x
# size_font = 16
type_colormap = 'Jet'
mostra = 0
# 0 = porcentagem de part perdidas
# 1 = número medio de voltas
# 2 = posicao em que foram perdidas
# 3 = plano em que foram perdidas
plot_loss_rate = True


CURDIR = _os.path.abspath(_os.path.curdir)


def _full(x):
    return _os.path.sep.join(x)


def find_right_folders(paths):
    """."""
    pathnames = []
    for path in paths:
        listing = _os.listdir(path)
        if any([i.startswith('rms') for i in listing]):
            pathnames += [path]
            continue
        paths2 = []
        for file in listing:
            if file.startswith(('dynap_xy_out.txt',
                                'dynap_ex_out.txt',
                                'dynap_ma_out.txt')):
                pathnames += [path]
            else:
                file = _full((path, file))
                if _os.path.isdir(file) and not file.startswith(('.', '..')):
                    paths2 += [file]
        if paths2:
            pathnames += find_right_folders(paths2)
    return sorted(pathnames)


def ma_analysis(paths, leg_text, title_text, mach, energy, mode):
    """."""
    if mach.find('bo') >= 0:
        acc = getattr(pymodels, 'bo')
        acc = acc.create_accelerator()
        acc.energy = energy
        pymodels.bo.lattice.set_rf_voltage(acc._accelerator.lattice, energy)
        if energy == 0.15 * 1e9:
            # BOOSTER (equillibirum parameters from LINAC)
            emit0 = 170e-9  # linac
            sigE = 5.0e-3  # linac
            sigS = 11.2e-3  # linac
            accepRF = 0.033
            K = 0.0002
            Ic = 0.6
            nrBun = 1
        else:
            eqpar = pyaccel.optics.get_equilibrium_parameters(acc)
            emit0 = eqpar[0]['natural_emittance']
            sigE = eqpar[0]['natural_energy_spread']
            sigS = eqpar[0]['bunch_length']
            K = 0.0002
            Ic = 0.6
            nrBun = 1
            accepRF = eqpar[0]['rf_energy_acceptance']
    else:
        acc = getattr(pymodels, 'si')
        acc = acc.create_accelerator(optics_mode=mode)
        acc.energy = energy

        eqpar = pyaccel.optics.get_equilibrium_parameters(acc)
        # Data given by Natalia
        emit0 = 0.250e-9  # eqpar['natural_emittance']
        sigE = 9.4e-4   # eqpar['natural_energy_spread']
        sigS = 3.0e-3   # 3.5e-3 # takes IBS into account
        # sigS  = eqpar['bunch_length']
        K = 0.01
        Ic = 100
        nrBun = 864
        accepRF = eqpar[0]['rf_energy_acceptance']

    # users selects beam lifetime parameters
    prompt = [
        'Emitance[nm.rad]', 'Energy spread', 'Bunch length (with IBS) [mm]',
        'Coupling [%]', 'Current [mA]', 'Nr bunches',
        'RF Energy Acceptance [%]']
    defaultanswer = [
        str(emit0/1e-9), str(sigE), str(sigS*1000), str(100*K),
        str(Ic), str(nrBun), str(accepRF*100)]
    ok, answer = _input_dialog(prompt, defaultanswer, 'Lifetime Parameters')
    if not ok:
        return
    emit0 = float(answer[0])*1e-9
    sigE = float(answer[1])
    sigS = float(answer[2])/1000
    K = float(answer[3])/100
    Ic = float(answer[4])/1000
    nrBun = int(answer[5])
    accepRF = float(answer[6])/100
    N = Ic / nrBun / \
        _mp.constants.elementary_charge*(acc.length/_mp.constants.light_speed)
    params = dict(natural_emittance=emit0,
                  energy_spread=sigE, bunch_length=sigS, coupling=K,
                  n=N, energy=energy/1e9)
    twi, *_ = pyaccel.optics.calc_twiss(acc, indices='open')

    ma_text = ''
    fma, ama = _plt.subplots(figsize=(11, 6))
    ama.grid(True)
    ama.set_xlabel('Pos [m]', fontsize=size_font)
    ama.set_ylabel(r'$\delta$ [%]', fontsize=size_font)
    ama.set(yticklabels=['-5', '-2.5', '0', '2.5', '5'],
            yticks=[-5, -2.5, 0, 2.5, 5], position=[0.10, 0.17, 0.84, 0.73])
    ama.set_title('MA - ' + title_text)
    pyaccel.graphics.draw_lattice(acc, symmetry=5, offset=0,
                                  gca=True, height=0.4)
    ama.set_xlim([0, 104])
    ama.set_ylim([-limne-0.2, limpe+0.2])
    if len(paths) == 1:
        path = paths[0]
        ltime, accep, rate = [], [], []
        result = sorted([ii for ii in _os.listdir(path) if
                        _os.path.isdir(_full([path, ii]))])
        n_pastas = len(result)

        for k in range(n_pastas):
            pathn = _full([path, result[k]])
            if _os.path.isfile(_full([pathn, 'dynap_ma_out.txt'])):
                pos, aceit, *_ = load_dynap_ma(pathn)
                accep += [aceit]
                Accep = dict(s=pos, pos=_np.minimum(aceit[0], accepRF),
                             neg=_np.maximum(aceit[1], -accepRF))
                # não estou usando alguns outputs
                LT = _mp.beam_lifetime.calc_touschek_loss_rate(
                    Accep, twi, **params)
                rate += [LT['rate']]
                ltime += [1/LT['ave_rate']/60/60]  # em horas
            else:
                text = '{0:5s}: ma nao carregou\n'.format(result[k])
                print(text, end='')
                ma_text += text
        accep = _np.dstack(accep)*100
        rate = _np.vstack(rate)
        ma_ave = accep.mean(axis=2)
        ltime = _np.hstack(ltime)
        lt_ave = ltime.mean()
        lt_rms = ltime.std(ddof=1)

        # make the figures
        ama.plot(pos, accep[0], color=[0.6, 0.6, 1.0])
        ama.plot(pos, accep[1], color=[0.6, 0.6, 1.0])
        ama.plot(pos, ma_ave.T, linewidth=esp_lin, color=[0, 0, 1])
        if plot_loss_rate:
            ama.plot(LT['pos'], limne/2*rate.T/rate.max(), color='k')
        stri = ('${0:3s}$ = {1:3.1f} GeV\n'.format('E', energy/1e9) +
                '${0:3s}$ = {1:5.3f} mA\n'.format('I_b', Ic/nrBun*1e3) +
                '${0:3s}$ = {1:3.1f} %'.format('K', K*100))
        ama.annotate(stri, (0.1, 0.3),
                     fontsize=12, color='k', xycoords='axes fraction')
        stri = (
            '${0:3s}$ = {1:5.3f} nm.rad\n'.format('\epsilon_0', emit0*1e9) +
            '${0:3s}$ = {1:5.3f} % \n'.format('\sigma_{\delta}', sigE*100) +
            '${0:3s}$ = {1:5.3f} mm'.format('\sigma_L', sigS*1e3))
        ama.annotate(
            stri, (0.4, 0.3), fontsize=12, color='k', xycoords='axes fraction')

        stri = 'Tousc LT = {0:5.1f} \xb1 {1:3.1f} h'.format(lt_ave, lt_rms)
        ama.annotate(
            stri, (0.67, 0.35), fontsize=12, color='k',
            xycoords='axes fraction')
        return fma, ma_text

    text = '\n{0:^20s} {1:15s}\n'.format('Configuration', 'Lifetime [h]')
    print(text, end='')
    ma_text += text
    for i, path in enumerate(paths):
        ltime, accep = [], []

        result = sorted([ii for ii in _os.listdir(path) if
                         _os.path.isdir(_full([path, ii]))])
        n_pastas = len(result)
        rms_mode = True
        if n_pastas == 0:
            rms_mode = False
            n_pastas = 1

        lt_prob = 0
        for k in range(n_pastas):
            pathn = path
            if rms_mode:
                pathn += _os.path.sep + result[k]
            if _os.path.isfile(_full([pathn, 'dynap_ma_out.txt'])):
                pos, aceit, *_ = load_dynap_ma(pathn)
                if _np.isclose(aceit, 0).any():
                    lt_prob += 1
                else:
                    accep += [aceit]
                    Accep = dict(s=pos, pos=_np.minimum(aceit[0], accepRF),
                                 neg=_np.maximum(aceit[1], -accepRF))
                    # não estou usando alguns outputs
                    LT = _mp.beam_lifetime.calc_touschek_loss_rate(
                        Accep, twi, **params)
                    ltime += [1/LT['ave_rate']/60/60]  # em horas
            else:
                text = '{0:02d}-{1:5s}: ma nao carregou\n'.format(i, result[k])
                print(text, end='')
                ma_text += text
        accep = _np.dstack(accep)*100
        ma_ave = accep.mean(axis=2)
        ltime = _np.hstack(ltime)
        lt_ave = ltime.mean()
        if rms_mode:
            ma_rms = accep.std(axis=2, ddof=1)
            lt_rms = ltime.std(ddof=1)
        #  exposição dos resultados ######
        color = color_vec[i % len(color_vec)]
        ave_conf = dict(linewidth=esp_lin, color=color, linestyle='-')
        rms_conf = dict(linewidth=2, color=color, linestyle='--')
        # imprime o tempo de vida
        text = '{0:20s} '.format(leg_text[i].upper()[:20])
        print(text, end='')
        ma_text += text
        if rms_mode:
            text = '{0:>6.3f} \xB1 {1:6.3f} \n'.format(lt_ave, lt_rms)
            print(text, end='')
            ma_text += text
            if lt_prob:
                text = ('   *{0:02d} máquinas desprezadas'.format(lt_prob) +
                        ' no cálculo por possuírem aceitancia nula.\n')
                print(text, end='')
                ma_text += text
        else:
            text = '{0:6.3f} \n'.format(lt_ave)
            print(text, end='')
            ma_text += text
        ama.plot(pos, ma_ave[0], label=leg_text[i], **ave_conf)
        ama.plot(pos, ma_ave[1], **ave_conf)
        if rms_mode:
            ama.plot(pos, ma_ave[0]+ma_rms[0], **rms_conf)
            ama.plot(pos, ma_ave[0]-ma_rms[0], **rms_conf)
            ama.plot(pos, ma_ave[1]+ma_rms[1], **rms_conf)
            ama.plot(pos, ma_ave[1]-ma_rms[1], **rms_conf)
    ama.legend(loc='best')
    return fma, ma_text


def xy_analysis(paths, leg_text, title_text):
    """."""
    xy_text = ''
    fxy, axy = _plt.subplots(figsize=(9, 6))
    axy.grid(True)
    axy.set_xlabel('x [mm]', fontsize=size_font)
    axy.set_ylabel('y [mm]', fontsize=size_font)
    axy.set_title('DAXY - ' + title_text)
    axy.set_xlim([-limx, limx])
    axy.set_ylim([0, limy])

    if len(paths) == 1:
        path = paths[0]

        result = sorted([ii for ii in _os.listdir(path) if
                         _os.path.isdir(_full([path, ii]))])
        n_pastas = len(result)

        idx_daxy = None
        for k in range(n_pastas):
            pathn = _full([path, result[k]])
            if _os.path.isfile(_full([pathn, 'dynap_xy_out.txt'])):
                _, a, dados = load_dynap_xy(pathn, var_plane)
                if idx_daxy is None:
                    idx_daxy = dados['plane']*0.0
                if mostra == 0:
                    idx_daxy += (dados['plane'] == 0)
                elif mostra == 1:
                    idx_daxy += dados['turn']
                elif mostra == 2:
                    idx_daxy += (dados['pos'] % 51.8396)
                elif mostra == 3:
                    idx_daxy += dados['plane']
            else:
                text = '{0:5s}: xy nao carregou\n'.format(result[k])
                print(text, end='')
                xy_text += text
        if mostra == 0:
            idx_daxy = (n_pastas-idx_daxy)/n_pastas*100
            idx_daxy[0, 0] = 100
            idx_daxy[0, 1] = 0
        # make the figures
        pc = axy.pcolormesh(1000*dados['x'], 1000*dados['y'], idx_daxy)
        axy.annotate('y = 1 mm', (0.01, 0.90), fontsize=size_font, color='w',
                     xycoords='axes fraction')
        axy.set_xlim([dados['x'].min()*1000, dados['x'].max()*1000])
        axy.set_ylim([dados['y'].min()*1000, dados['y'].max()*1000])
        ax = fxy.add_axes([0.91, 0.10, 0.03, 0.83])
        cl = fxy.colorbar(pc, cax=ax, ticks=[0, 20, 40, 60, 80, 100])
        cl.set_ticklabels(['100%', '80%', '60%', '40%', '20%', '0%'])
        axy.set_position([0.08, 0.10, 0.82, 0.83])
        return fxy, xy_text

    text = '\n{0:^20s} {1:15s} {2:15s}\n'.format(
        'Configuration', 'Dynap XY [mm^2]', 'Aper@y=0.2 [mm]')
    print(text, end='')
    xy_text += text
    for i, path in enumerate(paths):
        area, aper_xy = [], []
        result = sorted([ii for ii in _os.listdir(path) if
                         _os.path.isdir(_full([path, ii]))])
        n_pastas = len(result)
        rms_mode = True
        if n_pastas == 0:
            rms_mode = False
            n_pastas = 1
        for k in range(n_pastas):
            pathn = path
            if rms_mode:
                pathn += _os.path.sep + result[k]
            if _os.path.isfile(_full([pathn, 'dynap_xy_out.txt'])):
                aper, a, *_ = load_dynap_xy(pathn, var_plane)
                area += [a]
                aper_xy += [aper]
            else:
                text = '{0:02d}-{1:5s}: xy nao carregou\n'.format(i, result[k])
                print(text, end='')
                xy_text += text
        aper_xy = _np.dstack(aper_xy)*1000
        xy_ave = aper_xy.mean(axis=2)
        neg_ave = xy_ave[0][2]
        area = _np.hstack(area)*1e6
        area_ave = area.mean()
        if rms_mode:
            xy_rms = aper_xy.std(axis=2, ddof=1)
            neg_rms = xy_rms[0][2]
            area_rms = area.std(ddof=1)

        # exposição dos resultados ######
        color = color_vec[i % len(color_vec)]
        ave_conf = dict(linewidth=esp_lin, color=color, linestyle='-')
        rms_conf = dict(linewidth=2, color=color, linestyle='--')

        text = '{0:20s} '.format(leg_text[i].upper()[:20])
        print(text, end='')
        xy_text += text

        axy.plot(xy_ave[0], xy_ave[1], label=leg_text[i], **ave_conf)
        if rms_mode:
            sfmt = '{0:>6.3f} \xB1 {1:6.3f}   {2:>6.3f} \xB1 {3:6.3f}   \n'
            text = sfmt.format(
                    area_ave, area_rms, neg_ave, neg_rms)
            print(text, end='')
            xy_text += text
            axy.plot(xy_ave[0]+xy_rms[0], xy_ave[1]+xy_rms[1], **rms_conf)
            axy.plot(xy_ave[0]-xy_rms[0], xy_ave[1]-xy_rms[1], **rms_conf)
        else:
            sfmt = '{0:>6.3f}           {1:>5.1f}           \n'
            text = sfmt.format(area_ave, neg_ave)
            print(text, end='')
            xy_text += text
    axy.legend(loc='best')
    return fxy, xy_text


def ex_analysis(paths, leg_text, title_text):
    """."""
    ex_text = ''
    fex, aex = _plt.subplots(figsize=(9, 6))
    aex.grid(True)
    aex.set_xlabel(r'$\delta$ [%]', fontsize=size_font)
    aex.set_ylabel('x [mm]', fontsize=size_font)
    aex.set_xlim([-limne, limpe])
    aex.set_ylim([-limx, 0])
    aex.set_title('DAEX - ' + title_text)
    if len(paths) == 1:
        path = paths[0]
        aper_ex = []

        result = sorted([ii for ii in _os.listdir(path) if
                         _os.path.isdir(_full([path, ii]))])
        n_pastas = len(result)

        idx_daex = None
        for k in range(n_pastas):
            pathn = _full([path, result[k]])
            if _os.path.isfile(_full([pathn, 'dynap_ex_out.txt'])):
                _, dados = load_dynap_ex(pathn)
                if idx_daex is None:
                    idx_daex = dados['plane']*0.0
                if mostra == 0:
                    idx_daex += (dados['plane'] == 0)
                elif mostra == 1:
                    idx_daex += dados['turn']
                elif mostra == 2:
                    idx_daex += (dados['pos'] % 51.8396)
                elif mostra == 3:
                    idx_daex += dados['plane']
            else:
                text = '{0:5s}: ex nao carregou\n'.format(result[k])
                print(text, end='')
                ex_text += text
        if mostra == 0:
            idx_daex = (n_pastas-idx_daex)/n_pastas*100
            idx_daex[0, 0] = 100
            idx_daex[0, 1] = 0
        pc = aex.pcolormesh(100*dados['en'], 1000*dados['x'], idx_daex)
        aex.annotate(r'$\delta$ = 0', (0.01, 0.05), fontsize=size_font,
                     color='w', xycoords='axes fraction')
        aex.set_xlim([dados['en'].min()*100, dados['en'].max()*100])
        aex.set_ylim([dados['x'].min()*1000, dados['x'].max()*1000])
        ax = fex.add_axes([0.91, 0.10, 0.03, 0.83])
        cl = fex.colorbar(pc, cax=ax, ticks=[0, 20, 40, 60, 80, 100])
        cl.set_ticklabels(['100%', '80%', '60%', '40%', '20%', '0%'])
        aex.set_position([0.08, 0.10, 0.82, 0.83])
        return fex, ex_text

    for i, path in enumerate(paths):
        aper_ex = []

        result = sorted([ii for ii in _os.listdir(path) if
                         _os.path.isdir(_full([path, ii]))])
        n_pastas = len(result)
        rms_mode = True
        if n_pastas == 0:
            rms_mode = False
            n_pastas = 1
        for k in range(n_pastas):
            pathn = path
            if rms_mode:
                pathn += _os.path.sep + result[k]
            if _os.path.isfile(_full([pathn, 'dynap_ex_out.txt'])):
                aper, *_ = load_dynap_ex(pathn)
                aper_ex += [aper]
            else:
                text = '{0:02d}-{1:5s}: ex nao carregou\n'.format(i, result[k])
                print(text, end='')
                ex_text += text
        aper_ex = _np.dstack(aper_ex)
        ex_ave = aper_ex.mean(axis=2)
        if rms_mode:
            ex_rms = aper_ex.std(axis=2, ddof=1)

        # exposição dos resultados ######
        color = color_vec[i % len(color_vec)]
        ave_conf = dict(linewidth=esp_lin, color=color, linestyle='-')
        rms_conf = dict(linewidth=2, color=color, linestyle='--')

        aex.plot(100*ex_ave[0], 1000*ex_ave[1], label=leg_text[i], **ave_conf)
        if rms_mode:
            aex.plot(100*(ex_ave[0]+ex_rms[0]),
                     1000*(ex_ave[1]+ex_rms[1]), **rms_conf)
            aex.plot(100*(ex_ave[0]-ex_rms[0]),
                     1000*(ex_ave[1]-ex_rms[1]), **rms_conf)
    aex.legend(loc='best')
    return fex, ex_text


def trackcpp_da_ma_lt(path=None, save=False, show=True):
    """."""
    # user selects submachine
    ok, answer = _radio_dialog(['si', 'bo'], name='Accelerator')
    if not ok:
        return
    submachine = answer
    # submachine = 'si'

    if submachine == 'si':
        defaultanswer = ['3.0', 'S05.01', '2', 'ma xy ex']
    elif submachine == 'bo':
        defaultanswer = ['0.150', 'M01', '2', 'ma xy ex']
    else:
        raise Exception('Invalid submachine name')

    user selects main parameters
    prompt = ['energy [GeV]', 'Optics Mode', 'Number of plots',
              'Types of plots']
    ok, answer = _input_dialog(prompt, defaultanswer, 'Main Parameters')
    if not ok:
        return
    answer = ['3.0', 'S05.01', '2', 'ma xy ex']

    energy = float(answer[0]) * 1e9
    mode = answer[1]
    n_calls = round(float(answer[2]))

    xy = True if answer[3].find('xy') >= 0 else False
    ex = True if answer[3].find('ex') >= 0 else False
    ma = True if answer[3].find('ma') >= 0 else False

    if path is None:
        path = _full(['', 'home', 'fac_files', 'data', 'pymodels',
                      submachine, 'beam_dynamics'])
    i = 0
    leg_text = []
    folders = []
    while i < n_calls:
        ok, paths = _directories_dialog(path, 'Selecione pastas com dados')
        if not ok:
            return
        paths = find_right_folders(paths)
        for path in paths:
            if i >= n_calls:
                break
            folders += [path]
            na = _os.path.abspath(path).split('/')[1:]
            leg_text += _input_dialog('Digite a legenda', na[-3], 'Legenda')[1]
            i += 1
    title_text = _input_dialog('Título',
                               name='Digite um Título para os Gráficos')[1][0]
    text = ''
    if xy:
        fxy, xy_text = xy_analysis(folders, leg_text, title_text)
        text += xy_text
        if save:
            fxy.savefig(_full((CURDIR, 'XY-'+title_text + '.svg')))
    if ex:
        fex, ex_text = ex_analysis(folders, leg_text, title_text)
        text += ex_text
        if save:
            fex.savefig(_full((CURDIR, 'EX-'+title_text + '.svg')))
    if ma:
        fma, ma_text = ma_analysis(folders, leg_text, title_text,
                                   submachine, energy, mode)
        text += ma_text
        if save:
            fma.savefig(_full((CURDIR, 'MA-'+title_text + '.svg')))
    if save:
        with open(_full((CURDIR, 'SUMMARY-'+title_text + '.txt')), 'w') as fh:
            fh.write(text)
    if show:
        _plt.show()


if __name__ == '__main__':

    if 'beam_dynamics' not in CURDIR:
        CURDIR = None

    # configuration of the parser for the arguments
    parser = _optparse.OptionParser()
    parser.add_option('-p', '--path', dest='path', type='str',
                      help="Path to be used as initial guess.", default=CURDIR)
    parser.add_option('-s', '--save', dest='save', action='store_true',
                      help="Save the figures generated in the current folder.",
                      default=False)
    (opts, _) = parser.parse_args()

    trackcpp_da_ma_lt(path=opts.path, save=opts.save)
