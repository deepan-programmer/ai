# RTSP AI Detection System

## Overview
This AI detection system has been enhanced to work with RTSP (Real Time Streaming Protocol) streams for real-time video analysis and idle person detection. The system provides comprehensive logging and robust error handling for RTSP connections.

## Features

### RTSP Capabilities
- **Real-time RTSP stream processing** with automatic reconnection
- **Optimized for low latency** with configurable buffer sizes
- **Robust error handling** with configurable retry attempts
- **Stream health monitoring** with periodic status logging
- **Automatic fallback** to webcam if RTSP fails

### Enhanced Logging
- **Detailed RTSP connection logs** with connection status and stream properties
- **Real-time detection logging** with person tracking and idle detection alerts
- **Performance monitoring** with FPS and frame processing statistics
- **Error tracking** with detailed exception information
- **Periodic status reports** every 30 seconds

## Configuration

### RTSP Settings in `assets/config.mk`
```json
{
  "mode": "rtsp",
  "rtsp_link": "rtsp://admin:admin123@192.168.1.111:554//Streaming//Channel//101",
  "rtsp_reconnect_attempts": 5,
  "rtsp_reconnect_delay": 2.0,
  "rtsp_buffer_size": 1,
  "rtsp_timeout": 30,
  "log_file_path": "assets/rtsp_detection.log"
}
```

### Configuration Parameters
- **`mode`**: Set to "rtsp" to enable RTSP mode
- **`rtsp_link`**: RTSP stream URL
- **`rtsp_reconnect_attempts`**: Maximum number of reconnection attempts (default: 5)
- **`rtsp_reconnect_delay`**: Delay between reconnection attempts in seconds (default: 2.0)
- **`rtsp_buffer_size`**: Frame buffer size for low latency (default: 1)
- **`rtsp_timeout`**: Stream timeout in seconds (default: 30)

## Usage

### Running the System
```bash
python main.py
```

### Testing RTSP Connection
```bash
python test_rtsp.py
```

## Log Output Examples

### System Startup
```
2024-06-29 10:30:00,123 - INFO - [main:62] - ================================================================================
2024-06-29 10:30:00,124 - INFO - [main:63] - RTSP AI Detection System Starting
2024-06-29 10:30:00,125 - INFO - [main:64] - Project: RTSP AI Detection System
2024-06-29 10:30:00,126 - INFO - [main:65] - Author: Prakash pacharne
2024-06-29 10:30:00,127 - INFO - [main:66] - Mode: rtsp
2024-06-29 10:30:00,128 - INFO - [main:67] - RTSP URL: rtsp://admin:admin123@192.168.1.111:554//Streaming//Channel//101
```

### RTSP Connection
```
2024-06-29 10:30:00,150 - INFO - [videocaptureclass:58] - Attempting to connect to RTSP stream: rtsp://admin:admin123@192.168.1.111:554//Streaming//Channel//101
2024-06-29 10:30:02,234 - INFO - [videocaptureclass:65] - RTSP connection established successfully
2024-06-29 10:30:02,235 - INFO - [videocaptureclass:71] - Stream properties - FPS: 25.0, Resolution: 1920x1080
```

### Detection Alerts
```
2024-06-29 10:30:15,789 - WARNING - [main:420] - IDLE PERSON DETECTED - ID: 1, Position: (320, 240), Idle time: 12.5s, Frame: 375
```

### Status Monitoring
```
2024-06-29 10:30:35,456 - INFO - [main:251] - RTSP Status - Active: True, Frames processed: 825
2024-06-29 10:30:35,457 - INFO - [main:253] - Stream Info - FPS: 25.0, Resolution: 1920x1080, Reconnects: 0
```

## File Structure
```
ai/
├── main.py                     # Main application with RTSP support
├── test_rtsp.py               # RTSP testing script
├── assets/
│   ├── config.mk              # Configuration file
│   ├── config_reader.py       # Configuration reader
│   ├── videocaptureclass.py   # Enhanced RTSP VideoCapture class
│   ├── rtsp_detection.log     # Main log file
│   ├── rtsp_test.log          # Test log file
│   ├── sample_rtsp_operation.log # Sample log output
│   ├── yolov9t.onnx          # YOLO model (ONNX format)
│   ├── yolov9t.pt            # YOLO model (PyTorch format)
│   └── roi_points.txt         # Region of Interest points
└── requirements.txt           # Python dependencies
```

## Key Improvements

### Enhanced VideoCapture Class
- **Threaded frame reading** for better performance
- **Automatic reconnection** with exponential backoff
- **Stream health monitoring** with timeout detection
- **Low-latency buffering** with configurable queue size
- **Detailed error logging** for troubleshooting

### Robust Error Handling
- **Connection failure recovery** with automatic retry
- **Frame loss detection** and logging
- **Graceful degradation** with fallback options
- **Resource cleanup** on shutdown

### Comprehensive Logging
- **Structured log format** with timestamps and function names
- **Multiple log levels** (INFO, WARNING, ERROR, CRITICAL)
- **Performance metrics** tracking
- **Real-time status updates**

## Troubleshooting

### Common Issues
1. **RTSP Connection Failed**: Check network connectivity and RTSP URL
2. **Authentication Error**: Verify username and password in RTSP URL
3. **Stream Timeout**: Increase `rtsp_timeout` value in configuration
4. **High Latency**: Reduce `rtsp_buffer_size` to 1 for lowest latency

### Log Analysis
- Check `assets/rtsp_detection.log` for detailed operation logs
- Look for WARNING and ERROR messages for issues
- Monitor reconnection attempts and stream status

## Dependencies
- OpenCV (cv2) for video processing
- Ultralytics YOLO for object detection
- NumPy for array operations
- Threading and Queue for concurrent processing

## Performance Optimization
- Use ONNX model format for faster inference
- Set appropriate buffer size for your network conditions
- Monitor log files for performance bottlenecks
- Adjust detection parameters based on your use case