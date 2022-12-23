from flask import Flask
from flask import template_rendered
from flaskext.mysql import MySQL

app=Flask (__name__)
mysql=MySQL()

if __name__ == '__main__':
    app.run(debug=True)
