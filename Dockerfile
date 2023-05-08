FROM __src_tag_name__

# Installing the dependencies

RUN set -eux; \
    apt update -y; \
    apt install openjdk-__java_version__-jdk; \
    rm -rf /var/log /tmp;

