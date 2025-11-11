import mysql.connector

def get_connection(role=None):
    role_users = {
        "Manager": ("manager_user", "manager123"),
        "Supervisor": ("supervisor_user", "supervisor123"),
        "Receptionist": ("reception_user", "recept123"),
        "Agent": ("agent_user", "agent123"),
        "Clerk": ("clerk_user", "clerk123"),
    }

    # default: root user
    username, password = ("root", "blue_wings_22")

    if role in role_users:
        username, password = role_users[role]

    try:
        return mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database="vehicle_rental"
        )
    except mysql.connector.Error as e:
        raise Exception(f"Database connection failed for role '{role}': {e}")
