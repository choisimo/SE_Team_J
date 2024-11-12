import threading
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI


# execute_command를 제어하는 콜백 함수
# -> 이 함수에서 시그널을 입력받고 처리하는 로직을 구성하면, 알아서 GUI에 연동이 됩니다.

def execute_command_callback(command, car_controller):

    engine_status = car_controller.get_engine_status()
    car_speed = car_controller.get_speed()
    left_door_status = car_controller.get_left_door_status()
    right_door_status = car_controller.get_right_door_status()
    trunk_status = car_controller.get_trunk_status()


    # 2.2.1 엔진 제어 요구 사항
    # 1.현재 엔진 상태 확인 > 2.명령 입력 > 3.상태 변경 수행 > 4.상태 업데이트 > 5.상태 확인
    if command == "ENGINE_BTN":
        # 1. 현재 엔진 상태 확인
        print(f"Current engine status: {engine_status}")

        # 2. 명령 입력
        print("ENGINE_BTN command executed")

        # 3. 상태 변경 수행
        if car_speed == 0:
            car_controller.toggle_engine()

        # 4. 엔진 상태 업데이트
            engine_status = "ON" if engine_status == "OFF" else "OFF"
            return f"engine toggled to {engine_status}"

        else:
            return f"[ERROR] current speed must be 0 to toggle engine state."


    # 2.2.3 가속 페달 요구 사항
    # 1.현재 속도 확인 > 2.명령 입력 > 3.속도 증가 수행 > 4.속도 업데이트 > 5.상태 확인

    # 3.2.3 가속 페달 제어
    # 사전 조건:
    # - 자동차의 엔진이 ON 상태이어야 함
    # - 자동차의 모든 문이 CLOSED 상태이어야 함
    # - 자동차의 트렁크가 CLOSED 상태이어야 함
    # - 자동차의 속도가 200km/h 이하이어야 함

    elif command == "ACCELERATE":

        # 1. 현재 속도와 가속 상태를 사용자 인터페이스에 표시함
        print(f"Current speed: {car_speed} km/h")
        print(f"Current engine status: {engine_status}")
        print(f"Left door status: {car_controller.left_door_status}, Right door status: {car_controller.right_door_status}")
        print(f"Trunk status: {car_controller.trunk_status}")

        # 2. 명령 입력
        print("ACCELERATE command executed")

        # 3. 사전 조건 만족할 때 가속 수행
        if (engine_status == "ON" and
            left_door_status == "CLOSED" and
            right_door_status() == "CLOSED" and
            trunk_status == "CLOSED" and
            car_speed < 200):
            car_controller.accelerate() # 속도 +10

            # 4. 속도 업데이트
            new_speed = car_controller.get_speed()
            return f"Speed update to: {new_speed} km/h"

        else:
            return "[ERROR] Engine must be ON and speed below 200 to accelerate."


    # 2.2.4 브레이크 페달 요구 사항
    # 1.현재 속도 확인 > 2.명령 입력 > 3.속도 감소 수행 > 4.속도 업데이트 > 5.상태 확인
    elif command == "BRAKE":
        # 1. 현재 속도 확인
        print(f"Current speed: {car_speed} km/h")

        # 2. 명령 입력
        print("Brake command executed")

        # 3. 속도 감소 수행
        if engine_status == "ON":
            car_controller.brake() # 속도 -10

            # 4. 속도 업데이트
            new_speed = car_controller.get_speed()
            print(f"Speed update to: {new_speed} km/h")

            # 5. 상태 확인
            return f"Braked speed: {new_speed} km/h"
        else:
            return "[ERROR] Engine must be ON to brake"


    # 2.2.2 자동차 전체 잠금 장치 요구 사항
    # 1.현재 잠금 상태 확인 > 2.명령 입력 > 3.상태 변경 수행 > 4.상태 업데이트 > 5.상태 확인
    elif command == "LOCK":
        if (car_controller.get_left_door_status() == "CLOSED" and car_controller.get_right_door_status() == "CLOSED"
                and car_controller.get_trunk_status() == "CLOSED"):
            car_controller.lock_vehicle()
        else:
            return "[ERROR] All doors and trunk must be closed to lock the vehicle"
    elif command == "UNLOCK":
        car_controller.unlock_vehicle() # 차량잠금해제
    elif command == "LEFT_DOOR_LOCK":
        if car_controller.get_left_door_lock() == "UNLOCKED" and car_speed == 0:
            car_controller.lock_left_door() # 왼쪽문 잠금
    elif command == "LEFT_DOOR_UNLOCK":
        car_controller.unlock_left_door() # 왼쪽문 잠금해제
    elif command == "LEFT_DOOR_OPEN":
        car_controller.open_left_door() # 왼쪽문 열기
    elif command == "LEFT_DOOR_CLOSE":
        car_controller.close_left_door() # 왼쪽문 닫기
    elif command == "TRUNK_OPEN":
        car_controller.open_trunk() # 트렁크 열기


# 파일 경로를 입력받는 함수
# -> 가급적 수정하지 마세요.
#    테스트의 완전 자동화 등을 위한 추가 개선시에만 일부 수정이용하시면 됩니다. (성적 반영 X)
def file_input_thread(gui):
    while True:
        file_path = input("Please enter the command file path (or 'exit' to quit): ")

        if file_path.lower() == 'exit':
            print("Exiting program.")
            break

        # 파일 경로를 받은 후 GUI의 mainloop에서 실행할 수 있도록 큐에 넣음
        gui.window.after(0, lambda: gui.process_commands(file_path))

# 메인 실행
# -> 가급적 main login은 수정하지 마세요.
if __name__ == "__main__":
    car = Car()
    car_controller = CarController(car)

    # GUI는 메인 스레드에서 실행
    gui = CarSimulatorGUI(car_controller, lambda command: execute_command_callback(command, car_controller))

    # 파일 입력 스레드는 별도로 실행하여, GUI와 병행 처리
    input_thread = threading.Thread(target=file_input_thread, args=(gui,))
    input_thread.daemon = True  # 메인 스레드가 종료되면 서브 스레드도 종료되도록 설정
    input_thread.start()

    # GUI 시작 (메인 스레드에서 실행)
    gui.start()