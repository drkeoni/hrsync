#!/bin/zsh
#
# source this file
#
PKG_NAME='hrsync'

ROOT=$(dirname $(dirname $(greadlink -f ${(%):-%N})))
VE_DIR=ve

source $ROOT/$VE_DIR/bin/activate

export PYTHONPATH=${ROOT}${PYTHONPATH:+:$PYTHONPATH}
export PATH=$ROOT/bin${PATH:+:$PATH}
export DEPLOY_MODE=local

export PROMPT='(%F{magenta}${PKG_NAME}%f) %3~ $ '
