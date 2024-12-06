입력 예시파일 - example_fail, example_success

실행방법 - 입력파일을 프로젝트 path에 포함 후, 콘솔창에 파일 이름을 입력
# 테스트코드
```
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
```
# TDD 과정
## 1. 
브레이크와 엔진 점화 버튼이 같은 줄에서 실행될 때 엔진이 켜져야 함.
```
    """
    if command == "ENGINE_BTN":
        print("\n")
        print(f"Current engine status: {engine_status}")
        if car_speed == 0:
            car_controller.toggle_engine()
            engine_status = "ON" if car_controller.get_engine_status() else "OFF"
            print(f"Engine toggled to {engine_status}")
        else:
            print("[ERROR] Speed must be 0 to toggle engine.")
    """
    if command == "BRAKE ENGINE_BTN":
        print("\n")
        print(f"Executing combined command: BRAKE ENGINE_BTN")
        # 브레이크 적용 후 엔진 점화 처리
        car_controller.brake()
        if car_speed == 0:  # 차량 정지 상태 확인
            car_controller.toggle_engine()
            engine_status = "ON" if car_controller.get_engine_status() else "OFF"
            print(f"Engine toggled to {engine_status}")
        else:
            print("[ERROR] Speed must be 0 to toggle engine.")
```

## 2
브레이크 없이 엔진 점화 버튼만 있는 경우 엔진이 켜지지 않아야 함.
```
    if command == "ENGINE_BTN":
        print("\n")
        print(f"Current engine status: {engine_status}")
        if car_speed == 0 and engine_status == "ON" :
            car_controller.toggle_engine()
            engine_status = "OFF"
            print(f"Engine toggled to {engine_status}")
        else:
            print("[ERROR] Engine toggles only with brake applied.")
    
    elif command == "BRAKE ENGINE_BTN":
        print("\n")
        print(f"Executing combined command: BRAKE ENGINE_BTN")
        # 브레이크 적용 후 엔진 점화 처리
        car_controller.brake()
        if car_speed == 0:  # 차량 정지 상태 확인
            car_controller.toggle_engine()
            engine_status = "ON"
            print(f"Engine toggled to {engine_status}")
        else:
            print("[ERROR] Speed must be 0 to toggle engine.")
```

## 3
같은 줄에서 점화 버튼이 먼저 입력되고 이후 브레이크가 입력된 경우 엔진이 켜지지 않아야 함.
```
수정사항 없음
```

## 4
브레이크와 엔진 점화 버튼이 같은 줄에 여러 공백으로 구분된 경우에도 올바른 순서로 실행되면 엔진이 켜져야 함.
```
cmd_s = command.split() # 공백기준 명령어 분리

    if len(cmd_s) > 1: #길이 2부턴 한줄 동시 입력으로 처리
        for i, cmd in enumerate(cmd_s):
            if cmd == "BRAKE" and i + 1 < len(cmd_s): # 다음요소가 유효하면
                if cmd_s[i + 1] == "ENGINE_BTN": #BRAKE 다음 ENGINE_BTN 이면
                    print("\n")
                    print(f"Executing combined command: BRAKE ENGINE_BTN")
                    # 브레이크 적용 후 엔진 점화 처리
                    car_controller.brake()
                    if car_speed == 0:  # 차량 정지 상태 확인
                        car_controller.toggle_engine()
                        engine_status = "ON"
                        print(f"Engine toggled to {engine_status}")
                    else:
                        print("[ERROR] Speed must be 0 to toggle engine.")
    elif command == "ENGINE_BTN":
        print("\n")
        print(f"Current engine status: {engine_status}")
        if car_speed == 0 and engine_status == "ON" :
            car_controller.toggle_engine()
            engine_status = "OFF"
            print(f"Engine toggled to {engine_status}")
        else:
            print("[ERROR] Engine toggles only with brake applied.")
    # elif command == "BRAKE ENGINE_BTN" 부분 삭제
```

