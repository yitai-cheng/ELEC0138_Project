"using faker library generate a csv file with 20 emails and 20 names."
import csv
from faker import Faker

#Create instance of Faker
fake = Faker()

names = [fake.name() for x in range(20)]
emails = [fake.email() for x in range(20)]

#Create the csv file
with open('email_db.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name', 'email'])
    writer.writerow(['Rares Nitu','nitu.rares@yahoo.com'])
    writer.writerow(['Eden Eden','chooseyourtask@gmail.com'])
    for i in range(20):
        writer.writerow([names[i], emails[i]])

    