

def transform_data(document, index_name):
    
    transformed_document = document  # This is just a placeholder line
    
    if index_name == 'gares' :
        transformed_document = {
            "id": document["code_uic"],
            "libelle": document["libelle"],
            "commune": document["commune"],
            "departemen": document["departemen"],
            "geo_point_2d": {"lat": document["geo_point_2d"]["lat"], "lon": document["geo_point_2d"]["lon"]}
        }
        
    elif index_name == 'users' :
         transformed_document = {
            "id": document["id"],
            "name": "{} {}".format(document["firstname"], document["lastname"]),
            "username": document["login"]["username"],
            "birthDate": document["birthDate"],
            "address": "{}, {} {}\n{}".format(document["address"]["street"], document["address"]["zipcode"], document["address"]["city"],  document["address"]["suite"]),
            "geo_point_2d": {"lat": document["address"]["geo"]["lat"], "lon": document["address"]["geo"]["lng"]}
        }

    return transformed_document
