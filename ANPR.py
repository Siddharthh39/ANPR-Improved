import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import db_config


# Connect to MySQL
conn = db_config.get_db_connection()
cursor = conn.cursor()

# Query Data
query = """
SELECT 
    t.weather_condition,
    AVG(t.processing_time) AS traditional_time,
    AVG(y.processing_time) AS yolo_time,
    SUM(t.false_positive) AS traditional_fp,
    SUM(y.false_positive) AS yolo_fp,
    SUM(t.false_negative) AS traditional_fn,
    SUM(y.false_negative) AS yolo_fn
FROM traditional_anpr t
JOIN yolo_v11_anpr y ON t.weather_condition = y.weather_condition
GROUP BY t.weather_condition;
"""
df = pd.read_sql(query, conn)

# Close connection
cursor.close()
conn.close()

# Create the figure and axis with styling similar to the Intel benchmark chart
plt.figure(figsize=(12, 6), facecolor='white')
ax = plt.gca()
ax.set_facecolor('white')

# Prepare data for plotting
x = np.arange(len(df['weather_condition']))
width = 0.4

# Create bars with colors resembling the Intel chart
traditional_bars = plt.bar(x - width/2, df['traditional_time'], width, color='#1E90FF', label='Traditional ANPR')
yolo_bars = plt.bar(x + width/2, df['yolo_time'], width, color='#FF6347', label='YOLO v11 ANPR')

# Add value labels on the bars
for i, (trad_bar, yolo_bar) in enumerate(zip(traditional_bars, yolo_bars)):
    # Traditional ANPR values
    plt.text(trad_bar.get_x() + trad_bar.get_width()/2, trad_bar.get_height(), 
             f'{trad_bar.get_height():.2f}', 
             ha='center', va='bottom', fontweight='bold', color='white')
    
    # YOLO ANPR values
    plt.text(yolo_bar.get_x() + yolo_bar.get_width()/2, yolo_bar.get_height(), 
             f'{yolo_bar.get_height():.2f}', 
             ha='center', va='bottom', fontweight='bold', color='white')

# Customize the plot to match the Intel chart style
plt.xlabel('Weather Condition', fontweight='bold')
plt.ylabel('Processing Time (s)', fontweight='bold')
plt.title('ANPR Performance Comparison', fontweight='bold')
plt.xticks(x, df['weather_condition'], rotation=45, ha='right')
plt.legend()

# Add grid and styling
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Show the plot
plt.show()