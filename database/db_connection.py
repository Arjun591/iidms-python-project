# This file does one job only:
# it connects our Python app to MongoDB
# Think of it as the phone line between our app and the database

from pymongo import MongoClient

def get_database():
    # MongoClient is like dialing a phone number
    # 27017 is the default port MongoDB listens on
    # This is always the address when MongoDB runs on your own computer
    client = MongoClient("mongodb://127.0.0.1:27017/")
    
    # This creates (or opens) a database called "iidms"
    # If it doesn't exist yet, MongoDB creates it automatically
    db = client["iidms"]
    
    return db

# This part only runs if you run THIS file directly
# It won't run when other files import from this file
if __name__ == "__main__":
    db = get_database()
    print("Connected to database:", db.name)
    print("MongoDB connection successful ✓")