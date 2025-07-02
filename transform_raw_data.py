import decimal

def to_str(raw_item):
    if '_id' in raw_item:
        raw_item['_id'] = str(raw_item['_id'])
    return raw_item

def clean(raw_item):
    if isinstance(raw_item, float):
        return decimal.Decimal(str(raw_item))
    
    elif isinstance(raw_item, list):
        cleaned_list = []
        for i in raw_item:
            cleaned_list.append(clean(i))
        return cleaned_list

    elif isinstance(raw_item, dict):
        cleaned_dict = {}
        for k, v in raw_item.items():
            cleaned_dict[k] = clean(v)
        return cleaned_dict

    else:
        return raw_item
