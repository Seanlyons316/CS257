'''
    app.py
    Sean Lyons and Matvei Keshkekian, 19 May 2025
    Adapted from Jeff Ondich, 25 April 2016

    A tiny Flask application that provides a website with an accompanying
    API (which is also tiny) to support that website.
'''
import sys
from flask import render_template
import flask
import api as api
########### Initializing Flask ###########
# Note that this stuff has to be up here at the top, because otherwise
# the @app.route lines would raise a "name not defined" exception.
app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.app, url_prefix='/api')


########### The website routes ###########
# (As you can see, there's not much of a website in this example.)
@app.route('/') 
def get_main_page():
    ''' This is the only route intended for human users '''
    return flask.render_template('index.html')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')
@app.route('/search')
def search_list():
    return render_template('search_list.html')

@app.route('/tsunami/<int:wave_id>')
def tsunami_info(wave_id):
    return render_template('tsunami_info.html', wave_id=wave_id)

@app.route('/map')
def world_map():
    return render_template('world_map.html')



########### Running the website server ###########
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    app.run(host=host, port=port, debug=True)
