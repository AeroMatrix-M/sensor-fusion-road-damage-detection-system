"""
Edge pipeline for road damage detection system.

This module orchestrates:
- Vision-based detection (YOLO)
- Perception-level verification (verified vs unverified)
- Laser depth measurement
- Sensor fusion & severity assessment
- GPS geo-tagging

Outputs map-ready road damage data.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to Python path to allow imports
# This ensures the script works when run directly
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# Now import from sibling modules
from perception.image_detection import detect_road_damage
from perception.detection_verification import verify_detections
from depth.laser_depth_reader import get_depth_data
from fusion.road_damage_assessment import assess_road_damage
from gps.geo_tagging import get_gps_location


def run_edge_pipeline(mode="mock"):
    """
    Execute one full detection cycle on the edge device.
    
    Args:
        mode: Operating mode - "mock" for testing, "real" for hardware integration
        
    Returns:
        List of map-ready detection outputs, or None if no detections
    """

    # Step 1: Vision-based detection (wide view via YOLO)
    print("Step 1: Running vision-based detection...")
    vision_detections = detect_road_damage(mode=mode)
    print(f"  Found {len(vision_detections)} vision detections")

    # Step 2: Laser depth sensing (local precision)
    print("\nStep 2: Reading laser depth data...")
    depth_data = get_depth_data(mode=mode)
    
    # Determine whether laser coverage is available
    laser_available = bool(depth_data and "depth_values" in depth_data)
    print(f"  Laser coverage available: {laser_available}")

    # Step 3: Perception-level verification (verified/unverified tagging)
    print("\nStep 3: Verifying detections...")
    vision_detections = verify_detections(
        vision_detections,
        laser_coverage=laser_available
    )
    for det in vision_detections:
        print(f"  {det['type']}: {det['verification']}")

    # Step 4: Sensor fusion & severity assessment
    print("\nStep 4: Performing sensor fusion...")
    fused_results = assess_road_damage(vision_detections, depth_data)

    if not fused_results:
        print("  No damage detected")
        return None
    
    print(f"  Generated {len(fused_results)} fused assessments")

    # Step 5: GPS geo-tagging
    print("\nStep 5: Acquiring GPS location...")
    gps_data = get_gps_location(mode=mode)
    print(f"  Location: {gps_data['latitude']}, {gps_data['longitude']}")

    # Step 6: Prepare map-ready output
    print("\nStep 6: Preparing map-ready output...")
    map_ready_outputs = []
    for result in fused_results:
        output_entry = {
            "latitude": gps_data["latitude"],
            "longitude": gps_data["longitude"],
            "damage_type": result.get("type"),
            "depth_mm": result.get("depth_mm"),
            "severity": result.get("severity", "unknown"),
            "verification": result.get("verification", "unverified"),
            "confidence": result.get("confidence", 0.0),
            "source": result.get("source", "unknown")
        }
        map_ready_outputs.append(output_entry)
        print(f"  ✓ {output_entry['damage_type']} - {output_entry['severity']} ({output_entry['verification']})")

    return map_ready_outputs


def main():
    """
    Main execution function for testing the pipeline.
    """
    print("=" * 60)
    print("ROAD DAMAGE DETECTION - EDGE PIPELINE")
    print("=" * 60)
    print()
    
    # Run the pipeline in mock mode
    output = run_edge_pipeline(mode="mock")
    
    print("\n" + "=" * 60)
    print("FINAL OUTPUT")
    print("=" * 60)
    
    if output:
        import json
        print(json.dumps(output, indent=2))
    else:
        print("No detections to report")
    
    print("\n" + "=" * 60)
    print("Pipeline execution complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
