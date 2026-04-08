# This file handles everything related to users and login
# Including password hashing and login verification

import hashlib
from database.db_connection import get_database

db = get_database()
users_collection = db["users"]


def hash_password(password):
    # Converts a plain text password into a secure hash
    # hashlib.sha256 is Python's built-in hashing function
    # .encode() converts the string to bytes - required by hashlib
    # .hexdigest() gives us the final hash as a readable string
    
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username, password, name, rank, clearance_level, role):
    # Saves a new user to the database
    # Notice we NEVER store the plain password
    # We only store the hash
    
    user = {
        "username":       username,
        "password_hash":  hash_password(password),  # hashed, not plain
        "name":           name,
        "rank":           rank,
        "clearance_level": clearance_level,
        "role":           role,
        "is_active":      True
    }
    
    # Check if username already exists before inserting
    existing = users_collection.find_one({"username": username})
    if existing:
        print(f"User '{username}' already exists - skipping")
        return None
    
    result = users_collection.insert_one(user)
    print(f"User '{username}' created with ID: {result.inserted_id}")
    return result.inserted_id


def verify_login(username, password):
    from utils.audit_logger import log_action
    
    user = users_collection.find_one({"username": username})
    
    if not user:
        return None
    
    entered_hash = hash_password(password)
    
    if entered_hash == user["password_hash"]:
        # Log successful login
        log_action(
            action  = "LOGIN",
            user    = user,
            details = f"Successful login from username: {username}"
        )
        return user
    else:
        # Log failed attempt - important for security monitoring
        log_action(
            action  = "FAILED_LOGIN",
            user    = {"username": username, "name": "Unknown",
                      "clearance_level": "None", "role": "None"},
            details = f"Failed login attempt for username: {username}"
        )
        return None


def get_all_users():
    # Returns all users - used by admin only
    return list(users_collection.find())


def setup_default_users():
    # Creates default system users for testing
    # In a real system these would be created through an admin panel
    
    print("Setting up default users...")
    print("")
    
    create_user(
        username        = "admin",
        password        = "Admin@1234",
        name            = "System Administrator",
        rank            = "Commander",
        clearance_level = "L4",
        role            = "Admin"
    )
    
    create_user(
        username        = "officer1",
        password        = "Officer@123",
        name            = "Major Arjun Singh",
        rank            = "Major",
        clearance_level = "L3",
        role            = "Officer"
    )
    
    create_user(
        username        = "analyst1",
        password        = "Analyst@123",
        name            = "Lt. Priya Sharma",
        rank            = "Lieutenant",
        clearance_level = "L2",
        role            = "Analyst"
    )
    
    create_user(
        username        = "field1",
        password        = "Field@123",
        name            = "Constable Rahul Verma",
        rank            = "Constable",
        clearance_level = "L1",
        role            = "Field Analyst"
    )
    
    print("")
    print("Default users created ✓")