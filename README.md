# Sensor-Fusion Based Road Damage Detection System

## Problem Context
Manual road inspections are infrequent, subjective, and expensive, allowing small surface defects to evolve into hazardous potholes before timely intervention.

This project focuses on continuous, objective road-condition assessment using vehicles already operating on city roads.

## System Overview
The system integrates computer vision, laser depth sensing, and edge computing to detect, assess, and prioritize road damage under real-world driving conditions, with minimal additional infrastructure.

## Architecture & Design Rationale
- Dashcams provide wide-field coverage across full road lanes.
- Edge AI performs real-time detection to avoid cloud dependency.
- A Laser Time-of-Flight sensor (VL53L1X) provides quantitative depth and surface profiling where vision alone is unreliable.
- Sensor fusion enables severity estimation rather than binary detection.
- GPS data is sourced from the dashcam when available; otherwise, a dedicated GPS module within the pothole unit is used for geo-tagging.
- Fleet-based deployment allows easy integration with existing government vehicles.

## Edge-First Processing
All perception and fusion logic runs locally on the vehicle to ensure:
- Low-latency operation
- Reduced bandwidth usage
- Robustness in low-connectivity environments

Only validated, low-volume metadata is transmitted for centralized road condition mapping.

## Optional Preventive Extension
For low-speed municipal vehicles (e.g., garbage trucks), the system can optionally flag eligible micro-cracks (<1 cm) for automated preventive sealing to limit water ingress and delay pothole formation.

This extension is intentionally constrained and rule-based to ensure safety, feasibility, and regulatory compatibility.

## Scope & Limitations
This repository demonstrates system logic and architectural feasibility.
Regulatory approvals are outside the current scope.

## References
- YOLO-based road damage detection and segmentation adapted from public research and Kaggle implementations.
