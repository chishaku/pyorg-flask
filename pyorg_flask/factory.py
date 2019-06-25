"""Application factory."""

from flask import Flask, render_template


def create_app(config_file=None, config=None):
	"""Create the pyorg Flask application object.

	Parameters
	----------
	config_file : str
		Config file to load. Otherwise use PYORG_CONFIG environment variable.
	config : dict
		Dictionary with additional configuration.

	Returns
	-------
	flask.Flask
	"""
	app = Flask(__package__)

	# Configuration
	app.config.from_object(__package__ + '.config_default')
	if config_file is None:
		app.config.from_envvar('PYORG_CONFIG', silent=True)
	else:
		app.config.from_pyfile(config_file)
	if config is not None:
		app.config.from_mapping(config)

	# Register blueprints
	from .blueprints.files import files_bp
	app.register_blueprint(files_bp, url_prefix='/files/')
	from .blueprints.agenda import agenda_bp
	app.register_blueprint(agenda_bp, url_prefix='/agenda/')

	# Routes
	@app.route('/')
	def home():
		return render_template('home.html.j2')

	return app
