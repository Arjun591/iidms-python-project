# This file defines what a "personnel record" looks like in our system
# Personnel means the officers and analysts who USE the system
# and who get ASSIGNED to incidents

from datetime import datetime

def create_personnel(name, rank, unit, clearance_level, contact, role):
    
    # Packages all personnel details into a dictionary
    # Same idea as incident.py - a structured form
    
    personnel = {
        # Full name of the officer or analyst
        # Example: "Major Arjun Singh"
        "name": name,
        
        # Their military rank
        # Example: "Major", "Colonel", "Lieutenant", "Analyst"
        "rank": rank,
        
        # Which unit or division they belong to
        # Example: "Northern Command", "Cyber Intelligence Unit"
        "unit": unit,
        
        # Clearance level determines what they can access in the system
        # L1 = basic access, L2 = moderate, L3 = sensitive, L4 = top secret
        "clearance_level": clearance_level,
        
        # Contact information - email or phone
        "contact": contact,
        
        # Their role in the system
        # Options: "Officer", "Analyst", "Admin"
        "role": role,
        
        # List of incident IDs assigned to this person
        # Starts empty - incidents get added later
        "assigned_incidents": [],
        
        # Automatically records when this record was created
        "date_added": datetime.now(),
        
        # Whether this person's account is active or deactivated
        "is_active": True
    }
    
    return personnel


def get_clearance_label(level):
    # Converts clearance level to a descriptive label
    # Used in the GUI to show colored badges
    
    clearance_map = {
        "L1": "Basic",
        "L2": "Confidential", 
        "L3": "Secret",
        "L4": "Top Secret"
    }
    
    # .get() safely looks up the level
    # if level doesn't exist it returns "Unknown" instead of crashing
    return clearance_map.get(level, "Unknown")


# Test this file directly
if __name__ == "__main__":
    
    # Create a sample officer
    officer = create_personnel(
        name            = "Major Arjun Singh",
        rank            = "Major",
        unit            = "Northern Command Intelligence",
        clearance_level = "L3",
        contact         = "arjun.singh@mil.in",
        role            = "Officer"
    )
    
    # Create a sample analyst
    analyst = create_personnel(
        name            = "Lt. Priya Sharma",
        rank            = "Lieutenant",
        unit            = "Cyber Intelligence Unit",
        clearance_level = "L2",
        contact         = "priya.sharma@mil.in",
        role            = "Analyst"
    )
    
    print("--- Sample Officer ---")
    for key, value in officer.items():
        print(f"{key}: {value}")
    
    print("")
    print("Clearance Label:", get_clearance_label(officer["clearance_level"]))
    
    print("")
    print("--- Sample Analyst ---")
    for key, value in analyst.items():
        print(f"{key}: {value}")
    
    print("")
    print("Clearance Label:", get_clearance_label(analyst["clearance_level"]))
    
    print("")
    print("Personnel model working correctly ✓")