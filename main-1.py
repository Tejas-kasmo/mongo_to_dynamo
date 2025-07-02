import extract_from_mongo
import transform_raw_data
import load_to_dynamo 

cursor = extract_from_mongo.get_cursor()

i=0
sequence_token = None

for raw_data in cursor:
    object_removed = transform_raw_data.to_str(raw_item=raw_data)
    cleaned_raw_data = transform_raw_data.clean(raw_item=object_removed)
    load_to_dynamo.load(cleaned_raw_data)
    sequence_token = load_to_dynamo.update_log(message=f"index {i} row loaded to tickets table", seq_token=sequence_token)
    i+=1
