from create_weather_info import feature_weather
from settings import DataSettings


def main():
    print(feature_weather(data=DataSettings(), city='Moscow'))


if __name__ == '__main__':
    main()
