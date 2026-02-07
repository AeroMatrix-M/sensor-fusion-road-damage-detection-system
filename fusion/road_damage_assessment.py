"""
Sensor fusion and road damage assessment module.

Vision provides wide-area detection of road defects.
Laser depth sensing (multi-sensor array) provides high-precision
local validation and helps distinguish potholes from uniform
road features such as speed breakers.
"""

def classify_severity(depth_mm):
    """
    Classify pothole severity based on depth measurement.

    Returns:
        'low', 'moderate', or 'severe'
    """
    if depth_mm < 10:
        return "low"
    elif depth_mm < 25:
        return "moderate"
    else:
        return "severe"


def is_uniform_surface(depth_values, variation_threshold=3):
    """
    Determine whether depth readings are uniform across sensors.

    Uniform depth change across all sensors typically indicates
    a speed breaker or ramp rather than a pothole.

    Args:
        depth_values: List of depth readings from laser sensors
        variation_threshold: Max allowed difference (in mm)

    Returns:
        True if surface is uniform, False otherwise
    """
    if not depth_values:
        return False

    return (max(depth_values) - min(depth_values)) <= variation_threshold


def assess_road_damage(vision_detections, depth_data):
    """
    Fuse vision-based detections with laser depth sensing,
    filter out road features, and assign severity levels.

    Args:
        vision_detections: List of detections from vision module
        depth_data: Dictionary containing laser depth readings
                    {
                        "depth_values": [d1, d2, d3, ...],
                        "confidence": float
                    }

    Returns:
        List of fused road damage assessments
    """

    if not depth_data or "depth_values" not in depth_data:
        return None

    depth_values = depth_data["depth_values"]
    max_depth = max(depth_values)
    severity_level = classify_severity(max_depth)

    # Case 1: Uniform elevation change → speed breaker / road feature
    if is_uniform_surface(depth_values):
        return [{
            "type": "road-feature",
            "feature": "speed-breaker",
            "severity": "ignore",
            "confidence": depth_data.get("confidence", 0.8),
            "source": "laser-array"
        }]

    fused_results = []

    # Case 2: Vision + laser confirmed pothole
    if vision_detections:
        for d in vision_detections:
            fused_results.append({
                "type": d["type"],
                "depth_mm": max_depth,
                "severity": severity_level,
                "confidence": d["confidence"],
                "source": "vision+laser"
            })

    # Case 3: Laser-only localized micro-damage
    else:
        fused_results.append({
            "type": "micro-damage",
            "depth_mm": max_depth,
            "severity": severity_level,
            "confidence": depth_data.get("confidence", 0.8),
            "source": "laser-only"
        })

    return fused_results
