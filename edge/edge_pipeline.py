"""
Edge pipeline for road damage detection system.

This module orchestrates:
- Vision-based detection
- Laser depth measurement
- Sensor fusion & severity assessment
- GPS geo-tagging

Outputs map-ready road damage data.
"""

from perception.image_detection import detect_road_damage
from depth.laser_depth_reader import get_depth_data
from fusion.road_damage_assessment import assess_road_damage
from gps.geo_tagging import get_gps_location


def run_edge_pipeline():
    """
    Execute one full detection cycle on the edge device.
    """

    # Step 1: Vision-based detection (wide view)
    vision_detections = detect_road_damage()

    # Step 2: Laser depth sensing (local precision)
    depth_data = get_depth_data()

    # Step 3: Sensor fusion & severity assessment
    fused_results = assess_road_damage(vision_detections, depth_data)

    if not fused_results:
        return None

    # Step 4: GPS geo-tagging
    gps_data = get_gps_location()

    # Step 5: Prepare map-ready output
    map_ready_outputs = []
    for result in fused_results:
        map_ready_outputs.append({
            "latitude": gps_data["latitude"],
            "longitude": gps_data["longitude"],
            "damage_type": result["type"],
            "depth_mm": result["depth_mm"],
            "severity": result["severity"],
            "confidence": result["confidence"],
            "source": result["source"]
        })

    return map_ready_outputs


if __name__ == "__main__":
    output = run_edge_pipeline()
    if output:
        for entry in output:
            print(entry)
