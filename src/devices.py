from dataclasses import dataclass
from enum import Enum
from paho.mqtt.client import Client
import time
from utils import get_logger

logger = get_logger(__name__)


class Status(Enum):
    ON: bool = 'ON'
    OFF: bool = 'OFF'


@dataclass
class Valve:
    valve_id: int
    zone: str
    qos: int
    gpio_pin: int
    __stat: Status = Status('OFF')

    @property
    def id(self):
        return self.valve_id

    @property
    def status(self):
        return self.__stat

    @property
    def topic(self):
        return 'valve_' + str(self.valve_id)

    def set_status(self, status: Status) -> None:
        """
            Set the status of the valve.
            Call the set status method on the GPIO
        """

        # Call GPIO set status function here

        # set the status
        self.__stat = status

        logger.info(f'Successfully changes the status of valve {self.id} to {self.__stat}')
        return


class Device:
    def __init__(self):
        self.valves: dict[str: Valve] = {}

    def __str__(self):
        return f'Device:\n{self.valves}'

    def add_valves(self, valves: list[Valve]) -> None:
        if not self.valves:
            self.valves = {valve.valve_id: valve for valve in valves}
        else:
            self.valves.update({valve.valve_id: valve for valve in valves})
        return

    def drop_valve(self, valve_id: int) -> None:
        self.valves.pop(valve_id)
        return

    def get_valve_status(self, valve_id) -> Status:
        return self.valves.get(valve_id).status

    def set_valve_status(self, valve_id: str, status: Status) -> Status:
        self.valves[valve_id].set_status(status)
        return status

    @property
    def topics(self) -> list[str]:
        return [(valve.topic, valve.qos) for valve in self.valves.values()]

    @property
    def status(self) -> bool:
        """
            Returns the status ON if one or more valves are ON, otherwise returns OFF
        """
        raise NotImplementedError


class Controller:
    def __init__(self, device: Device) -> None:
        self.device = device

    def listen(self, host: str, port: int) -> None:

        client = Client(client_id='listener', clean_session=True)
        try:
            client.connect(host=host, port=port)
        except Exception as e:
            logger.error(e)
            raise e
        client.on_connect = self._on_connect
        client.on_message = self._on_message

        try:
            client.loop_start()
        except Exception as e:
            logger.error(e)
            raise e
        return

    def report_status(self, host: str, port: int) -> None:
        client = Client(client_id='publisher', clean_session=True)

        while True:
            if not client.is_connected():
                try:
                    client.connect(host=host, port=port)
                except Exception as e:
                    logger.error(e)

            for valve in self.device.valves.values():
                client.publish(topic=valve.topic+'/status', payload=valve.status.value)
            time.sleep(.5)
        return

    def _on_connect(self, client, userdata, flags, rc) -> None:
        logger.info("Connected with result code "+str(rc))
        topics = self.device.topics
        try:
            client.subscribe(topics)
            logger.info(f'Subscribed to: {topics}')
        except Exception as e:
            logger.error(e)
            raise e
        return

    def _on_message(self, client, userdata, msg) -> None:
        logger.info(f'Messgae received. Topic: {msg.topic}, payload: {msg.payload}')

        status = Status(msg.payload.decode('utf-8'))
        valve_id = int(msg.topic.split('_')[-1])
        self.device.set_valve_status(valve_id=valve_id, status=status)

        return
