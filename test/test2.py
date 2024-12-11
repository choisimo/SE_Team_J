import unittest
from car import Car
from car_controller import CarController
from main import execute_command_callback


class TestCarEngineControlWithBrakeRequirement(unittest.TestCase):
    def setUp(self):
        """각 테스트 실행 전 호출되는 메서드"""
        self.car = Car()
        self.car_controller = CarController(self.car)
        print(f"\n[TEST START] {self._testMethodName} - {self.shortDescription()}")

    def tearDown(self):
        """각 테스트 실행 후 호출되는 메서드"""
        print(f"[TEST END] {self._testMethodName} - {self.shortDescription()}")

    def test_engine_starts_only_with_brake_on_same_line(self):
        """
        브레이크와 엔진 점화 버튼이 같은 줄에 올바른 순서로 입력된 경우에만 엔진이 켜져야 함.
        """
        # 초기 상태: 엔진 꺼짐
        self.assertFalse(self.car.engine_on, "초기 상태에서 엔진은 꺼져 있어야 함")

        # 올바른 순서로 같은 줄에 명령이 입력된 경우
        command = "BRAKE ENGINE_BTN"
        execute_command_callback(command, self.car_controller)

        # 엔진이 켜졌는지 확인
        self.assertTrue(self.car.engine_on, "브레이크와 점화 버튼이 같은 줄에서 올바른 순서로 실행되면 엔진이 켜져야 함")

    def test_engine_does_not_start_without_brake_on_same_line(self):
        """
        브레이크 없이 엔진 점화 버튼만 입력된 경우 엔진이 켜지지 않아야 함.
        """
        # 초기 상태: 엔진 꺼짐
        self.assertFalse(self.car.engine_on, "초기 상태에서 엔진은 꺼져 있어야 함")

        # 점화 버튼만 입력된 경우
        command = "ENGINE_BTN"
        execute_command_callback(command, self.car_controller)

        # 엔진이 켜지지 않았는지 확인
        self.assertFalse(self.car.engine_on, "브레이크 없이 같은 줄에서 점화 버튼만 입력된 경우 엔진이 켜지면 안 됨")

    def test_engine_does_not_start_with_incorrect_order_on_same_line(self):
        """
        같은 줄에서 점화 버튼이 먼저 입력되고 이후 브레이크가 입력된 경우 엔진이 켜지지 않아야 함.
        """
        # 점화 버튼이 먼저 실행된 경우
        command = "ENGINE_BTN BRAKE"
        execute_command_callback(command, self.car_controller)

        # 엔진이 켜지지 않았는지 확인
        self.assertFalse(self.car.engine_on, "점화 버튼이 먼저 실행된 경우 엔진이 켜지면 안 됨")

    def test_engine_starts_with_multiple_spaces_on_same_line(self):
        """
        브레이크와 엔진 점화 버튼이 같은 줄에 여러 공백으로 구분된 경우에도 올바른 순서로 실행되면 엔진이 켜져야 함.
        """
        # 여러 공백이 포함된 명령어
        command = "BRAKE     ENGINE_BTN"
        execute_command_callback(command, self.car_controller)

        # 엔진이 켜졌는지 확인
        self.assertTrue(self.car.engine_on, "여러 공백이 포함된 경우에도 올바른 순서로 실행되면 엔진이 켜져야 함")
    
    def test_speed_reduces_with_brake_and_engine_button(self):
        """
        엔진이 켜져 있고 속도가 0 이상인 상태에서 브레이크와 엔진 점화 버튼이 같은 줄에 올바른 순서로 입력되면 속도가 줄어야 함.
        """
        # 초기 상태: 엔진 켜고 가속
        execute_command_callback("BRAKE ENGINE_BTN", self.car_controller)  # 브레이크와 점화 버튼으로 엔진 켜기
        execute_command_callback("ACCELERATE", self.car_controller)  # 가속
        execute_command_callback("ACCELERATE", self.car_controller)  # 추가 가속
        self.assertEqual(self.car.speed, 20, "가속 후 속도는 20이어야 함")

        # 브레이크와 점화 버튼이 같은 줄에서 입력된 경우
        command = "BRAKE ENGINE_BTN"
        execute_command_callback(command, self.car_controller)

        # 속도가 줄어들었는지 확인
        self.assertLess(self.car.speed, 20, "브레이크와 점화 버튼이 입력되면 속도가 줄어야 함")



if __name__ == "__main__":
    unittest.main()
