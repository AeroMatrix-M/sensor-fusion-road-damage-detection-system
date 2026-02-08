"""
Sensor fusion and road damage assessment module.

Combines:
- Vision-based detections (YOLO)
- Laser depth sensing (multi-sensor array)

Responsibilities:
- Distinguish potholes from uniform road features (e.g. speed breakers)
- Assign severity when depth data is available
- Preserve verification status for unverified (vision-only) detections
"""

def classify_severity(depth_mm):
    """
    Classify road damage severity based on depth.

    Args:
        depth_mm: Maximum measured depth in millimeters

    Returns:
        Severity label: 'low', 'moderate', or 'severe'
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

    Uniform readings typically indicate speed breakers or ramps
    rather than potholes.

    Args:
        depth_values: List of depth readings (mm)
        variation_threshold: Max allowed difference (mm)

    Returns:
        True if surface is uniform, False otherwise
    """
    if not depth_values:
        return False

    return (max(depth_values) - min(depth_values)) <= variation_threshold


def assess_road_damage(vision_detections, depth_data):
    """
    Fuse vision detections with laser depth data to assess road damage.

    Args:
        vision_detections: List of detections from perception layer
        depth_data: Laser depth dictionary or None

    Returns:
        List of fused road damage assessments
    """

    # -------------------------------
    # CASE 1: Vision-only detections
    # (Outside laser coverage)
    # -------------------------------
    if not depth_data or "depth_values" not in depth_data:
        if not vision_detections:
            return None

        return [
            {
                "type": d["type"],
                "severity": "unknown",
                "confidence": d["confidence"],
                "verification": d.get("verification", "unverified"),
                "source": d.get("source", "vision-only")
            }
            for d in vision_detections
        ]

    # -------------------------------
    # Laser data available
    # -------------------------------
    depth_values = depth_data["depth_values"]
    max_depth = max(depth_values)

    # Speed breaker / ramp detection
    if is_uniform_surface(depth_values):
        return [{
            "type": "road-feature",
            "feature": "speed-breaker",
            "severity": "ignore",
            "confidence": depth_data.get("confidence", 0.8),
            "source": "laser-array"
        }]

    severity_level = classify_severity(max_depth)
    fused_results = []

    # -------------------------------
    # CASE 2: Vision + laser confirmed
    # -------------------------------
    if vision_detections:
        for d in vision_detections:
            fused_results.append({
                "type": d["type"],
                "depth_mm": max_depth,
                "severity": severity_level,
                "confidence": d["confidence"],
                "verification": d.get("verification", "verified"),
                "source": d.get("source", "vision+laser")
            })

    # -------------------------------
    # CASE 3: Laser-only detection
    # (No vision match, local damage)
    # -------------------------------
    else:
        fused_results.append({
            "type": "micro-damage",
            "depth_mm": max_depth,
            "severity": severity_level,
            "confidence": depth_data.get("confidence", 0.8),
            "verification": "verified",
            "source": "laser-only"
        })

    return fused_results
