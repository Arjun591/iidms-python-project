# This file defines what an "incident" looks like in our system
# Think of it as a template or a form
# Every incident logged in IIDMS will follow this exact structure

from datetime import datetime

def create_incident(title, incident_type, location, severity, description, reported_by):
    
    # This function takes in all the details about an incident
    # and packages them into a neat dictionary
    # A dictionary in Python is like a form with labeled fields
    
    incident = {
        # The title is a short name for the incident
        # Example: "Border Breach - Sector 7"
        "title": title,
        
        # Type tells us what kind of incident this is
        # Options: "Border Breach", "Cyber Attack", "Recon Activity", "Terror Threat"
        "incident_type": incident_type,
        
        # Where it happened
        # Example: "Sector 7 North", "Cyber Division", "Base Alpha"
        "location": location,
        
        # Severity is a number from 1 to 5
        # 1 = very minor, 5 = extremely critical
        "severity": severity,
        
        # A longer description of what exactly happened
        "description": description,
        
        # Who logged this incident - their name or ID
        "reported_by": reported_by,
        
        # Status tells us if the incident is being handled or is closed
        # Always starts as "Active" when first logged
        "status": "Active",
        
        # This automatically records the exact date and time
        # the incident was logged - we never have to type this manually
        "date_logged": datetime.now(),
        
        # This will store the risk level calculated by our NumPy engine later
        # For now it starts as "Unassessed"
        "risk_level": "Unassessed"
    }
    
    return incident


def get_risk_label(severity):
    # This function converts a severity number into a text label
    # It's simple but important - used throughout the app
    
    if severity == 1:
        return "LOW"
    elif severity == 2:
        return "LOW"
    elif severity == 3:
        return "MODERATE"
    elif severity == 4:
        return "HIGH"
    elif severity == 5:
        return "CRITICAL"
    else:
        return "UNKNOWN"


# Test this file directly
if __name__ == "__main__":
    
    # Let's create a sample incident to make sure everything works
    sample = create_incident(
        title       = "Unauthorized Border Crossing - Sector 4",
        incident_type = "Border Breach",
        location    = "Sector 4 North",
        severity    = 4,
        description = "Three unidentified individuals detected crossing northern perimeter",
        reported_by = "Officer Sharma"
    )
    
    # Print each field of the incident
    print("--- Sample Incident ---")
    for key, value in sample.items():
        print(f"{key}: {value}")
    
    print("")
    print("Risk Label:", get_risk_label(sample["severity"]))
    print("")
    print("Incident model working correctly ✓")