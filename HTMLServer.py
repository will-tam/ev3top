from bottle import Bottle, template, run

class HTMLServer():
    """

    # Public attributes.
        None.
    """

    frmwk = Bottle()

    # Private attributes.

    # Public methods.

    def __init__(self):
        """
        Constructor.
        @parameter : none.
        @return : none.
        """
        pass
#        self.frmwk = Bottle()

    @frmwk.route('/')
    def index(self):
        """
        index.html simulation.
        @parameter : none.
        @return : none.
        """
        body = "<h1>EV3Dev</h1>"
        return template(body)

    # Private methods.


#    @app.route('/hello')
#    def hello():
#        return "Hello World!"
#
#    @app.route('/')
#    @app.route('/hello/<name>')
#    def greet(name='Stranger'):
#        return template('Hello {{name}}, how are you?', name=name)
#

#app.run(self.__frmwk, host='10.42.0.131', port=8080)

