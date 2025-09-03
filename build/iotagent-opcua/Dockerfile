FROM iotagent4fiware/iotagent-opcua:2.3.1

USER root 

COPY build/iotagent-opcua/custom-init.sh /opt/iotagent-opcua/custom-init.sh
COPY build/iotagent-opcua/inject.sh /opt/iotagent-opcua/inject.sh

RUN chown root /opt/iotagent-opcua/custom-init.sh  && \
    chgrp root /opt/iotagent-opcua/custom-init.sh

RUN chown root /opt/iotagent-opcua/inject.sh  && \
    chgrp root /opt/iotagent-opcua/inject.sh

RUN chmod 775 /opt/iotagent-opcua/custom-init.sh
RUN chmod 775 /opt/iotagent-opcua/inject.sh

WORKDIR /opt/iotagent-opcua

EXPOSE 4041
ENTRYPOINT ["sh", "custom-init.sh"]