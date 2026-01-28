from app import create_app

app = create_app()

if __name__ == '__main__':
    from app.config import Config
    
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )
