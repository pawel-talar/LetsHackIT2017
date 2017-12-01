import yaml


def get_redis_address_from_config(filename):
    redis_field_name = 'redis'
    with open(filename, 'r') as f:
        config = yaml.load(f.read())
    assert config is not None
    assert redis_field_name in config
    print(config[redis_field_name])
    return config[redis_field_name]


def get_token_from_config(filename):
    token_field_name = 'token'
    config = None
    with open(filename, 'r') as f:
        config = yaml.load(f.read())
    assert config is not None
    assert token_field_name in config
    return config[token_field_name]