#!/usr/bin/env python3
"""
RTSP Test Script for AI Detection System
This script tests the RTSP functionality and generates sample log output
"""

import sys
sys.dont_write_bytecode = True

import cv2
import time
import logging
from assets.config_reader import config_reader
from assets.videocaptureclass import VideoCapture

def setup_logging():
    """Setup logging for the test"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.FileHandler('assets/rtsp_test.log', mode='w'),
            logging.StreamHandler()
        ]
    )

def test_rtsp_connection():
    """Test RTSP connection and log the results"""
    try:
        # Load configuration
        data = config_reader()
        rtsp_link = data['rtsp_link']
        
        logging.info("="*80)
        logging.info("RTSP Connection Test Starting")
        logging.info(f"Testing RTSP URL: {rtsp_link}")
        logging.info("="*80)
        
        # Test with enhanced VideoCapture class
        logging.info("Initializing enhanced RTSP VideoCapture...")
        cap = VideoCapture(
            rtsp_link,
            max_reconnect_attempts=3,
            reconnect_delay=1.0,
            buffer_size=1,
            timeout=10
        )
        
        # Test frame reading
        frame_count = 0
        test_duration = 30  # Test for 30 seconds
        start_time = time.time()
        
        logging.info(f"Starting frame capture test for {test_duration} seconds...")
        
        while time.time() - start_time < test_duration:
            frame = cap.read()
            
            if frame is not None:
                frame_count += 1
                if frame_count % 30 == 0:  # Log every 30 frames
                    logging.info(f"Successfully captured {frame_count} frames")
                    
                    # Get stream info
                    if hasattr(cap, 'get_stream_info'):
                        stream_info = cap.get_stream_info()
                        if stream_info:
                            logging.info(f"Stream Info - FPS: {stream_info.get('fps', 'N/A')}, "
                                       f"Resolution: {stream_info.get('width', 'N/A')}x{stream_info.get('height', 'N/A')}")
            else:
                logging.warning("Failed to capture frame")
                time.sleep(0.1)
        
        # Test results
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time if elapsed_time > 0 else 0
        
        logging.info("="*80)
        logging.info("RTSP Connection Test Results")
        logging.info(f"Test duration: {elapsed_time:.2f} seconds")
        logging.info(f"Total frames captured: {frame_count}")
        logging.info(f"Average FPS: {fps:.2f}")
        logging.info(f"Stream active: {cap.is_stream_active() if hasattr(cap, 'is_stream_active') else 'Unknown'}")
        
        # Cleanup
        cap.release()
        logging.info("RTSP test completed successfully")
        logging.info("="*80)
        
        return True
        
    except Exception as e:
        logging.error(f"RTSP test failed: {e}")
        return False

def test_fallback_to_webcam():
    """Test fallback to webcam if RTSP fails"""
    try:
        logging.info("Testing fallback to webcam...")
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                logging.info("Webcam fallback successful")
                cap.release()
                return True
            else:
                logging.warning("Webcam available but failed to read frame")
        else:
            logging.warning("No webcam available for fallback")
        
        cap.release()
        return False
        
    except Exception as e:
        logging.error(f"Webcam fallback test failed: {e}")
        return False

def generate_sample_log():
    """Generate a sample log file showing typical RTSP operation"""
    sample_log_path = 'assets/sample_rtsp_operation.log'
    
    with open(sample_log_path, 'w') as f:
        f.write("""2024-06-29 10:30:00,123 - INFO - [main:62] - ================================================================================
