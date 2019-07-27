FROM centos:centos7

COPY . /app

WORKDIR /app

RUN yum install -y lftp perl perl-Data-Dumper 'perl(Archive::Tar)' 'perl(Digest::MD5)' 'perl(List::MoreUtils)' && \
    lftp -e "set ftp:proxy http://nibr-proxy.global.nibr.novartis.net:2011; open ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/; get ncbi-blast-2.9.0+-1.x86_64.rpm; bye" && \
    rpm -ivh ncbi-blast-2.9.0+-1.x86_64.rpm && \
    bash build_blast_database.sh mouse.fna mouse && \
    yum install -y https://centos7.iuscommunity.org/ius-release.rpm && \
    yum install -y python36u python36u-libs python36u-devel python36u-pip && \
    alias python=/usr/bin/python3.6 && \
    yum clean all && \
    rm -rf /var/cache/yum

ENTRYPOINT [ "/bin/bash" ]