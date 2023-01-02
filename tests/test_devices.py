import sys
sys.path.append('C:\\Users\\d852859\\OneDrive - Telstra\\My Documents\\IrrigationPlus\\')
sys.path.append('C:\\Users\\d852859\\OneDrive - Telstra\\My Documents\\IrrigationPlus\\src\\')
from unittest import TestCase, main
from src.devices import Valve, Device, Controller, Status


class TestValve(TestCase):
    def setUp(self):
        self.valve = Valve(valve_id=1, zone='zone1', qos=1, gpio_pin=23)

    def test_status_property(self):
        # Test the status property
        self.assertEqual(self.valve.status, Status.OFF)

    def test_set_status(self):
        # Test the set_status method
        self.valve.set_status(Status.ON)
        self.assertEqual(self.valve.status, Status.ON)
        self.valve.set_status(Status.OFF)
        self.assertEqual(self.valve.status, Status.OFF)


class TestDevice(TestCase):
    def setUp(self):
        # Create a mock Device object with a single valve
        valve = Valve(valve_id=1, zone='zone1', qos=1, gpio_pin=23)
        self.device = Device()
        self.device.add_valves([valve])

    def test_add_valves(self):
        # Test the add_valves method
        self.assertEqual(len(self.device.valves), 1)
        valve2 = Valve(valve_id=2, zone='zone2', qos=1, gpio_pin=24)
        self.device.add_valves([valve2])
        self.assertEqual(len(self.device.valves), 2)

    def test_drop_valve(self):
        # Test the drop_valve method
        self.device.drop_valve(1)
        self.assertEqual(len(self.device.valves), 0)
        # self.device.drop_valve(2)
        # self.assertEqual(len(self.device.valves), 0)

    def test_get_valve_status(self):
        # Test the get_valve_status method
        self.assertEqual(self.device.get_valve_status(1), Status.OFF)

    def test_set_valve_status(self):
        # Test the set_valve_status method
        self.device.set_valve_status(1, Status.ON)
        self.assertEqual(self.device.get_valve_status(1), Status.ON)
        self.device.set_valve_status(1, Status.OFF)
        self.assertEqual(self.device.get_valve_status(1), Status.OFF)

    def test_topics(self):
        # Test the topics property
        self.assertEqual(self.device.topics, [('valve_1', 1)])

    def test_status(self):
        # Test the status property
        ...


class TestController(TestCase):
    def setUp(self):
        # Create a mock Device object with a single valve
        valve = Valve(valve_id=1, zone='zone1', qos=1, gpio_pin=23)
        self.device = Device()
        self.device.add_valves([valve])
        self.controller = Controller(self.device)

    def test_listen(self):
        # Test the listen method
        # You can mock the MQTT client and its connect, subscribe, and loop_start methods to test this
        pass

    def test_report_status(self):
        # Test the report_status method
        # You can mock the MQTT client and its connect and publish methods to test this
        pass

    def test_on_connect(self):
        # Test the _on_connect method
        # You can mock the MQTT client and call the _on_connect method to test this
        pass

    def test_on_message(self):
        # Test the _on_message method
        # You can mock the MQTT client and its message object, and call the _on
        pass


if __name__ == '__main__':
    main()
