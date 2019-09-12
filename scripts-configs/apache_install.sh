#!/bin/bash

read -p "Enter install location: " INSTALL_PATH

cd $INSTALL_PATH

mkdir build_temp

cd build_temp

# extract the source into build directory
for i in ../*.gz; do tar -zxvf $i; done

# install the dependencies
cd apr-1.7.0 && ./configure --prefix="$INSTALL_PATH/apache/libs/srclib/apr-1.7.0" && make && make install && cd ..
cd apr-util-1.6.1 && ./configure --prefix="$INSTALL_PATH/apache/libs/apr-util-1.6.1" --with-ldap --with-apr="$INSTALL_PATH/apache/libs/srclib/apr-1.7.0" && make && make install && cd ..
cd pcre-8.38 && ./configure --prefix="$INSTALL_PATH/apache/libs/pcre/pcre-8.38" && make && make install && cd ..

# install apache
cd httpd-2.4.39 && ./configure --prefix="$INSTALL_PATH/apache" --with-apr="$INSTALL_PATH/apache/libs/srclib/apr-1.7.0/" --with-apr-util="$INSTALL_PATH/apache/libs/apr-util-1.6.1/" --with-pcre="$INSTALL_PATH/apache/libs/pcre/pcre-8.38" && make && make install && cd ..

# install mod_wsgi
cd mod_wsgi-4.6.5 && ./configure --prefix="$INSTALL_PATH/apache/modules/" --with-apxs="$INSTALL_PATH/apache/bin/apxs" --with-python=/apps/nttech/rbhanot/tools/miniconda3/envs/django-env/bin/python3 && LD_RUN_PATH=/apps/nttech/rbhanot/tools/miniconda3/envs/django-env/lib make && make install & cd $INSTALL_PATH

sed -i -e '/Listen/s/80/9000/g' -e '/ldap/s/^#//g' -e '/rewrite.so/a LoadModule wsgi_module modules/mod_wsgi.so' $INSTALL_PATH/apache/conf/httpd.conf
#sed -i '/Listen/s/80/9000/g' $INSTALL_PATH/apache/conf/httpd.conf
#sed -i '/ldap/s/^#//g' $INSTALL_PATH/apache/conf/httpd.conf
#sed -i '/rewrite.so/a LoadModule wsgi_module modules/mod_wsgi.so' $INSTALL_PATH/apache/conf/httpd.conf

# clean up
# rm -rf build_temp
