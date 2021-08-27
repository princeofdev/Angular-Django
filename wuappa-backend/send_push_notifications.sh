#!/bin/bash

export LC_ALL=C
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

source ~/.env && \
pyenv activate env && \
python manage.py sendnotifications
