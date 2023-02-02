from waitress import serve

from EnergoProcess.wsgi import application

if __name__ == '__main__':
    serve(application, port='8000')