from app import Web
from app.Web import logger
from config import DEFAULT_HOST, DEFAULT_PORT, IS_DEBUG, APP_ENV

if __name__  == '__main__':
    logger.info(f"Starting app in {APP_ENV} environment")
    logger.info(f"With config: host={DEFAULT_HOST}, port={DEFAULT_PORT}, debug={IS_DEBUG()}")
    Web.app.run(host=DEFAULT_HOST, port=DEFAULT_PORT, debug=IS_DEBUG())
