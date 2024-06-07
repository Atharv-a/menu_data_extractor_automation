def individual_serial(data) -> dict:
    return{
        "id": str(data["_id"]),
        "name": data["name"],
        "menu_list": data["menu_list"]
    }

def list_serial(datalist) ->list:
    return [individual_serial(data) for data in datalist]