FROM eprosima/vulcanexus:jazzy-desktop

ENV ROS_DISTRO=jazzy
ENV ROS_WS=/control_station-ws
ENV VENV_PATH=/py_venv

# Install system-level dependencies
RUN apt update && apt install -y --no-install-recommends \
    python3-venv \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment for Python packages
RUN python3 -m venv $VENV_PATH

# Python dependencies into the virtual environment venv
RUN $VENV_PATH/bin/pip install --upgrade pip && \
    $VENV_PATH/bin/pip install fastapi[standard] requests