2024-06-29 10:30:00,124 - INFO - [main:63] - RTSP AI Detection System Starting
2024-06-29 10:30:00,125 - INFO - [main:64] - Project: RTSP AI Detection System
2024-06-29 10:30:00,126 - INFO - [main:65] - Author: Prakash pacharne
2024-06-29 10:30:00,127 - INFO - [main:66] - Mode: rtsp
2024-06-29 10:30:00,128 - INFO - [main:67] - RTSP URL: rtsp://admin:admin123@192.168.1.111:554//Streaming//Channel//101
2024-06-29 10:30:00,129 - INFO - [main:68] - Log file: assets/rtsp_detection.log
2024-06-29 10:30:00,130 - INFO - [main:69] - ================================================================================
2024-06-29 10:30:00,135 - INFO - [main:188] - Initializing RTSP connection with parameters:
2024-06-29 10:30:00,136 - INFO - [main:189] -   - URL: rtsp://admin:admin123@192.168.1.111:554//Streaming//Channel//101
2024-06-29 10:30:00,137 - INFO - [main:190] -   - Reconnect attempts: 5
2024-06-29 10:30:00,138 - INFO - [main:191] -   - Reconnect delay: 2.0s
2024-06-29 10:30:00,139 - INFO - [main:192] -   - Buffer size: 1
2024-06-29 10:30:00,140 - INFO - [main:193] -   - Timeout: 30s
2024-06-29 10:30:00,145 - INFO - [videocaptureclass:48] - RTSP settings configured successfully
2024-06-29 10:30:00,150 - INFO - [videocaptureclass:58] - Attempting to connect to RTSP stream: rtsp://admin:admin123@192.168.1.111:554//Streaming//Channel//101
2024-06-29 10:30:02,234 - INFO - [videocaptureclass:65] - RTSP connection established successfully
2024-06-29 10:30:02,235 - INFO - [videocaptureclass:71] - Stream properties - FPS: 25.0, Resolution: 1920x1080
2024-06-29 10:30:02,236 - INFO - [videocaptureclass:34] - RTSP VideoCapture initialized for: rtsp://admin:admin123@192.168.1.111:554//Streaming//Channel//101
2024-06-29 10:30:02,240 - INFO - [main:202] - RTSP VideoCapture initialized successfully
2024-06-29 10:30:02,245 - INFO - [main:218] - YOLO model loaded successfully from ONNX
2024-06-29 10:30:02,250 - INFO - [main:234] - Frame resizing enabled: 640x640
2024-06-29 10:30:02,251 - INFO - [main:235] - Frame normalization enabled: True
2024-06-29 10:30:02,252 - INFO - [main:236] - Starting main detection loop...
2024-06-29 10:30:05,123 - INFO - [main:251] - RTSP Status - Active: True, Frames processed: 75
2024-06-29 10:30:05,124 - INFO - [main:253] - Stream Info - FPS: 25.0, Resolution: 1920x1080, Reconnects: 0
2024-06-29 10:30:12,456 - INFO - [main:429] - Person 1 - Status: Moving, Position: (320, 240), Movement: 15.2px
2024-06-29 10:30:15,789 - WARNING - [main:420] - IDLE PERSON DETECTED - ID: 1, Position: (320, 240), Idle time: 12.5s, Frame: 375
2024-06-29 10:30:22,123 - INFO - [main:429] - Person 1 - Status: IDLE, Position: (322, 242), Movement: 2.1px
2024-06-29 10:30:35,456 - INFO - [main:251] - RTSP Status - Active: True, Frames processed: 825
2024-06-29 10:30:35,457 - INFO - [main:253] - Stream Info - FPS: 25.0, Resolution: 1920x1080, Reconnects: 0
2024-06-29 10:30:42,789 - INFO - [main:429] - Person 1 - Status: Moving, Position: (350, 260), Movement: 28.3px
2024-06-29 10:31:05,123 - INFO - [main:251] - RTSP Status - Active: True, Frames processed: 1575
2024-06-29 10:31:05,124 - INFO - [main:253] - Stream Info - FPS: 25.0, Resolution: 1920x1080, Reconnects: 0
2024-06-29 10:31:12,456 - INFO - [main:429] - Person 2 - Status: Moving, Position: (480, 360), Movement: 22.7px
2024-06-29 10:31:18,789 - WARNING - [main:420] - IDLE PERSON DETECTED - ID: 2, Position: (482, 362), Idle time: 11.2s, Frame: 1900
2024-06-29 10:31:35,123 - INFO - [main:251] - RTSP Status - Active: True, Frames processed: 2325
2024-06-29 10:31:35,124 - INFO - [main:253] - Stream Info - FPS: 25.0, Resolution: 1920x1080, Reconnects: 0
""")
    
    logging.info(f"Sample log file created: {sample_log_path}")

if __name__ == "__main__":
    setup_logging()
    
    logging.info("Starting RTSP functionality test...")
    
    # Test RTSP connection
    rtsp_success = test_rtsp_connection()
    
    # Test webcam fallback
    webcam_success = test_fallback_to_webcam()
    
    # Generate sample log
    generate_sample_log()
    
    # Summary
    logging.info("="*80)
    logging.info("Test Summary:")
    logging.info(f"RTSP Connection Test: {'PASSED' if rtsp_success else 'FAILED'}")
    logging.info(f"Webcam Fallback Test: {'PASSED' if webcam_success else 'FAILED'}")
    logging.info("Sample log files generated successfully")
    logging.info("="*80)