#!/usr/bin/env python3
import sys

current_key = None
total_count = 0
total_peak = 0

for line in sys.stdin:
    try:
        artist_year, peak_position, count = line.strip().split('\t')
        peak_position = float(peak_position)
        count = int(count)
        if current_key == artist_year:
            total_peak += peak_position
            total_count += count
        else:
            if current_key:
                artist, year = current_key.split('_')
                avg_peak = total_peak / total_count if total_count > 0 else 0
                print(f"{artist},{year},{total_count},{avg_peak:.2f}")
            current_key = artist_year
            total_peak = peak_position
            total_count = count
    except:
        continue

if current_key:
    artist, year = current_key.split('_')
    avg_peak = total_peak / total_count if total_count > 0 else 0
    print(f"{artist},{year},{total_count},{avg_peak:.2f}")
