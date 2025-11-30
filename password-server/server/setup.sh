# !/bin/bash

# image dir
# app/
# wheels/
set -e

# install
pip install -r ./app/requirements.txt

# there is only one
cd wheels
WHEEL_FILE=$(ls)
echo "${WHEEL_FILE}"

cd ../app
pip install ../wheels/${WHEEL_FILE}