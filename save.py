import csv

def save_to_file(company_name, jobs):
  file = open(f"{company_name}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["place", "title", "time", "pay", "date"])
  for job in jobs:
    writer.writerow(list(job.values()))
  print(file)
  return