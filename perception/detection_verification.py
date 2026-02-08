"""
Perception-level verification module.

Tags camera detections as VERIFIED or UNVERIFIED
based on laser coverage.
"""

def verify_detections(yolo_detections, laser_coverage):
    """
    Assign verification status to YOLO detections.

    Args:
        yolo_detections: Output from YOLO detection
        laser_coverage: Boolean (True if laser covers this region)

    Returns:
        List of detections with verification metadata
    """

    verified_detections = []

    for d in yolo_detections:
        detection = d.copy()

        if laser_coverage:
            detection["verification"] = "verified"
            detection["source"] = "vision+laser"
        else:
            detection["verification"] = "unverified"
            detection["source"] = "vision-only"

        verified_detections.append(detection)

    return verified_detections
