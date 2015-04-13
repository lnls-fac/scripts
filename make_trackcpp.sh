#!/bin/bash

cd $FACCODE/trackcpp; make all -j && make install
cd $FACCODE/trackcpp/python_swig_module; make all -j && make install

