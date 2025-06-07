# Billboard Hot 100 Artist Ranking Analyzer (MapReduce)

This project implements a MapReduce job to analyze the Billboard Hot 100 dataset (1940-2023, ~330,000 rows). The task counts the number of chart entries per artist and computes their average peak chart position, grouped by year. The project uses Hadoop Streaming with Python scripts and was executed on a single-node Hadoop setup on Ubuntu.

---

## Registration Numbers
```bash
EG/2020/4092 - Nehara S.A.T
EG/2020/4095 - Nethsara R.A.A
EG/2020/4097 - Nettasinghe N.A.O.D
```

## Dataset Used

**Source**: [Kaggle - Billboard Hot 100 Songs](https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs)

**Columns:**
- `date`: Week of chart entry (e.g., 2015-08-01)
- `rank`: Rank that week (1 = best)
- `song`: Song name
- `artist`: Artist name
- `last-week`: Rank last week
- `peak-rank`: Best rank ever reached
- `weeks-on-board`: Total weeks on chart

---

## How It Works

This MapReduce job calculates:

1. **How many times each artist appeared on the chart in a given year**
2. **The average of their peak ranks for that year** (lower average = better performance)

---

## Prerequisites
- **Environment**: Linux (Ubuntu) with Hadoop 3.3.6 and Python 3 installed
- **Hadoop Services**: NameNode, DataNode, SecondaryNameNode, ResourceManager, NodeManager
- **Dependencies**: Python `csv` module (standard library)
- **Files**:
  - `mapper.py`: Maps chart entries to artist-year key with peak position and count
  - `reducer.py`: Aggregates counts and computes average peak position
  - `data/charts_sample.csv`: Sample dataset
  - `data/2025_songs.csv`: 2025 data
  - `results.csv`: MapReduce output
  - `results_summary.txt`: Results interpretation
  - `screenshots/`: Execution evidence

## Setup
1. **Install Dependencies** (if not already installed):
   ```bash
   sudo apt update
   sudo apt install python3

2. **Start Hadoop Services**
   ```bash
   start-dfs.sh
   start-yarn.sh
   jps
  - Expected jps output: NameNode, DataNode, SecondaryNameNode, ResourceManager, NodeManager
    
3. **Upload Dataset to HDFS**
   ```bash
    hdfs dfs -mkdir -p /user/hadoop/billboard
    hdfs dfs -put data/charts.csv /user/hadoop/billboard/

  - Note: Use full charts.csv (Kaggle, with appended 2025 data) for actual runs; charts_sample.csv is for reference.

4. **Prepare Scripts**
  - Save mapper.py and reducer.py in /home/ashen/hadoop_project/
  - Make executable:
    ```bash
    chmod +x /home/ashen/hadoop_project/mapper.py /home/ashen/hadoop_project/reducer.py

## Running the MapReduce Job
1. Clear Previous Output (if any)
   ```bash
   hdfs dfs -rm -r /user/hadoop/billboard/output

2. Execute Job
   ```bash
   hadoop jar /home/ashen/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
   -D mapreduce.job.name="BillboardAnalysis" \
   -input /user/hadoop/billboard/charts.csv \
   -output /user/hadoop/billboard/output \
   -mapper "python3 /home/ashen/hadoop_project/mapper.py" \
   -reducer "python3 /home/ashen/hadoop_project/reducer.py" \
   -file /home/ashen/hadoop_project/mapper.py \
   -file /home/ashen/hadoop_project/reducer.py

3. Retrieve Results
   ```bash
   hdfs dfs -cat /user/hadoop/billboard/output/part-00000 > /home/ashen/hadoop_project/results.csv

4. Test Locally
   ```bash
   head -n 1000 /home/ashen/hadoop_project/data/charts.csv | python3 /home/ashen/hadoop_project/mapper.py | sort | python3 /home/ashen/hadoop_project/reducer.py > /home/ashen/hadoop_project/test_output.txt

## Output
- Format: artist,year,chart_entries,avg_peak_position
- Example
  ```csv
  ROSÉ and Bruno Mars,2025,2,6.50
  Chappell Roan,2025,3,4.00
  The Beatles,1965,10,3.20

- Explanation:
    - artist: Name of the artist
    - year: Chart year
    - chart_entries: Number of times the artist appeared on the Billboard Hot 100 that year
    - avg_peak_position: Average peak chart position (lower is better, e.g., 1 = #1)
