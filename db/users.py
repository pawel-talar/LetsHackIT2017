def register_user(redis_client, user_id, list_of_competitions):
    assert redis_client is not None
    assert type(user_id) == int and type(list_of_competitions) == list
    for c in list_of_competitions:
        redis_client.lpush(user_id, c)
