# This file records every action taken in the system
# Think of it as a security camera that never turns off
# Every create, edit, delete, login is permanently logged here

from datetime import datetime
from database.db_connection import get_database

db = get_database()
audit_collection = db["audit_logs"]


def log_action(action, user, details="", record_ref=""):
    # Records a single action to the audit log
    # This function will be called from everywhere in the app
    
    # user is the full user dictionary from the login session
    # so we always have their name, username, and clearance
    
    log_entry = {
        # What action was performed
        # Examples: LOGIN, CREATE_INCIDENT, EDIT_INCIDENT,
        #           DELETE_INCIDENT, CREATE_USER, RESET_PASSWORD
        "action":        action,
        
        # Who did it - pulled from login session automatically
        "username":      user.get("username", "unknown"),
        "user_name":     user.get("name", "unknown"),
        "clearance":     user.get("clearance_level", "unknown"),
        "role":          user.get("role", "unknown"),
        
        # Which record was affected (incident ID, personnel ID etc.)
        # Empty string if not applicable (like a LOGIN action)
        "record_ref":    str(record_ref),
        
        # Human readable description of what happened
        "details":       details,
        
        # Exact timestamp - automatically recorded
        "timestamp":     datetime.now(),
        
        # Date only - makes it easy to filter logs by date
        "date":          datetime.now().strftime("%Y-%m-%d"),
    }
    
    audit_collection.insert_one(log_entry)


def get_all_logs():
    # Returns all audit logs sorted by newest first
    # -1 means descending order (newest at top)
    return list(audit_collection.find().sort("timestamp", -1))


def get_logs_by_user(username):
    # Returns all actions by a specific user
    return list(audit_collection.find(
        {"username": username}
    ).sort("timestamp", -1))


def get_logs_by_action(action):
    # Returns all logs of a specific action type
    # Example: get_logs_by_action("DELETE_INCIDENT")
    return list(audit_collection.find(
        {"action": action}
    ).sort("timestamp", -1))


def get_recent_logs(limit=50):
    # Returns the most recent N log entries
    # Default is 50 - used for the dashboard activity feed
    return list(audit_collection.find().sort(
        "timestamp", -1
    ).limit(limit))