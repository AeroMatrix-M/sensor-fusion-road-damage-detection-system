"""
Image-based road damage detection module.

This module represents the vision component of the system.
It uses a YOLO-based approach (to be integrated later)
to detect potholes and surface cracks from dashcam images.
"""

def detect_road_damage(image, mode="mock"):
    """
    Detect potholes and cracks from a road image.

    Args:
        image: Input image frame from dashcam
        mode: "mock" for development, "model" for real inference

    Returns:
        List of detected road damage regions
    """

    if mode == "mock":
        return [
            {
                "type": "pothole",
                "confidence": 0.85,
                "estimated_area": 1200
            }
        ]

    elif mode == "model":
        # TODO: Integrate YOLO segmentation inference here
        raise NotImplementedError(
            "YOLO inference will be integrated during prototype phase"
        )
