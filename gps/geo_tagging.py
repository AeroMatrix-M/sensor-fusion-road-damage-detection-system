"""
GPS geo-tagging module.

Provides location information for detected road damage.
Uses dashcam GPS when available, otherwise falls back
to a dedicated GPS module.
"""

def get_gps_location(mode="mock"):
    """
    Retrieve GPS coordinates.

    Args:
        mode: "mock" for development, "real" for hardware integration

    Returns:
        Dictionary containing latitude, longitude, and source
    """

    if mode == "mock":
        return {
            "latitude": 18.5204,
            "longitude": 73.8567,
            "source": "dashcam-gps"
        }

    elif mode == "real":
        # TODO: Integrate dashcam GPS or external GPS module
        raise NotImplementedError(
            "GPS hardware integration pending prototype phase"
        )