## 5
엔진이 켜져 있고 속도가 0 이상인 상태에서 브레이크와 엔진 점화 버튼이 같은 줄에 입력되면 속도가 줄어야 함.
```
    if len(cmd_s) > 1: #길이 2부턴 한줄 동시 입력으로 처리
        for i, cmd in enumerate(cmd_s):
            if cmd == "BRAKE" and i + 1 < len(cmd_s): # 다음요소가 유효하면
                if cmd_s[i + 1] == "ENGINE_BTN": #BRAKE 다음 ENGINE_BTN 이면
                    print("\n")
                    print(f"Executing combined command: BRAKE ENGINE_BTN")
                    # 브레이크 적용 후 엔진 점화 처리
                    car_controller.brake()
                    car_speed = car_controller.get_speed()  # 속도 업데이트
                    if car_speed == 0:  # 차량 정지 상태 확인
                        car_controller.toggle_engine()
                        engine_status = "ON"
                        print(f"Engine toggled to {engine_status}")
                    else:
                        print("[ERROR] Speed must be 0 to toggle engine.")     
```

## 최종 실행결과
```
[TEST START] test_engine_does_not_start_with_incorrect_order_on_same_line - 같은 줄에서 점화 버튼이 먼저 입력되고 이후 브레이크가 입력된 경우 엔진이 켜지지 않아야 함.
[TEST END] test_engine_does_not_start_with_incorrect_order_on_same_line - 같은 줄에서 점화 버튼이 먼저 입력되고 이후 브레이크가 입력된 경우 엔진이 켜지지 않아야 함.
.
[TEST START] test_engine_does_not_start_without_brake_on_same_line - 브레이크 없이 엔진 점화 버튼만 입력된 경우 엔진이 켜지지 않아야 함.


Current engine status: OFF
[ERROR] Engine toggles only with brake applied.
[TEST END] test_engine_does_not_start_without_brake_on_same_line - 브레이크 없이 엔진 점화 버튼만 입력된 경우 엔진이 켜지지 않아야 함.
.
[TEST START] test_engine_starts_only_with_brake_on_same_line - 브레이크와 엔진 점화 버튼이 같은 줄에 올바른 순서로 입력된 경우에만 엔진이 켜져야 함.


Executing combined command: BRAKE ENGINE_BTN
Engine toggled to ON
[TEST END] test_engine_starts_only_with_brake_on_same_line - 브레이크와 엔진 점화 버튼이 같은 줄에 올바른 순서로 입력된 경우에만 엔진이 켜져야 함.
.
[TEST START] test_engine_starts_with_multiple_spaces_on_same_line - 브레이크와 엔진 점화 버튼이 같은 줄에 여러 공백으로 구분된 경우에도 올바른 순서로 실행되면 엔진이 켜져야 함.


Executing combined command: BRAKE ENGINE_BTN
Engine toggled to ON
[TEST END] test_engine_starts_with_multiple_spaces_on_same_line - 브레이크와 엔진 점화 버튼이 같은 줄에 여러 공백으로 구분된 경우에도 올바른 순서로 실행되면 엔진이 켜져야 함.
.
[TEST START] test_speed_reduces_with_brake_and_engine_button - 엔진이 켜져 있고 속도가 0 이상인 상태에서 브레이크와 엔진 점화 버튼이 같은 줄에 올바른 순서로 입력되면 속도가 줄어야 함.


Executing combined command: BRAKE ENGINE_BTN
Engine toggled to ON
Current speed: 0 km/h, Engine: ON
Left door: CLOSED, Right door: CLOSED, Trunk: CLOSED
Speed updated to 10 km/h
Current speed: 10 km/h, Engine: ON
Left door: CLOSED, Right door: CLOSED, Trunk: CLOSED
Speed updated to 20 km/h
Vehicle locked
Left door locked
Right door locked


Executing combined command: BRAKE ENGINE_BTN
[ERROR] Speed must be 0 to toggle engine.
[TEST END] test_speed_reduces_with_brake_and_engine_button - 엔진이 켜져 있고 속도가 0 이상인 상태에서 브레이크와 엔진 점화 버튼이 같은 줄에 올바른 순서로 입력되면 속도가 줄어야 함.
.
----------------------------------------------------------------------
Ran 5 tests in 0.364s

OK
```
