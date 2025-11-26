import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
random.seed(42)

# --- Configuration ---
NUM_NORMAL = 2000
NUM_ATTACK = 60       # Increased slightly to ensure batches are even
BATCHES = 6           # We will have 6 bursts of 10 attacks each
START_TIME = datetime(2023, 11, 15, 0, 0, 0) # Start at midnight

# Attack Traffic (Batched)
attacks_per_batch = NUM_ATTACK // BATCHES
attacker_ips_pool = ['192.168.25.1', '192.168.99.99', '172.16.0.1', '45.22.11.9']
attacker_geo_locations = ['RU', 'CN', 'KP', 'Unknown']
attack_user_agents = ['python-requests/2.28', 'curl/7.68.0', 'Mozilla/5.0 (compatible; sqlmap/1.4.7)' , 'Nikto/2.1.6', 'masscan/1.0']

# --- Helpers ---
def generate_normal_traffic(timestamp):
    return {
        'timestamp': timestamp,
        'src_ip': fake.ipv4(),
        'user_agent': fake.chrome() if random.random() > 0.5 else fake.firefox(),
        'http_method': 'POST',
        'endpoint': '/login',
        'status_code': 200 if random.random() > 0.15 else 403,
        'response_bytes': random.randint(1500, 5000),
        'request_duration_ms': random.randint(100, 800),
        'geo_location': fake.country_code(),
        'label': 'Normal'
    }

def generate_attack_traffic(timestamp, ip, country_code):
    return {
        'timestamp': timestamp,
        'src_ip': ip,
        'user_agent': random.choice(attack_user_agents) if random.random() > 0.5 else fake.chrome(),
        'http_method': 'POST',
        'endpoint': '/login',
        'status_code': 403 if random.random() > 0.1 else 200,
        'response_bytes': random.randint(200, 500) if random.random() > 0.5 else random.randint(1500, 5000),
        'request_duration_ms': random.randint(5, 50) if random.random() > 0.5 else random.randint(100, 800),
        'geo_location': country_code,
        'label': 'Attack'
    }

# --- Generation ---
data_rows = []
current_time = START_TIME

# 1. Normal Traffic (Background Noise)
for _ in range(NUM_NORMAL):
    current_time += timedelta(seconds=random.randint(10, 300))
    data_rows.append(generate_normal_traffic(current_time))


for i in range(BATCHES):
    # Randomize start time of the batch within the 24h window
    batch_time_offset = random.randint(0, 86000) # Seconds in a day
    batch_start = START_TIME + timedelta(seconds=batch_time_offset)
    
    # Pick an IP for this batch
    batch_ip = random.choice(attacker_ips_pool)
    batch_geo = random.choice(attacker_geo_locations)
    
    for _ in range(attacks_per_batch):
        batch_start += timedelta(milliseconds=random.randint(10, 100))
        data_rows.append(generate_attack_traffic(batch_start, batch_ip, batch_geo))

# --- Finalize ---
df = pd.DataFrame(data_rows)
df = df.sort_values(by='timestamp').reset_index(drop=True)


print(f"Data Generated: {len(df)} rows.")
print(f"Attack Batches: {BATCHES}")
print(df['label'].value_counts())

# Check a sample attack batch
print("\nSample Attack Burst:")
print(df[df['label']=='Attack'].head(10))

df.to_csv('Labs/Lab2/dataset.csv', index=False)

print("File saved successfully as 'dataset.csv'")