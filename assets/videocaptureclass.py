import sys
sys.dont_write_bytecode = True

import threading
import queue
import cv2
import time
import logging

class VideoCapture:
    def __init__(self, camera_link, max_reconnect_attempts=5, reconnect_delay=2.0, buffer_size=1, timeout=30):
        self.camera_link = camera_link
        self.max_reconnect_attempts = max_reconnect_attempts
        self.reconnect_delay = reconnect_delay
        self.buffer_size = buffer_size
        self.timeout = timeout
        self.reconnect_count = 0
        self.is_connected = False
        self.last_frame_time = time.time()
        
        # Initialize video capture with RTSP optimizations
        self.cap = cv2.VideoCapture()
        self._configure_rtsp_settings()
        self._connect()
        
        # Frame queue with limited size to prevent memory buildup
        self.q = queue.Queue(maxsize=self.buffer_size)
        
        # Start reader thread
        self.reader_thread = threading.Thread(target=self._reader)
        self.reader_thread.daemon = True
        self.reader_thread.start()
        
        logging.info(f"RTSP VideoCapture initialized for: {camera_link}")

    def _configure_rtsp_settings(self):
        """Configure OpenCV settings optimized for RTSP streams"""
        try:
            # Set buffer size to minimize latency
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, self.buffer_size)
            
            # Set timeout for RTSP connection
            self.cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, self.timeout * 1000)
            
            # Enable TCP transport for more reliable connection
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))
            
            logging.info("RTSP settings configured successfully")
        except Exception as e:
            logging.warning(f"Could not configure all RTSP settings: {e}")

    def _connect(self):
        """Establish connection to RTSP stream"""
        try:
            if self.cap.isOpened():
                self.cap.release()
            
            logging.info(f"Attempting to connect to RTSP stream: {self.camera_link}")
            success = self.cap.open(self.camera_link)
            
            if success:
                self.is_connected = True
                self.reconnect_count = 0
                self.last_frame_time = time.time()
                logging.info("RTSP connection established successfully")
                
                # Log stream properties
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                logging.info(f"Stream properties - FPS: {fps}, Resolution: {width}x{height}")
            else:
                self.is_connected = False
                logging.error("Failed to establish RTSP connection")
                
            return success
        except Exception as e:
            logging.error(f"Exception during RTSP connection: {e}")
            self.is_connected = False
            return False

    def _reconnect(self):
        """Attempt to reconnect to RTSP stream"""
        if self.reconnect_count >= self.max_reconnect_attempts:
            logging.error(f"Maximum reconnection attempts ({self.max_reconnect_attempts}) reached")
            return False
        
        self.reconnect_count += 1
        logging.warning(f"RTSP reconnection attempt {self.reconnect_count}/{self.max_reconnect_attempts}")
        
        time.sleep(self.reconnect_delay)
        return self._connect()

    def _reader(self):
        """Background thread for reading frames from RTSP stream"""
        consecutive_failures = 0
        max_consecutive_failures = 10
        
        while True:
            try:
                if not self.is_connected:
                    if not self._reconnect():
                        time.sleep(self.reconnect_delay)
                        continue
                
                ret, frame = self.cap.read()
                
                if ret and frame is not None:
                    consecutive_failures = 0
                    self.last_frame_time = time.time()
                    
                    # Clear old frames to maintain low latency
                    while not self.q.empty():
                        try:
                            self.q.get_nowait()
                        except queue.Empty:
                            break
                    
                    # Add new frame
                    try:
                        self.q.put(frame, timeout=0.1)
                    except queue.Full:
                        logging.warning("Frame queue full, dropping frame")
                        
                else:
                    consecutive_failures += 1
                    logging.warning(f"Failed to read frame (consecutive failures: {consecutive_failures})")
                    
                    if consecutive_failures >= max_consecutive_failures:
                        logging.error("Too many consecutive frame read failures, attempting reconnection")
                        self.is_connected = False
                        consecutive_failures = 0
                    
                    time.sleep(0.1)
                    
            except Exception as e:
                logging.error(f"Exception in RTSP reader thread: {e}")
                self.is_connected = False
                time.sleep(self.reconnect_delay)

    def read(self):
        """Read the latest frame from the RTSP stream"""
        try:
            # Check for timeout
            current_time = time.time()
            if current_time - self.last_frame_time > self.timeout:
                logging.warning("RTSP stream timeout detected")
                self.is_connected = False
                return None
            
            # Get frame with timeout
            frame = self.q.get(timeout=5.0)
            return frame
            
        except queue.Empty:
            logging.warning("No frames available in queue")
            return None
        except Exception as e:
            logging.error(f"Error getting frame from RTSP queue: {e}")
            return None

    def is_stream_active(self):
        """Check if RTSP stream is active and receiving frames"""
        current_time = time.time()
        return self.is_connected and (current_time - self.last_frame_time) < self.timeout

    def get_stream_info(self):
        """Get information about the RTSP stream"""
        if not self.is_connected:
            return None
        
        try:
            info = {
                'fps': self.cap.get(cv2.CAP_PROP_FPS),
                'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'reconnect_count': self.reconnect_count,
                'last_frame_time': self.last_frame_time,
                'is_connected': self.is_connected
            }
            return info
        except Exception as e:
            logging.error(f"Error getting stream info: {e}")
            return None

    def release(self):
        """Release the RTSP stream and cleanup resources"""
        try:
            logging.info("Releasing RTSP stream resources")
            self.is_connected = False
            if self.cap.isOpened():
                self.cap.release()
        except Exception as e:
            logging.error(f"Error releasing RTSP resources: {e}")