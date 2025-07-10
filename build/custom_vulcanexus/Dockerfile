FROM eprosima/vulcanexus:jazzy-desktop

ENV ROS_DISTROO=vulcanexus/jazzy
ENV ROS_WS=/control_station_ws


RUN curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | \
    gpg --dearmor --batch --yes -o /usr/share/keyrings/ros2-latest-archive-keyring.gpg


# Install deps
RUN apt update && apt install -y \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-virtualenv\
    python3-requests\
    python3-empy\
    python3-catkin-pkg\
    python3-numpy\
    python3-lark\
    python3-uvicorn\
    python3-fastapi\
    x11-apps \
    && rm -rf /var/lib/apt/lists/*



# to source the ros distribution on the .bashrc
RUN echo 'if [ -n "$BASH_VERSION" ]; then' >> /root/.bashrc && \
    echo '  [ -f /opt/${ROS_DISTROO}/setup.bash ] && source /opt/${ROS_DISTROO}/setup.bash' >> /root/.bashrc && \
    echo '  [ -f ${ROS_WS}/install/setup.bash ] && source ${ROS_WS}/install/setup.bash' >> /root/.bashrc && \
    echo 'fi' >> /root/.bashrc



# # Create directory and python venv
RUN mkdir -p ${ROS_WS} 

COPY configs/ros2_pkgs/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
    