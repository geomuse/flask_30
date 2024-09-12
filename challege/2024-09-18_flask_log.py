from flask import Flask
from loguru import logger

app = Flask(__name__)

logger.add("app.log", 
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {module}:{function}:{line} - {message}", 
           level="DEBUG")
# 使用 Loguru 的 logger 替代默认的 Flask 日志记录器
# logger.add("app.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB")

@app.route('/')
def index():
    logger.info("Serving the index page with Loguru.")
    logger.debug("Debugging the index page.")
    return "Hello, Flask with Loguru!"

if __name__ == '__main__':
    
    app.run(debug=True)
