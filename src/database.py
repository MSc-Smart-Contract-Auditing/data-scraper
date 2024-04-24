# WIP
# class Database:
#     def __init__(self, name):
#         self.file = open(name, "a")

#         fieldnames = [
#             "name",
#             "severity",
#             "type",
#             "function",
#             "description",
#             "recommendation",
#             "exploit_scenarios",
#         ]

#     def record(self, data):
#         self.file.write(data)

#     def close(self):
#         self.file.close()


# def record():

#     fieldnames = [
#         "name",
#         "severity",
#         "type",
#         "function",
#         "description",
#         "recommendation",
#         "exploit_scenarios",
#     ]
#     # Process each field to escape special characters
#     data = {
#         field: escape_special_chars(request.form.get(field, "")) for field in fieldnames
#     }

#     print(data)

#     file_exists = os.path.isfile("db.csv")

#     with open("db.csv", "a", newline="") as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect="mydialect")
#         if not file_exists:
#             writer.writeheader()
#         writer.writerow(data)
