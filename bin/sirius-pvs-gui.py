#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.Qt import *
from functools import partial
import sirius as _sirius
from va.pvs import li as _pvs_li
from va.pvs import tb as _pvs_tb
from va.pvs import ts as _pvs_ts
from va.pvs import bo as _pvs_bo
from va.pvs import si as _pvs_si
from va.pvs import ti as _pvs_ti

qt_app = QApplication(sys.argv)

class RecordNameList(QWidget):

    def __init__(self, prefix):
        QWidget.__init__(self)
        self.prefix = prefix
        self.setWindowTitle('Record name list')
        self.setMinimumSize(500, 500)
        self.layout = QVBoxLayout()

        # LI
        self.create_one_button_system('LI', li_rec_name(), self.layout)

        # TB
        tb_di, tb_di_list = self.create_button_and_list('TBDI', tb_rec_name('tbdi'))
        tb_ps, tb_ps_list = self.create_button_and_list('TBPS', tb_rec_name('tbps'))
        tb_pu, tb_pu_list = self.create_button_and_list('TBPU', tb_rec_name('tbpu'))
        tb_ma, tb_ma_list = self.create_button_and_list('TBMA', tb_rec_name('tbma'))
        tb_pm, tb_pm_list = self.create_button_and_list('TBPM', tb_rec_name('tbpm'))
        tb_fk, tb_fk_list = self.create_button_and_list('TBFK', tb_fk_name())
        tb_dict = {tb_di:tb_di_list, tb_ps:tb_ps_list, tb_pu:tb_pu_list, tb_ma:tb_ma_list, tb_pm:tb_pm_list, tb_fk:tb_fk_list}
        self.create_system_button('TB', tb_dict, self.layout)
        self.create_button_group_and_add_to_layout(tb_dict, self.layout)

        # BO
        bo_di, bo_di_list = self.create_button_and_list('BODI', bo_rec_name('bodi'))
        bo_ps, bo_ps_list = self.create_button_and_list('BOPS', bo_rec_name('bops'))
        bo_pu, bo_pu_list = self.create_button_and_list('BOPA', bo_rec_name('bopa'))
        bo_ma, bo_ma_list = self.create_button_and_list('BOMA', bo_rec_name('boma'))
        bo_pm, bo_pm_list = self.create_button_and_list('BORF', bo_rec_name('borf'))
        bo_fk, bo_fk_list = self.create_button_and_list('BOFK', bo_fk_name())
        bo_dict = {bo_di:bo_di_list, bo_ps:bo_ps_list, bo_pu:bo_pu_list, bo_ma:bo_ma_list, bo_pm:bo_pm_list, bo_fk:bo_fk_list}
        self.create_system_button('BO', bo_dict, self.layout)
        self.create_button_group_and_add_to_layout(bo_dict, self.layout)

        # TS
        ts_di, ts_di_list = self.create_button_and_list('TSDI', ts_rec_name('tsdi'))
        ts_ps, ts_ps_list = self.create_button_and_list('TSPS', ts_rec_name('tsps'))
        ts_pu, ts_pu_list = self.create_button_and_list('TSPU', ts_rec_name('tspu'))
        ts_ma, ts_ma_list = self.create_button_and_list('TSMA', ts_rec_name('tsma'))
        ts_pm, ts_pm_list = self.create_button_and_list('TSPM', ts_rec_name('tspm'))
        ts_fk, ts_fk_list = self.create_button_and_list('TSFK', ts_fk_name())
        ts_dict = {ts_di:ts_di_list, ts_ps:ts_ps_list, ts_pu:ts_pu_list, ts_ma:ts_ma_list, ts_pm:ts_pm_list, ts_fk:ts_fk_list}
        self.create_system_button('TS', ts_dict, self.layout)
        self.create_button_group_and_add_to_layout(ts_dict, self.layout)

        # SI
        si_di, si_di_list = self.create_button_and_list('SIDI', si_rec_name('sidi'))
        si_ps, si_ps_list = self.create_button_and_list('SIPS', si_rec_name('sips'))
        si_pu, si_pu_list = self.create_button_and_list('SIPA', si_rec_name('sipa'))
        si_ma, si_ma_list = self.create_button_and_list('SIMA', si_rec_name('sima'))
        si_pm, si_pm_list = self.create_button_and_list('SIRF', si_rec_name('sirf'))
        si_fk, si_fk_list = self.create_button_and_list('SIFK', si_fk_name())
        si_dict = {si_di:si_di_list, si_ps:si_ps_list, si_pu:si_pu_list, si_ma:si_ma_list, si_pm:si_pm_list, si_fk:si_fk_list}
        self.create_system_button('SI', si_dict, self.layout)
        self.create_button_group_and_add_to_layout(si_dict, self.layout)

        # TI
        self.create_one_button_system('TI', ti_rec_name('ti'), self.layout)

        self.setLayout(self.layout)

    @pyqtSlot(bool)
    def system_button_clicked(self, bool, system_dict):
        if bool:
            for button in system_dict.keys():
                button.show()
        else:
            for button in system_dict.keys():
                button.hide()
            for list in system_dict.values():
                list.hide()

    @pyqtSlot(bool)
    def element_button_clicked(self, bool, list, system_dict):
        if bool:
            for lt in system_dict.values():
                lt.hide()
            list.show()
        else:
            list.hide()

    @pyqtSlot(bool)
    def system_one_button_clicked(self, bool, list):
        if bool:
            list.show()
        else:
            list.hide()

    def create_button_group_and_add_to_layout(self, system_dict, vlayout):
        group = QButtonGroup()
        hlayout = QHBoxLayout()
        for button in system_dict.keys():
            group.addButton(button)
            hlayout.addWidget(button)
            button.hide()
            list = system_dict[button]
            button.clicked.connect(partial(self.element_button_clicked, list=list, system_dict = system_dict))
        vlayout.addLayout(hlayout)
        for list in system_dict.values():
            vlayout.addWidget(list)
            list.hide()

    def create_button_and_list(self, label, names):
        button = QPushButton(label)
        button.setCheckable(True)
        button.setAutoExclusive(True)
        list = QListWidget()
        list.setMaximumHeight(200)
        for name in names:
            list.addItem(self.prefix + name)
        return button, list

    def create_system_button(self, label, system_dict, layout):
        button = QPushButton(label)
        button.setCheckable(True)
        button.clicked.connect(partial(self.system_button_clicked, system_dict=system_dict))
        layout.addWidget(button)

    def create_one_button_system(self, label, names, layout):
        button = QPushButton(label)
        button.setCheckable(True)
        list = QListWidget()
        list.setMaximumHeight(200)
        for name in names:
            list.addItem(self.prefix + name)
        button.clicked.connect(partial(self.system_one_button_clicked, list=list))
        layout.addWidget(button)
        layout.addWidget(list)
        list.hide()

    def run(self):
        self.show()
        qt_app.exec_()


# LI
li_rec_name = _sirius.li.record_names.get_record_names
li_fk_name  = _pvs_li._get_fake_record_names
# TB
tb_rec_name = _sirius.tb.record_names.get_record_names
tb_fk_name  = _pvs_tb._get_fake_record_names
# BO
bo_rec_name = _sirius.bo.record_names.get_record_names
bo_fk_name  = _pvs_bo._get_fake_record_names
# TS
ts_rec_name = _sirius.ts.record_names.get_record_names
ts_fk_name  = _pvs_ts._get_fake_record_names
# SI
si_rec_name = _sirius.si.record_names.get_record_names
si_fk_name  = _pvs_si._get_fake_record_names
# TI
ti_rec_name = _sirius.ti.record_names.get_record_names
ti_fk_name  = _pvs_ti._get_fake_record_names


if len(sys.argv) > 1:
    prefix = sys.argv[1]
else:
    prefix = "VA-"

app = RecordNameList(prefix)
app.run()
