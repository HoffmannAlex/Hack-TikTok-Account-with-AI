import time
import logging
import psutil
import threading
import asyncio
from datetime import datetime
from logging_config import setup_logger
from typing import Dict, Any

class OperationMonitor:
    """Monitors security testing operations and resource usage"""
    
    def __init__(self):
        self.logger = setup_logger('OperationMonitor')
        self.active = False
        self._lock = threading.Lock()
        self._task = None
        self.stats = {
            'requests_sent': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'last_request_time': None,
            'start_time': None,
            'cpu_usage': [],
            'memory_usage': [],
            'active_threads': 0
        }

    def start_monitoring(self):
        """Start monitoring operations"""
        self.active = True
        self.stats['start_time'] = datetime.now()
        self.logger.info("Security testing monitoring started")
        
        if asyncio.get_event_loop().is_running():
            self._task = asyncio.create_task(self._monitor_resources_async())
        else:
            threading.Thread(target=self._monitor_resources, daemon=True).start()

    def stop_monitoring(self):
        """Stop monitoring and generate report"""
        self.active = False
        self._generate_report()

    async def _monitor_resources_async(self):
        """Asynchronous resource monitoring"""
        while self.active:
            with self._lock:
                self.stats['cpu_usage'].append(psutil.cpu_percent())
                self.stats['memory_usage'].append(psutil.Process().memory_percent())
                self.stats['active_threads'] = threading.active_count()
            await asyncio.sleep(1)

    def _monitor_resources(self):
        """Synchronous resource monitoring"""
        while self.active:
            self.stats['cpu_usage'].append(psutil.cpu_percent())
            self.stats['memory_usage'].append(psutil.Process().memory_percent())
            self.stats['active_threads'] = threading.active_count()
            time.sleep(1)

    def log_request(self, success: bool):
        """Log request statistics"""
        self.stats['requests_sent'] += 1
        self.stats['last_request_time'] = datetime.now()
        if success:
            self.stats['successful_requests'] += 1
        else:
            self.stats['failed_requests'] += 1

    def get_current_status(self) -> dict:
        """Get current monitoring status"""
        if not self.stats['start_time']:
            return {"status": "Monitoring not started"}

        elapsed_time = (datetime.now() - self.stats['start_time']).seconds
        return {
            "running_time": elapsed_time,
            "requests_sent": self.stats['requests_sent'],
            "success_rate": (self.stats['successful_requests'] / max(1, self.stats['requests_sent'])) * 100,
            "active_threads": self.stats['active_threads'],
            "avg_cpu_usage": sum(self.stats['cpu_usage'][-10:]) / min(10, len(self.stats['cpu_usage'])),
            "avg_memory_usage": sum(self.stats['memory_usage'][-10:]) / min(10, len(self.stats['memory_usage']))
        }

    def verify_operation(self) -> bool:
        """Verify testing operation is running correctly"""
        current_status = self.get_current_status()
        
        if current_status.get("running_time", 0) > 0:
            if current_status["requests_sent"] == 0:
                self.logger.error("No security tests conducted!")
                return False
                
            if current_status["active_threads"] < 1:
                self.logger.error("No active testing threads!")
                return False

            if current_status["success_rate"] < 1:
                self.logger.warning("Low success rate detected")
                
        return True

    def log_error(self, error_type: str, details: str):
        """Log security testing errors"""
        if 'errors' not in self.stats:
            self.stats['errors'] = {}
            
        if error_type not in self.stats['errors']:
            self.stats['errors'][error_type] = []
            
        self.stats['errors'][error_type].append({
            'time': datetime.now(),
            'details': details
        })
        self.logger.error(f"{error_type}: {details}")

    def _generate_report(self):
        """Generate security testing report"""
        final_stats = self.get_current_status()
        report = ["Security Testing Report", "======================"]
        
        report.extend([
            f"Duration: {final_stats['running_time']} seconds",
            f"Total Tests: {self.stats['requests_sent']}",
            f"Successful Tests: {self.stats['successful_requests']}",
            f"Failed Tests: {self.stats['failed_requests']}",
            f"Success Rate: {final_stats['success_rate']:.2f}%",
            f"Average CPU Usage: {final_stats['avg_cpu_usage']:.2f}%",
            f"Average Memory Usage: {final_stats['avg_memory_usage']:.2f}%",
            f"Active Threads: {final_stats['active_threads']}"
        ])
        
        if 'errors' in self.stats and self.stats['errors']:
            report.extend(["", "Error Summary:", "-------------"])
            for error_type, errors in self.stats['errors'].items():
                report.append(f"{error_type}: {len(errors)} occurrences")
        
        report_text = "\n".join(report)
        self.logger.info(report_text)
        with open('security_testing_report.txt', 'w') as f:
            f.write(report_text)