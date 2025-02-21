# Script modified from the original found in Kaggle: https://www.kaggle.com/datasets/vishnu0399/server-logs?resource=download

#!/usr/bin/env python3
import argparse
import random
from datetime import datetime, timedelta
import numpy as np
from faker import Faker
import os
from pathlib import Path

# Initialize Faker
fake = Faker()

class LogGenerator:
    def __init__(self):
        # Define realistic endpoints with weights
        self.endpoints = {
            '/api/users': 0.2,
            '/api/products': 0.25,
            '/api/orders': 0.2,
            '/api/auth/login': 0.1,
            '/api/auth/logout': 0.05,
            '/api/cart': 0.1,
            '/api/search': 0.05,
            '/health': 0.03,
            '/metrics': 0.02
        }
        
        # Define HTTP methods with weights
        self.methods = {
            'GET': 0.6,
            'POST': 0.2,
            'PUT': 0.1,
            'DELETE': 0.1
        }
        
        # Define status codes with weights
        self.status_codes = {
            200: 0.75,  # Success
            201: 0.05,  # Created
            301: 0.02,  # Moved Permanently
            304: 0.03,  # Not Modified
            400: 0.05,  # Bad Request
            401: 0.03,  # Unauthorized
            403: 0.02,  # Forbidden
            404: 0.03,  # Not Found
            500: 0.02   # Internal Server Error
        }
        
        # User agents with browser share weights
        self.user_agents = {
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36': 0.4,
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15': 0.2,
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0': 0.15,
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1': 0.1,
            'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36': 0.1,
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59': 0.05
        }

    def weighted_choice(self, choices_dict):
        """Make a weighted random choice from a dictionary of choices and weights."""
        choices, weights = zip(*choices_dict.items())
        return random.choices(choices, weights=weights, k=1)[0]

    def generate_response_time(self):
        """Generate a realistic response time with long tail distribution."""
        # Use a lognormal distribution for response times
        # Parameters chosen to give mostly fast responses with occasional slow ones
        return int(np.random.lognormal(mean=3.0, sigma=1, size=1)[0])

    def generate_bytes_sent(self):
        """Generate realistic response sizes with different distributions per endpoint."""
        # Use different distributions for different types of responses
        distribution_type = random.random()
        
        if distribution_type < 0.7:  # Normal responses (e.g., API responses)
            return int(np.random.lognormal(8, 0.5))
        elif distribution_type < 0.9:  # Small responses (e.g., status checks)
            return int(np.random.normal(500, 100))
        else:  # Large responses (e.g., file downloads)
            return int(np.random.normal(500000, 100000))

    def generate_ip(self):
        """Generate IP addresses with some recurring ones to simulate real traffic."""
        if random.random() < 0.3:  # 30% chance of using a "regular visitor" IP
            return random.choice([
                "192.168.1.100",
                "10.0.0.50",
                "172.16.0.100",
                "192.168.0.200",
                "10.0.0.25"
            ])
        return fake.ipv4()

    def generate_log_entry(self, timestamp):
        """Generate a single log entry."""
        method = self.weighted_choice(self.methods)
        endpoint = self.weighted_choice(self.endpoints)
        status_code = self.weighted_choice(self.status_codes)
        
        # Generate referrer (30% chance of having a referrer)
        referrer = fake.uri() if random.random() < 0.3 else "-"
        
        return (
            f'{self.generate_ip()} - - '
            f'[{timestamp.strftime("%d/%b/%Y:%H:%M:%S")} +0000] '
            f'"{method} {endpoint} HTTP/1.1" '
            f'{status_code} {self.generate_bytes_sent()} '
            f'"{referrer}" "{self.weighted_choice(self.user_agents)}" '
            f'{self.generate_response_time()}\n'
        )

    def generate_logs(self, num_lines, output_file):
        """Generate the specified number of log entries."""
        # Create output directory if it doesn't exist
        output_dir = Path('sample_logs')
        output_dir.mkdir(exist_ok=True)
        
        # Calculate timestamps with realistic patterns
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)  # Generate last 7 days of logs
        
        timestamps = []
        # Create timestamps with higher frequency during business hours
        current_time = start_time
        while current_time < end_time:
            hour = current_time.hour
            # More frequent logs during business hours (8am-6pm)
            if 8 <= hour <= 18:
                num_entries = np.random.poisson(5)  # Average 5 entries per minute
            else:
                num_entries = np.random.poisson(1)  # Average 1 entry per minute
            
            for _ in range(num_entries):
                # Add some random seconds
                random_seconds = random.random() * 60
                timestamps.append(current_time + timedelta(seconds=random_seconds))
            
            current_time += timedelta(minutes=1)
        
        # Sort timestamps and take the required number
        timestamps.sort()
        if len(timestamps) > num_lines:
            timestamps = random.sample(timestamps, num_lines)
        timestamps.sort()  # Resort after sampling
        
        # Write log entries
        output_path = output_dir / output_file
        with open(output_path, 'w') as f:
            for timestamp in timestamps:
                f.write(self.generate_log_entry(timestamp))
        
        print(f"Generated {num_lines} log entries in {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate sample server log files')
    parser.add_argument('--lines', type=int, default=1000,
                      help='number of log entries to generate (default: 1000)')
    parser.add_argument('--output', type=str, default='server.log',
                      help='output file name (default: server.log)')
    
    args = parser.parse_args()
    
    generator = LogGenerator()
    generator.generate_logs(args.lines, args.output)

if __name__ == "__main__":
    main()