from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
from pyramid.renderers import render_to_response
import mysql.connector as mysql
from dotenv import load_dotenv
import os

load_dotenv('credentials.env')

'''Enviroment Variables'''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

def gen_table(req):
    start_height = req.matchdict['start_height']
    end_height = req.matchdict['end_height']
    start_age = req.matchdict['start_age']
    end_age = req.matchdict['end_age']

    db = mysql.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_name
    )
    cursor = db.cursor()

    try:
        cursor.execute(f'''
            SELECT * FROM  Gallery_Details
                WHERE height>={start_height} AND height<{end_height}
                    AND age>={start_age} AND age<{end_age};
        ''')
    except:
        return Response("Your request is not quite right!")
    records = cursor.fetchall()
    db.close()

    if(len(records)==0):
        return Response("<div id=\"container\">Nothing found on our database.</div>")

    data = {'records': records}
    
    return render_to_response('gen_table.html', data, request=req)

def get_home(req):
    return FileResponse('index.html')

def main():
    with Configurator() as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_renderer('.html')

        config.add_route('home', '/')
        config.add_view(get_home, route_name='home')

        config.add_route('gen_table', '/table/{start_height}_{end_height}_{start_age}_{end_age}')
        config.add_view(gen_table, route_name='gen_table')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)

        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 80, app)
    print('Web server started on: http://0.0.0.0')
    server.serve_forever()

if __name__ == '__main__':
    main()