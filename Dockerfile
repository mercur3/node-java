FROM __src_tag_name__

# Installing the dependencies

RUN set -eux && \
    dnf update -y && \
    dnf install -y java-__java_version__-openjdk.x86_64 && \
    rm -rf /var/log /tmp;

