import json


def resImageJson(images):
    model_data = []
    for item in images:
        # delattr(item, 'video')
        item = {
            'id'    :   item.id,
            "name"  :   item.name,
            "date"  :   item.upload_date.strftime("%Y-%m-%d %H:%M:%S"),
            "type"  :   item.type,
            "url"   :   item.image.name
        }
        model_data.append(item)
    result = { "data": model_data }
    return model_data

