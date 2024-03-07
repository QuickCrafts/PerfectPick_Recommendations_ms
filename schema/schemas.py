def individual_serial(recommendation) -> dict:
    return {
        "id": str(recommendation["_id"]),
        "id_user": str(recommendation["id_user"]),
        "movies": recommendation["movies"],
        "books": recommendation["books"],
        "songs": recommendation["songs"],
    }

def list_serial(recommendations) -> list:
    return [individual_serial(recommendation) for recommendation in recommendations]