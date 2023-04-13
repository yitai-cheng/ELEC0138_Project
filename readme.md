Enter the OpenSSL directory
Configure OpenSSL：./config
Compile OpenSSL：make
Install OpenSSL: sudo make install
test:openssl version


run https: python manage.py runsslserver --cert D:\new_security\ELEC0138_Project\ssl/server.crt --key D:\new_security\ELEC0138_Project\ssl/server.key



backup:
you should install redis on your computer(there are some difficults) and after that you should run three commands in different terminals:
        celery -A mysite worker --pool=solo -l info

        set DJANGO_SETTINGS_MODULE=myhomwwork.settings
        celery -A mysite beat -l info
        
        sudo -u redis redis-server /mnt/d/new_security/ELEC0138_Project/redis-7.0.10/redis.conf(this commend will start redis server and it is different depends on your configuration)

you can test this function by:
        python manage.py shell
        from mysite.tasks import backup_data_to_google_drive
        result = backup_data_to_google_drive.delay()
