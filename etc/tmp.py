# import json
# with open("etc/data.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# output = dict()

# for key, site in data["sitematrix"].items():
#     try:
#         for s in site["site"]:
#             if s["sitename"] == "Wikipedia" and not "closed" in s:
#                 output[site["name"]] = site["code"]
#     except:
#         continue

# with open("etc/wikis_list.json", "w", encoding="utf-8") as o:
#     json.dump(output, o)