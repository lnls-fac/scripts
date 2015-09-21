#!/usr/bin/env python3

import sys

def usage():
    print('\nUsage: elegant2AT.py fileName1 fileName2 ... fileNameN\n')


def elegant2AT(filename):
    # primeiro eu uniformizo o arquivo de input
    with open(filename) as fin:
        filein = fin.read()
    filein = filein.lower().replace(' ','').replace('&\n','')
    
    filename = filename.replace('-','_')
    
    #Agora crio o arquivo de saida
    with open(''.join(filename.rpartition('.')[0:2]) + 'm',
                    'w+',encoding='utf8',newline='\n') as fout:
        
        fout.write('% {0}\n'.format(filename))
        fout.write('%% {0}\n'.format('QUADRUPOLES'))
        fout.write('%% {0}\n\n'.format(15*'='))
        for i in filein.splitlines(False):
            # vejo se é um quadrupolo
            if i.find('kquad') != -1:
                quad       = i.split(':')[0].strip('"') + '_strength'
                quad_stren = float(i.split(':')[1].split('k1=')[1].split(',')[0])
                fout.write('{0:16} = {1:> 08.6f};\n'.format(quad,quad_stren))

        fout.write('\n\n%% {0}\n'.format('Sextupoles'))
        fout.write('%% {0}\n\n'.format(15*'='))
        for i in filein.splitlines(False):
            # vejo se é um quadrupolo
            if i.find('ksext') != -1:
                sext       = i.split(':')[0].strip('"').strip('m') + '_strength'
                sext_stren = float(i.split(':')[1].split('k2=')[1].split(',')[0])
                fout.write('{0:16} = {1: 9.4f};\n'.format(sext,sext_stren/2))
    
try:
    
    for files in sys.argv[1:]:
        elegant2AT(filename=files)
except IndexError:
    usage()
