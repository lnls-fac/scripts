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

qt_app = QApplication(sys.argv)

class RecordNameList(QWidget):

    def __init__(self, prefix):
        QWidget.__init__(self)
        self.prefix = prefix
        self.setWindowTitle('Record name list')
        self.setMinimumSize(500, 500)
        self.layout = QVBoxLayout()

        # LI
        li_rn = li_rec_name(li_fd)
        li_rn.update(li_fk_name(li_fd))
        self.create_one_button_system('LI', li_rn , self.layout)

        # TB
        tb_di, tb_di_list = self.create_button_and_list('TBDI', tb_rec_name(tb_fd,'tbdi'))
        tb_ps, tb_ps_list = self.create_button_and_list('TBPS', tb_rec_name(tb_fd,'tbps'))
        tb_pu, tb_pu_list = self.create_button_and_list('TBPU', tb_rec_name(tb_fd,'tbpu'))
        tb_ma, tb_ma_list = self.create_button_and_list('TBMA', tb_rec_name(tb_fd,'tbma'))
        tb_pm, tb_pm_list = self.create_button_and_list('TBPM', tb_rec_name(tb_fd,'tbpm'))
        tb_ti, tb_ti_list = self.create_button_and_list('TBTI', tb_rec_name(tb_fd,'tbti'))
        tb_fk, tb_fk_list = self.create_button_and_list('TBFK', tb_fk_name(tb_fd))
        tb_dict = {tb_di:tb_di_list, tb_ps:tb_ps_list, tb_pu:tb_pu_list, tb_ma:tb_ma_list, tb_pm:tb_pm_list, tb_fk:tb_fk_list, tb_ti:tb_ti_list}
        self.create_system_button('TB', tb_dict, self.layout)
        self.create_button_group_and_add_to_layout(tb_dict, self.layout)

        # BO
        bo_di, bo_di_list = self.create_button_and_list('BODI', bo_rec_name(bo_fd,'bodi'))
        bo_ps, bo_ps_list = self.create_button_and_list('BOPS', bo_rec_name(bo_fd,'bops'))
        bo_pu, bo_pu_list = self.create_button_and_list('BOPA', bo_rec_name(bo_fd,'bopa'))
        bo_ma, bo_ma_list = self.create_button_and_list('BOMA', bo_rec_name(bo_fd,'boma'))
        bo_pm, bo_pm_list = self.create_button_and_list('BORF', bo_rec_name(bo_fd,'borf'))
        bo_ti, bo_ti_list = self.create_button_and_list('BOTI', bo_rec_name(bo_fd,'boti'))
        bo_fk, bo_fk_list = self.create_button_and_list('BOFK', bo_fk_name(bo_fd))
        bo_dict = {bo_di:bo_di_list, bo_ps:bo_ps_list, bo_pu:bo_pu_list, bo_ma:bo_ma_list, bo_pm:bo_pm_list, bo_fk:bo_fk_list, bo_ti:bo_ti_list}
        self.create_system_button('BO', bo_dict, self.layout)
        self.create_button_group_and_add_to_layout(bo_dict, self.layout)

        # TS
        ts_di, ts_di_list = self.create_button_and_list('TSDI', ts_rec_name(ts_fd,'tsdi'))
        ts_ps, ts_ps_list = self.create_button_and_list('TSPS', ts_rec_name(ts_fd,'tsps'))
        ts_pu, ts_pu_list = self.create_button_and_list('TSPU', ts_rec_name(ts_fd,'tspu'))
        ts_ma, ts_ma_list = self.create_button_and_list('TSMA', ts_rec_name(ts_fd,'tsma'))
        ts_pm, ts_pm_list = self.create_button_and_list('TSPM', ts_rec_name(ts_fd,'tspm'))
        ts_ti, ts_ti_list = self.create_button_and_list('TSTI', ts_rec_name(ts_fd,'tsti'))
        ts_fk, ts_fk_list = self.create_button_and_list('TSFK', ts_fk_name(ts_fd))
        ts_dict = {ts_di:ts_di_list, ts_ps:ts_ps_list, ts_pu:ts_pu_list, ts_ma:ts_ma_list, ts_pm:ts_pm_list, ts_fk:ts_fk_list, ts_ti:ts_ti_list}
        self.create_system_button('TS', ts_dict, self.layout)
        self.create_button_group_and_add_to_layout(ts_dict, self.layout)

        # SI
        si_di, si_di_list = self.create_button_and_list('SIDI', si_rec_name(si_fd,'sidi'))
        si_ps, si_ps_list = self.create_button_and_list('SIPS', si_rec_name(si_fd,'sips'))
        si_pu, si_pu_list = self.create_button_and_list('SIPA', si_rec_name(si_fd,'sipa'))
        si_ma, si_ma_list = self.create_button_and_list('SIMA', si_rec_name(si_fd,'sima'))
        si_pm, si_pm_list = self.create_button_and_list('SIRF', si_rec_name(si_fd,'sirf'))
        si_ti, si_ti_list = self.create_button_and_list('SITI', si_rec_name(si_fd,'siti'))
        si_fk, si_fk_list = self.create_button_and_list('SIFK', si_fk_name(si_fd))
        si_dict = {si_di:si_di_list, si_ps:si_ps_list, si_pu:si_pu_list, si_ma:si_ma_list, si_pm:si_pm_list, si_fk:si_fk_list, si_ti:si_ti_list}
        self.create_system_button('SI', si_dict, self.layout)
        self.create_button_group_and_add_to_layout(si_dict, self.layout)

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
li = _sirius.li.create_accelerator()
li_fd = _sirius.li.families.get_family_data(li)
li_rec_name = _sirius.li.record_names.get_record_names
li_fk_name = _pvs_li.get_fake_record_names
# TB
tb = _sirius.tb.create_accelerator()
tb_fd = _sirius.tb.families.get_family_data(tb)
tb_rec_name = _sirius.tb.record_names.get_record_names
tb_fk_name  = _pvs_tb.get_fake_record_names
# BO
bo = _sirius.bo.create_accelerator()
bo_fd = _sirius.bo.families.get_family_data(bo)
bo_rec_name = _sirius.bo.record_names.get_record_names
bo_fk_name  = _pvs_bo.get_fake_record_names
# TS
ts = _sirius.ts.create_accelerator()
ts_fd = _sirius.ts.families.get_family_data(ts)
ts_rec_name = _sirius.ts.record_names.get_record_names
ts_fk_name  = _pvs_ts.get_fake_record_names
# SI
si = _sirius.si.create_accelerator()
si_fd = _sirius.si.families.get_family_data(si)
si_rec_name = _sirius.si.record_names.get_record_names
si_fk_name  = _pvs_si.get_fake_record_names


if len(sys.argv) > 1:
    prefix = sys.argv[1]
else:
    prefix = "VA-"

app = RecordNameList(prefix)
app.run()
