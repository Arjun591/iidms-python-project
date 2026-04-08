# This file handles all database operations for personnel
# Same structure as incident_controller.py but for officers and analysts

from database.db_connection import get_database
from models.personnel import create_personnel, get_clearance_label

# Get database and personnel collection
db = get_database()
personnel_collection = db["personnel"]


def add_personnel(name, rank, unit, clearance_level, contact, role):
    # CREATE - saves a new personnel record to MongoDB
    
    new_personnel = create_personnel(
        name            = name,
        rank            = rank,
        unit            = unit,
        clearance_level = clearance_level,
        contact         = contact,
        role            = role
    )
    
    result = personnel_collection.insert_one(new_personnel)
    print(f"Personnel saved with ID: {result.inserted_id}")
    return result.inserted_id


def get_all_personnel():
    # READ - fetches all personnel records
    personnel = list(personnel_collection.find())
    return personnel


def get_personnel_by_role(role):
    # READ - fetches only officers OR only analysts
    # Example: get_personnel_by_role("Officer")
    personnel = list(personnel_collection.find({"role": role}))
    return personnel


def get_personnel_by_clearance(clearance_level):
    # READ - fetches personnel by clearance level
    # Example: get_personnel_by_clearance("L4")
    personnel = list(personnel_collection.find({"clearance_level": clearance_level}))
    return personnel


def update_personnel_clearance(personnel_id, new_clearance):
    # UPDATE - promotes or changes clearance level of a person
    
    from bson.objectid import ObjectId
    
    personnel_collection.update_one(
        {"_id": ObjectId(personnel_id)},
        {"$set": {"clearance_level": new_clearance}}
    )
    print(f"Personnel {personnel_id} clearance updated to: {new_clearance}")


def assign_incident_to_personnel(personnel_id, incident_id):
    # UPDATE - assigns an incident to a personnel member
    # $push adds a new item to a list without removing existing ones
    # Remember "assigned_incidents" was an empty list [] in our model
    
    from bson.objectid import ObjectId
    
    personnel_collection.update_one(
        {"_id": ObjectId(personnel_id)},
        {"$push": {"assigned_incidents": incident_id}}
    )
    print(f"Incident {incident_id} assigned to personnel {personnel_id}")


def deactivate_personnel(personnel_id):
    # UPDATE - deactivates a personnel account
    # We never delete personnel records in a real system
    # We just mark them as inactive - for audit purposes
    
    from bson.objectid import ObjectId
    
    personnel_collection.update_one(
        {"_id": ObjectId(personnel_id)},
        {"$set": {"is_active": False}}
    )
    print(f"Personnel {personnel_id} deactivated")


def get_personnel_count():
    # Returns total number of personnel records
    return personnel_collection.count_documents({})