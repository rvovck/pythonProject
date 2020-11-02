# Installation guide:
1. Install Python 3.8 or newer
2. Install Poetry
3. Install Apache24
4. In project root folder, run ```poetry install``` to install Flask, WSGI and other packages
5. Change the path variable in pythonProject.wsgi to point to project root folder
6. Run ```mod_wsgi-express module-config``` in project root folder, copy the ```LoadModule``` output to Apache httpd.conf file, save ```WSGIPythonPath``` for later
7. Create a pythonProject.conf file in Apache conf folder, fil it with this
```
WSGIPythonPath 'your wsgi python path from earlier'

<VirtualHost *:80>
    ServerName 127.0.0.1
    WSGIScriptAlias / 'path to pythonproject.wsgi'
    <Directory 'path to project root folder'>
        Require all granted
    </Directory>
</VirtualHost>
```
8. Add ```Include conf/pythonproject.conf``` to the end of httpd.conf
9. Run httpd.exe using cmd
10. Profit!
