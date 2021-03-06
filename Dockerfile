# Without this pre-building every build will be taking an hour on CircleCI.
# They have docker layer caching, which is very faulty.
FROM antonkir/snailshell_life_dashboard_requirements:latest
MAINTAINER "Anton Kirilenko" <antony.kirilenko@gmail.com>

ENV QEMU_EXECVE 1
ENV ROOT /opt/snailshell/life_dashboard/
ENV STATIC_ROOT $ROOT/static
ENV RUN_USER snailshell-cp-user
COPY qemu/cross-build-end qemu/cross-build-start qemu/qemu-arm-static qemu/sh-shim /usr/bin/
RUN ["cross-build-start"]

# Create the user that will run the app
RUN groupadd $RUN_USER && useradd -m -g $RUN_USER $RUN_USER
RUN mkdir -p $STATIC_ROOT && chown $RUN_USER:$RUN_USER $STATIC_ROOT -R

ENV XDG_RUNTIME_DIR=/run/user/1000
ENV DISPLAY=':0'
RUN usermod -a -G video $RUN_USER

# Requirements are installed in a parent image.
# It takes very long time to build in QEMU, so we explicitely cache it this way.

COPY . $ROOT
WORKDIR $ROOT

RUN ["cross-build-end"]

USER $RUN_USER

CMD ["python3.6", "./run_app.py"]
