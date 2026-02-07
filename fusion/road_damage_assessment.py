"""
Sensor fusion and road damage assessment module.

Vision provides wide-area detection of road defects.
Laser depth sensing provides high-precision local validation
and detection of fine-grained surface damage.
"""

def classify_severity(depth_mm):
    """
    Classify pothole severity based on depth.

    Returns:
        'low', 'moderate', or 'severe'
    """
    if depth_mm < 10:
        return "low"
    elif depth_mm < 25:
        return "moderate"
    else:
        return "severe"


def assess_road_damage(vision_detections, depth_data):
    """
    Fuse vision-based detections with laser depth sensing
    and assign severity levels for mapping.
    """

    if not depth_data:
        return None

    severity_level = classify_severity(depth_data["depth_mm"])
    fused_results = []

    # Vision + laser validated damage
    if vision_detections:
        for d in vision_detections:
            fused_results.append({
                "type": d["type"],
                "depth_mm": depth_data["depth_mm"],
                "severity": severity_level,
                "confidence": d["confidence"],
                "source": "vision+laser"
            })

    # Laser-only local micro-damage
    else:
        fused_results.append({
            "type": "micro-damage",
            "depth_mm": depth_data["depth_mm"],
            "severity": severity_level,
            "confidence": depth_data.get("confidence", 0.8),
            "source": "laser-only"
        })

    return fused_results
