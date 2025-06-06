#!/usr/bin/env python3
import sys
import csv

for line in sys.stdin:
    try:
        row = next(csv.reader([line]))
        date, rank, song, artist, last_week, peak_position, weeks = row[:7]
        if artist and peak_position and date:
            year = date.split('-')[0]
            artist_year = f"{artist}_{year}"
            print(f"{artist_year}\t{peak_position}\t1")
    except:
        continue

