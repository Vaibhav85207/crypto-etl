import requests
import psycopg2
from datetime import datetime,timezone

DB_HOST ="db"
DB_NAME = "crypto"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

print("Starting ETL process...")
print("Fetching data from API...")

def fetch_crypto_data():
    url="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    response = requests.get(url)
    print("Fetching data from API...")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")
    print("Data fetched successfully.")

def load_data_to_postgres(data):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT
            )
            cursor = conn.cursor()

            cursor.execute("""  
                CREATE TABLE IF NOT EXISTS crypto_prices (
                    id SERIAL PRIMARY KEY, 
                    currency VARCHAR(50),
                    price_usd NUMERIC,
                    timestamp TIMESTAMP
                )
            """)

            timestamp = datetime.now(timezone.utc)

            for coin, price in data.items():
                cursor.execute("""
                    INSERT INTO crypto_prices (currency, price_usd, timestamp)
                    VALUES (%s, %s, NOW())
                """, (coin, price['usd']))
                conn.commit()

                print("Data loaded successfully into PostgreSQL database.")
                
        except Exception as e:
        
            print(f"An error occurred: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                print("PostgreSQL connection closed.")

if __name__ == "__main__":
    try:
        crypto_data = fetch_crypto_data()
        load_data_to_postgres(crypto_data)
    except Exception as e:
        print(f"ETL process failed: {e}")
    else:
        print("ETL process completed successfully.")
        print("Data loaded into PostgreSQL database.")  