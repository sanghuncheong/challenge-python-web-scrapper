import csv

def save_to_file(jobs, job_name):
    print(f"SAVE TO FILE: {job_name}.csv")
    file_name = job_name+".csv"
    file = open(f"{job_name}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "link"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return