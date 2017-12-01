import telegram
import yaml

default_config_filename = 'config.yaml'


def get_bot(token):
    assert type(token) == str
    assert len(token) > 0
    return telegram.Bot(token)


def get_token_from_config(filename):
    token_field_name = 'token'
    config = None
    with open(filename, 'r') as f:
        config = yaml.load(f.read())
    assert config is not None
    assert token_field_name in config
    return config[token_field_name]


if __name__ == '__main__':
    token = get_token_from_config(default_config_filename)
    bot = get_bot(token)
    print(bot.get_me())