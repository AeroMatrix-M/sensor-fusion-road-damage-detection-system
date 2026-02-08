"""
YOLO-based image detection module.

Detects potholes and road surface damage from dashcam images.
This module ONLY performs visual detection.
"""

def detect_road_damage(image=None, mode="mock"):
    """
    Detect road damage using YOLO.

    Args:
        image: Dashcam frame (optional in mock mode)
        mode: "mock" for testing, "yolo" for real inference

    Returns:
        List of detections
    """

    if mode == "mock":
        # Simulated YOLO output
        return [
            {
                "type": "pothole",
                "confidence": 0.87,
                "bbox": [120, 300, 200, 380],
                "estimated_area": 6400
            },
            {
                "type": "crack",
                "confidence": 0.74,
                "bbox": [420, 310, 520, 350],
                "estimated_area": 2400
            }
        ]

    elif mode == "yolo":
        # REAL YOLO INTEGRATION (later)
        # 1. Load YOLO weights
        # 2. Run inference on image
        # 3. Return detections in the SAME format

        raise NotImplementedError(
            "YOLO inference integration pending prototype phase"
        )
