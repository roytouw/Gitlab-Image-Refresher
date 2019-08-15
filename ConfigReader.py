import json


class ConfigReader:
    def __init__(self):
        with open('config.json', 'r') as config:
            try:
                self.data = json.load(config)
            except json.JSONDecodeError as error:
                raise error
            config.close()

    def get_data(self):
        return self.data

    def get_config(self):
        return self.data['config']

    def get_interval(self):
        return self.data['config']['interval']

    def get_registries(self):
        return self.data['registries']


if __name__ == "__main__":
    configReader = ConfigReader()
    print(configReader.get_interval())

    # print(get_image_info())


