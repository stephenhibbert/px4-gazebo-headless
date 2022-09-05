#!/bin/bash

function show_help {
    echo ""
    echo "Usage: ${0} [-h | -v VEHICLE | -w WORLD | -n NUMBER | -lat LATITUDE | -lon LONGITUDE] [IP_API | IP_QGC IP_API]"
    echo ""
    echo "Run a headless px4-gazebo simulation in a docker container. The"
    echo "available vehicles and worlds are the ones available in PX4"
    echo "(i.e. when running e.g. \`make px4_sitl gazebo_iris__baylands\`)"
    echo ""
    echo "  -h    Show this help"
    echo "  -v    Set the vehicle (default: iris) iris, plane, standard_vtol, rover, r1_rover, typhoon_h480"
    echo "  -w    Set the world (default: empty)"
    echo "  -n    Set the number of drones to simulate (default: 2)"
    echo "  -a  Set the home latitude (default: 51.50813980651898)"
    echo "  -o  Set the home longitude (default: -0.09708083901920365)"
    echo ""
    echo "  <IP_API> is the IP to which PX4 will send MAVLink on UDP port 14540"
    echo "  <IP_QGC> is the IP to which PX4 will send MAVLink on UDP port 14550"
    echo ""
    echo "By default, MAVLink is sent to the host."
}

OPTIND=1 # Reset in case getopts has been used previously in the shell.

vehicle=iris
world=empty
number=2
lat=51.50813980651898
lon=-0.09708083901920365

while getopts "h?v:w:n:" opt; do
    case "$opt" in
    h|\?)
        show_help
        exit 0
        ;;
    v)  vehicle=$OPTARG
        ;;
    w)  world=$OPTARG
        ;;
    n)  number=$OPTARG
        ;;
    a)  lat=$OPTARG
        ;;
    o)  lon=$OPTARG
        ;;
    esac
done

shift $((OPTIND-1))

# All the leftover arguments are supposed to be IPs
for arg in "$@"
do
    if ! [[ ${arg} =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "Error: invalid IP: ${arg}!"
        echo ""
        show_help
        exit 1
    fi
done

if [ "$#" -eq 1 ]; then
    IP_QGC="$1"
elif [ "$#" -eq 2 ]; then
    IP_API="$1"
    IP_QGC="$2"
elif [ "$#" -gt 2 ]; then
    show_help
    exit 1;
fi

Xvfb :99 -screen 0 1600x1200x24+32 &
${SITL_RTSP_PROXY}/build/sitl_rtsp_proxy &

source ${WORKSPACE_DIR}/edit_rcS.bash ${IP_API} ${IP_QGC} &&
cd ${FIRMWARE_DIR} &&
# HEADLESS=1 make px4_sitl gazebo_${vehicle}__${world}
HEADLESS=1 PX4_HOME_LAT=${lat} PX4_HOME_LON=${lon} ./Tools/simulation/gazebo/sitl_multiple_run.sh -n ${number} -m ${vehicle}

exec "${@:1}"
