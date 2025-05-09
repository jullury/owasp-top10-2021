FROM httpd:2.4

# Copy static folder to the Apache document root
COPY ./static/ /usr/local/apache2/htdocs/

RUN rm /usr/local/apache2/htdocs/index.html

# Enable .htaccess processing by setting AllowOverride to All
RUN sed -i \
    -e 's/AllowOverride None/AllowOverride All/g' \
    /usr/local/apache2/conf/httpd.conf

# Enable mod_rewrite which is often used with .htaccess
RUN sed -i \
    -e 's/#LoadModule rewrite_module/LoadModule rewrite_module/g' \
    /usr/local/apache2/conf/httpd.conf

# Expose port 80
EXPOSE 80

# Set working directory
WORKDIR /usr/local/apache2/htdocs/

# Default command to start Apache in foreground
CMD ["httpd-foreground"]
