import pymysql

def create_database():
    # Try different common configurations for local MySQL dev
    configs = [
        {'host': 'localhost', 'user': 'root', 'password': ''},
        {'host': 'localhost', 'user': 'root', 'password': 'root'},
        {'host': '127.0.0.1', 'user': 'root', 'password': ''},
    ]

    conn = None
    success_config = None

    for config in configs:
        try:
            print(f"Trying connection with user='{config['user']}', password='{config['password']}'...")
            conn = pymysql.connect(
                host=config['host'],
                user=config['user'],
                password=config['password']
            )
            success_config = config
            print("Connected successfully!")
            break
        except pymysql.err.OperationalError as e:
            print(f"Connection failed: {e}")
    
    if not conn:
        print("Could not connect to MySQL server. Please ensure MySQL is running and update credentials in the script.")
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS library_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print("Database 'library_db' created or already exists.")
        conn.commit()
        
        # Save working config to a file or print it for user to know
        print(f"Verified connection: {success_config}")
        return success_config
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()
