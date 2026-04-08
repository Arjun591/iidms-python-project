import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.user_controller import verify_login
from controllers.incident_controller import add_incident
from utils.audit_logger import get_recent_logs

# Simulate a login
print("Logging in as officer1...")
user = verify_login("officer1", "Officer@123")
print(f"Logged in as: {user['name']} [{user['clearance_level']}]")
print("")

# Add an incident as this logged in user
print("Adding incident...")
add_incident(
    title         = "Suspicious Vehicle - Gate 3",
    incident_type = "Border Breach",
    location      = "Gate 3 South",
    severity      = 3,
    description   = "Unregistered vehicle attempting entry",
    current_user  = user    # ← automatically records who did this
)
print("")

# Show recent audit logs
print("=== Recent Audit Log ===")
logs = get_recent_logs(10)
for log in logs:
    print(f"  [{log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}]"
          f"  {log['action']:20}"
          f"  {log['username']:12}"
          f"  {log['details'][:50]}")

print("")
print("Audit logging working correctly ✓")