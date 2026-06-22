"""
MiroFish Backend - Flask Application Factory
"""

import os
import warnings

# Suppress multiprocessing resource_tracker warnings (from third-party libraries like transformers)
# Must be set before all other imports
warnings.filterwarnings("ignore", message=".*resource_tracker.*")

from flask import Flask, request
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logger, get_logger


def create_app(config_class=Config):
    """Flask application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure JSON encoding: ensure Chinese displays directly (not as \uXXXX)
    # Flask >= 2.3 uses app.json.ensure_ascii, older versions use JSON_AS_ASCII config
    if hasattr(app, 'json') and hasattr(app.json, 'ensure_ascii'):
        app.json.ensure_ascii = False

    # Setup logging
    logger = setup_logger('mirofish')

    # Only print startup info in reloader subprocess (avoid printing twice in debug mode)
    is_reloader_process = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    debug_mode = app.config.get('DEBUG', False)
    should_log_startup = not debug_mode or is_reloader_process

    if should_log_startup:
        logger.info("=" * 50)
        logger.info("MiroFish-Offline Backend starting...")
        logger.info("=" * 50)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # --- Initialize Neo4jStorage singleton (DI via app.extensions) ---
    from .storage import Neo4jStorage
    try:
        neo4j_storage = Neo4jStorage()
        app.extensions['neo4j_storage'] = neo4j_storage
        if should_log_startup:
            logger.info("Neo4jStorage initialized (connected to %s)", Config.NEO4J_URI)
    except Exception as e:
        logger.error("Neo4jStorage initialization failed: %s", e)
        # Store None so endpoints can return 503 gracefully
        app.extensions['neo4j_storage'] = None

    # Register simulation process cleanup function (ensure all simulation processes terminate on server shutdown)
    from .services.simulation_runner import SimulationRunner
    SimulationRunner.register_cleanup()
    if should_log_startup:
        logger.info("Simulation process cleanup function registered")

    # Request logging middleware
    @app.before_request
    def log_request():
        logger = get_logger('mirofish.request')
        logger.debug(f"Request: {request.method} {request.path}")
        if request.content_type and 'json' in request.content_type:
            logger.debug(f"Request body: {request.get_json(silent=True)}")

    @app.after_request
    def log_response(response):
        logger = get_logger('mirofish.request')
        logger.debug(f"Response: {response.status_code}")
        return response

    # Register blueprints
    from .api import graph_bp, simulation_bp, report_bp
    from .api.settings import settings_bp
    from .api.scraper import scraper_bp
    from .api.auth import auth_bp
    app.register_blueprint(graph_bp, url_prefix='/api/graph')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')
    app.register_blueprint(scraper_bp, url_prefix='/api/scrape')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Seed default admin user
    from .models.user import UserManager
    try:
        UserManager.seed_admin()
        if should_log_startup:
            logger.info("Admin user seeded (username: admin)")
    except Exception as e:
        logger.error("Failed to seed admin user: %s", e)

    # Archive legacy simulations (those created before auth was added)
    _archive_legacy_simulations(logger)

    # Health check
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'MiroFish-Offline Backend'}

    if should_log_startup:
        logger.info("MiroFish-Offline Backend startup complete")

    return app


def _archive_legacy_simulations(logger):
    """Mark pre-auth simulations as archived so only admin can see them."""
    import json
    import os
    from .config import Config

    sims_dir = Config.OASIS_SIMULATION_DATA_DIR
    if not os.path.exists(sims_dir):
        return
    archived_count = 0
    for sim_id in os.listdir(sims_dir):
        state_file = os.path.join(sims_dir, sim_id, 'state.json')
        if not os.path.isfile(state_file):
            continue
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if 'owner_user_id' not in data:
                data['owner_user_id'] = None
                data['archived'] = True
                with open(state_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                archived_count += 1
        except Exception:
            pass
    if archived_count:
        logger.info("Archived %d legacy simulation(s) (pre-auth)", archived_count)

