#!/bin/bash
set -e

source /opt/vulcanexus/jazzy/setup.bash

# Build workspace if needed
if [ ! -f /control_station_ws/install/setup.bash ]; then
    echo "🔨 Building workspace..."
    colcon build --symlink-install --base-paths /control_station_ws/src --install-base /control_station_ws/install
fi

# Source workspace
source /control_station_ws/install/setup.bash
# exec ros2 run defective_pcb_detector defective_pcb_publisher

# Run app (replace with your logic)
exec "$@"