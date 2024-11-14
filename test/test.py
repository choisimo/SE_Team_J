import unittest
from car import Car
from car_controller import CarController
from main import execute_command_callback

class TestExecuteCommandCallback(unittest.TestCase):

    def setUp(self):
        """각 테스트 전에 Car 및 CarController 객체를 초기화"""
        self.car = Car()
        self.car_controller = CarController(self.car)

    def test_engine_btn_command(self):
        """ENGINE_BTN 커맨드 테스트"""
        # 초기 상태는 엔진 OFF이므로, 버튼을 누르면 ON으로 변경되어야 함
        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.assertTrue(self.car.engine_on)

        # 속도가 0이 아닐 경우 엔진을 끌 수 없어야 함
        self.car.accelerate()
        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.assertTrue(self.car.engine_on)  # 엔진이 계속 ON 상태여야 함

    def test_accelerate_command(self):
        """ACCELERATE 커맨드 테스트"""
        self.car.toggle_engine()  # 엔진 ON
        execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car.speed, 10)

        # 도어나 트렁크가 열려 있을 경우 가속이 되지 않아야 함
        self.car.open_left_door()
        execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car.speed, 10)  # 속도는 그대로 유지

    def test_brake_command(self):
        """BRAKE 커맨드 테스트"""
        self.car.toggle_engine()  # 엔진 ON
        self.car.accelerate()
        execute_command_callback("BRAKE", self.car_controller)
        self.assertEqual(self.car.speed, 0)

        # 엔진이 OFF일 경우 브레이크가 작동하지 않아야 함
        self.car.toggle_engine()  # 엔진 OFF
        execute_command_callback("BRAKE", self.car_controller)
        self.assertEqual(self.car.speed, 0)  # 속도는 그대로 유지

    def test_lock_unlock_commands(self):
        """LOCK 및 UNLOCK 커맨드 테스트"""
        execute_command_callback("LOCK", self.car_controller)
        self.assertTrue(self.car.lock)
        self.assertEqual(self.car.left_door_lock, "LOCKED")
        self.assertEqual(self.car.right_door_lock, "LOCKED")

        execute_command_callback("UNLOCK", self.car_controller)
        self.assertFalse(self.car.lock)
        self.assertEqual(self.car.left_door_lock, "UNLOCKED")
        self.assertEqual(self.car.right_door_lock, "UNLOCKED")

    def test_left_door_commands(self):
        """LEFT_DOOR 관련 커맨드 테스트"""
        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("LEFT_DOOR_UNLOCK", self.car_controller)
        self.assertEqual(self.car.left_door_lock, "UNLOCKED")

        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car.left_door_status, "OPEN")

        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car.left_door_status, "CLOSED")

        execute_command_callback("LEFT_DOOR_LOCK", self.car_controller)
        self.assertEqual(self.car.left_door_lock, "LOCKED")

    def test_right_door_commands(self):
        """RIGHT_DOOR 관련 커맨드 테스트"""
        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("RIGHT_DOOR_UNLOCK", self.car_controller)
        self.assertEqual(self.car.right_door_lock, "UNLOCKED")

        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car.right_door_status, "OPEN")

        execute_command_callback("RIGHT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car.right_door_status, "CLOSED")

        execute_command_callback("RIGHT_DOOR_LOCK", self.car_controller)
        self.assertEqual(self.car.right_door_lock, "LOCKED")

    def test_trunk_commands(self):
        """TRUNK 관련 커맨드 테스트"""
        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("TRUNK_OPEN", self.car_controller)
        self.assertFalse(self.car.trunk_status)  # 트렁크가 열려 있어야 함

        execute_command_callback("TRUNK_CLOSE", self.car_controller)
        self.assertTrue(self.car.trunk_status)  # 트렁크가 닫혀 있어야 함

    def test_sos_command(self):
        """SOS 커맨드 테스트"""
        self.car.toggle_engine()
        self.car.accelerate()
        self.car.accelerate()
        self.assertEqual(self.car.speed, 20)  # 속도가 20이어야 함

        execute_command_callback("SOS", self.car_controller)
        self.assertEqual(self.car.speed, 0)  # 속도가 0이어야 함
        self.assertFalse(self.car.lock)  # 차량이 잠금 해제 상태여야 함
        self.assertFalse(self.car.trunk_status)  # 트렁크가 열려 있어야 함

if __name__ == '__main__':
    unittest.main()
