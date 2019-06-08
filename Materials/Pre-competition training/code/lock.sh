#!/bin/bash
# variable
BaseDir=/sys/class/gpio/
Gpio=12
GpioDir=${BaseDir}"gpio"${Gpio}"/"


if [ ! -d $GpioDir ]; then
echo "fa" | sudo -S echo $Gpio > ${BaseDir}"export"
echo "Export GPIO"${Gpio}
fi
echo "fa" | sudo -S echo $1 > ${GpioDir}"direction"
echo "Write $1 to direction"
