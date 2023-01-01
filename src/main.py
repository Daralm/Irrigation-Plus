from devices import Valve, Device, Controller, Status
import yaml
import argparse
from utils import get_logger


logger = get_logger(__name__)


def parse_config(config_path: str) -> dict:
    with open(config_path, 'r') as f:
        conf = yaml.safe_load(f)
    logger.info(f'Successfully parsed the config file {config_path}')
    return conf


def create_device(config: dict):
    valves: list[Valve] = []
    for item in config:
        valve = Valve(valve_id=item.get('unique_id'), zone=item.get('zone'),
                      qos=item.get('qos'), gpio_pin=int(item.get('gpio_pin')))
        valves.append(valve)

    device = Device()
    device.add_valves(valves=valves)

    logger.info(f'Successfully created the device with valves: {device.valves}')

    return device


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('config_file_path', help='Path to config file')
    args = argument_parser.parse_args()
    # config_file_path = './config/config.yaml'
    config_file_path = args.config_file_path

    config = parse_config(config_path=config_file_path)
    device = create_device(config)
    controller = Controller(device=device)

    controller.listen('192.168.2.10', 1883)
    controller.report_status('192.168.2.10', 1883)

    # controller.listen('darameybodi.asuscomm.com', 1883)
    # controller.report_status('darameybodi.asuscomm.com', 1883)


if __name__ == '__main__':
    main()
