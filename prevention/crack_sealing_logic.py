"""
Optional preventive maintenance module.

This module defines logic for sealing early-stage road cracks
to prevent them from developing into potholes.

IMPORTANT:
- This module is OPTIONAL.
- It is only intended for low-speed municipal vehicles.
- It does NOT affect detection or mapping.
"""

def should_apply_preventive_fix(damage_entry, vehicle_speed_kmph):
    """
    Decide whether preventive crack sealing should be applied.

    Args:
        damage_entry: Dictionary containing damage assessment
        vehicle_speed_kmph: Current vehicle speed

    Returns:
        Boolean indicating whether preventive action is allowed
    """

    # Only allow at low speeds (safety constraint)
    if vehicle_speed_kmph > 20:
        return False

    # Only for minor damage
    if damage_entry["severity"] != "low":
        return False

    # Only for cracks or micro-damage
    if damage_entry["damage_type"] not in ["micro-damage", "crack"]:
        return False

    return True


def apply_preventive_fix(damage_entry):
    """
    Placeholder for crack sealing action.

    This function represents triggering a sealing mechanism.
    Actual actuation hardware is NOT implemented here.
    """

    return {
        "status": "preventive_fix_triggered",
        "damage_type": damage_entry["damage_type"],
        "location": {
            "latitude": damage_entry["latitude"],
            "longitude": damage_entry["longitude"]
        }
    }
