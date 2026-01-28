from app import create_app

app = create_app()

if __name__ == '__main__':
    from waitress import serve
    from app.config import Config
    
    serve(
        app,
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        threads=10
    )
