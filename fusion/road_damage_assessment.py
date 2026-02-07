"""
Sensor fusion and road damage assessment module.

Vision provides wide-area detection of road defects.
Laser depth sensing provides high-precision local validation
and detection of fine-grained surface damage within a limited area.
"""

def assess_road_damage(vision_detections, depth_data):
    """
    Fuse vision-based detections with laser depth sensing.

    Args:
        vision_detections: List of detections from image-based module
        depth_data: Local laser depth readings

    Returns:
        List of fused road damage assessments
    """

    fused_results = []

    # Case 1: Vision detection validated and refined by laser
    if vision_detections and depth_data:
        for d in vision_detections:
            fused_results.append({
                "type": d["type"],
                "confidence": d["confidence"],
                "depth_mm": depth_data["depth_mm"],
                "source": "vision+laser"
            })

    # Case 2: Laser-only local detection (micro-damage)
    elif depth_data and depth_data["depth_mm"] > 0:
        fused_results.append({
            "type": "micro-damage",
            "confidence": depth_data.get("confidence", 0.8),
            "depth_mm": depth_data["depth_mm"],
            "source": "laser-only"
        })

    if not fused_results:
        return None

    return fused_results
