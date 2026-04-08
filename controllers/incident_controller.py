# Updated incident_controller.py
# Now records every action to the audit log
# And pulls reported_by from the logged in user automatically

from database.db_connection import get_database
from models.incident import create_incident, get_risk_label
from utils.audit_logger import log_action

db = get_database()
incidents_collection = db["incidents"]


def add_incident(title, incident_type, location, severity,
                 description, current_user):
    # Notice: reported_by is no longer a parameter
    # We pull it automatically from current_user
    
    new_incident = create_incident(
        title         = title,
        incident_type = incident_type,
        location      = location,
        severity      = severity,
        description   = description,
        reported_by   = current_user["name"],  # auto from session
    )
    
    # Also store username and clearance for full traceability
    new_incident["reported_by_username"]  = current_user["username"]
    new_incident["reported_by_clearance"] = current_user["clearance_level"]
    
    result = incidents_collection.insert_one(new_incident)
    
    # Record this action in the audit log
    log_action(
        action     = "CREATE_INCIDENT",
        user       = current_user,
        details    = f"Created incident: {title} | Severity: {severity} | Location: {location}",
        record_ref = result.inserted_id
    )
    
    return result.inserted_id


def get_all_incidents():
    return list(incidents_collection.find().sort("date_logged", -1))


def get_incidents_by_severity(severity):
    return list(incidents_collection.find(
        {"severity": severity}
    ).sort("date_logged", -1))


def get_incidents_by_location(location):
    return list(incidents_collection.find(
        {"location": location}
    ).sort("date_logged", -1))


def update_incident_status(incident_id, new_status, current_user):
    from bson.objectid import ObjectId
    
    # Get the incident title for the audit log
    incident = incidents_collection.find_one({"_id": ObjectId(incident_id)})
    
    incidents_collection.update_one(
        {"_id": ObjectId(incident_id)},
        {"$set": {
            "status":          new_status,
            "last_updated_by": current_user["name"],
            "last_updated_at": __import__("datetime").datetime.now()
        }}
    )
    
    # Record the update in audit log
    log_action(
        action     = "UPDATE_INCIDENT",
        user       = current_user,
        details    = f"Status changed to '{new_status}' for: {incident['title']}",
        record_ref = incident_id
    )


def delete_incident(incident_id, current_user):
    from bson.objectid import ObjectId
    
    incident = incidents_collection.find_one({"_id": ObjectId(incident_id)})
    
    incidents_collection.delete_one({"_id": ObjectId(incident_id)})
    
    # Record deletion in audit log
    log_action(
        action     = "DELETE_INCIDENT",
        user       = current_user,
        details    = f"Deleted incident: {incident['title']}",
        record_ref = incident_id
    )


def get_incident_count():
    return incidents_collection.count_documents({})