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
    stat: Status = Status.OFF

    @property
    def id(self):
        return self.valve_id

    @property
    def status(self):
        return self.stat

    @property
    def topic(self):
        return 'valve_' + str(self.valve_id)

    def set_status(self, stat: Status) -> None:
        """
            Set the status of the valve.
            Call the set status method on the GPIO
        """

        # Call GPIO set status function here

        # set the status
        self.stat = stat

        logger.info(f'Successfully changes the status of valve {self.id} to {self.stat}')
        return

    def toggle_status(self):
        if self.stat == Status.OFF:
            self.set_status(Status.ON)
        else:
            self.set_status(Status.OFF)


class Device:
    def __init__(self):
        self.valves: dict[str: Valve] = {}

    def __str__(self):
        return f'Device:\n{self.valves}'

    def add_valves(self, valves: list[Valve]) -> None:
        self.valves = {valve.valve_id: valve for valve in valves}
        return

    def drop_valve(self, valve_id: str) -> None:
        self.valves.pop(valve_id, default=None)
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
        topics = self.device.topics
        client = Client(client_id='listener', clean_session=True)
        client.connect(host=host, port=port)
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        client.subscribe(topics)

        client.loop_start()
        return

    def report_status(self, host: str, port: int) -> None:
        client = Client(client_id='publisher', clean_session=True)
        client.connect(host=host, port=port)
        while True:
            for valve in self.device.valves.values():
                client.publish(topic=valve.topic+'/status', payload=valve.status.name)
            time.sleep(.5)
        return

    def _on_connect(self, client, userdata, flags, rc) -> None:
        print("Connected with result code "+str(rc))
        return

    def _on_message(self, client, userdata, msg) -> None:
        logger.info(
            f'Messgae received. Topic: {msg.topic}, payload: {msg.payload}')

        status = msg.payload.decode('utf-8')
        if status == 'ON':
            status = Status.ON
        else:
            status = Status.OFF

        self.device.set_valve_status(valve_id=int(msg.topic.split('_')[-1]), status=status)

        return
