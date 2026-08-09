from ecosphere import create_app, db
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # This will create database tables automatically if they do not exist
        # Works for SQLite fallback or standard MySQL
        try:
            db.create_all()
            print("Database tables initialized successfully.")
        except Exception as e:
            print(f"Warning: Could not auto-initialize database tables: {e}")
            print("Please ensure your database is running and configured correctly.")
            
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
