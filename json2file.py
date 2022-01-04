import json

data = {"blocks": [
    {
        "type": "section",
        "text": {
                "type": "mrkdwn",
                "text": "Danny Torrence left the following review for your property:"
        }
    },
    {
        "type": "section",
        "text": {
                "type": "mrkdwn",
                "text": "<https://example.com|Overlook Hotel> \n :star: \n Doors had too many axe holes, guest in room " +
                "237 was far too rowdy, whole place felt stuck in the 1920s."
        },
        "accessory": {
            "type": "image",
            "image_url": "https://images.pexels.com/photos/750319/pexels-photo-750319.jpeg",
            "alt_text": "Haunted hotel image"
        }
    },
    {
        "type": "section",
        "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Average Rating*\n1.0"
                }
        ]
    }
]
}


def dict_to_jsonfile(jsonfilepath: str, dict_type_json: dict) -> None:
    with open(jsonfilepath, 'w') as f:
        json.dump(dict_type_json, f, ensure_ascii=False)


dict_to_jsonfile('sample.json', data)
