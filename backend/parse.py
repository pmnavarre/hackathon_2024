import json


with open("./backend/assets/genres.json", "r") as f:
    genres = json.load(f)["genres"]
    output = {}
    for genre in genres:
        output[genre["name"]] = genre["id"]
    print(json.dumps(output, indent=4))
    with open("./backend/assets/genres.json", "w") as f:
        json.dump(output, f, indent=4)
