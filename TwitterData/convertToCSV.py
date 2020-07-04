import json
import csv


data_list = []
with open("coorChicago.json") as inputData:
    for line in inputData:
        data_list.append(json.loads(line.rstrip('\n')))
data_json = json.dumps(data_list, indent=4)
with open("coorChicago_new.json", "w") as outfile:
    outfile.write(data_json)


def get_leaves(item, key=None):
    if isinstance(item, dict):
        leaves = {}
        lat = 0.0
        lon = 0.0
        new_coordinates = []
        new_user = ""
        for i in item.keys():
            if i == "coordinates":
                if type(item[i]) == str:
                    point_dic = json.loads(item[i])
                else:
                    point_dic = item[i]
                new_coordinates = point_dic["coordinates"]
                lat = point_dic["coordinates"][1]
                lon = point_dic["coordinates"][0]
            if i == "user":
                if type(item[i]) == str:
                    user_dic = json.loads(item[i])
                else:
                    user_dic = item[i]
                new_user = user_dic["name"]
            if isinstance(item[i], dict):
                item[i] = json.dumps(item[i])
            temp = {i: item[i]}
            leaves.update(temp)
        temp_lat = {"lat": lat}
        # print(temp_lat)
        leaves.update(temp_lat)
        temp_lon = {"lon": lon}
        # print(temp_lon)
        leaves.update(temp_lon)
        temp_coordinates = {"coordinates": new_coordinates}
        leaves.update(temp_coordinates)
        temp_user = {"user": new_user}
        leaves.update(temp_user)
        # print(leaves)
        return leaves
    else:
        return {key: item}


with open("coorChicago_new.json") as json_file:
    new_data = json.load(json_file)

# First parse all entries to get the complete fieldname list
fieldnames = set()

for entry in new_data:
    fieldnames.update(get_leaves(entry).keys())
    # print(fieldnames)

with open('coorChicago.csv', 'w', newline='') as f_output:
    csv_output = csv.DictWriter(f_output, fieldnames=fieldnames)
    csv_output.writeheader()
    csv_output.writerows(get_leaves(entry) for entry in new_data)
