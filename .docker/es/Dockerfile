FROM docker.elastic.co/elasticsearch/elasticsearch-oss:7.9.3-amd64

RUN yum -y install wget; mkdir -p /usr/share/elasticsearch/config/hunspell/en_US /usr/share/elasticsearch/config/hunspell/ru_RU
RUN wget -O /tmp/en_US.zip http://ftp5.gwdg.de/pub/openoffice/contrib/dictionaries/en_US.zip && unzip /tmp/en_US.zip -d /usr/share/elasticsearch/config/hunspell/en_US/
RUN wget -O /tmp/ru_RU.zip http://ftp5.gwdg.de/pub/openoffice/contrib/dictionaries/ru_RU.zip && unzip /tmp/ru_RU.zip -d /usr/share/elasticsearch/config/hunspell/ru_RU/