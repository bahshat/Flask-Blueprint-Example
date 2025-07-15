# Convert rows to a list of dictionaries
def add_column_names(rows):
    metrics = []
    
    for row in rows:
        metrics.append({
            "timestamp": row[0],
            "cpuUsage": row[1],
            "cpuTemp": row[2],
            "memUsed": row[3],
            "nwStatSent": row[4],
            "nwStatRecv": row[5]
        })

    return metrics