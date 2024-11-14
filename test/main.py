import threading
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI


# execute_command를 제어하는 콜백 함수
# -> 이 함수에서 시그널을 입력받고 처리하는 로직을 구성하면, 알아서 GUI에 연동이 됩니다.

def execute_command_callback(command, car_controller):

    engine_status = "ON" if car_controller.get_engine_status() else "OFF"
    car_speed = car_controller.get_speed()
    left_door_status = car_controller.get_left_door_status()  # "OPEN" or "CLOSED"
    right_door_status = car_controller.get_right_door_status()  # "OPEN" or "CLOSED"
    trunk_status = "CLOSED" if car_controller.get_trunk_status() else "OPEN"  # True = Closed, False = Opened
    lock_status = "LOCKED" if car_controller.get_lock_status() else "UNLOCKED"  # True = Locked, False = Unlocked

    if command == "ENGINE_BTN":
        print("\n")
        print(f"Current engine status: {engine_status}")
        if car_speed == 0:
            car_controller.toggle_engine()
            engine_status = "ON" if car_controller.get_engine_status() else "OFF"
            print(f"Engine toggled to {engine_status}")
        else:
            print("[ERROR] Speed must be 0 to toggle engine.")

    elif command == "ACCELERATE":
        print(f"Current speed: {car_speed} km/h, Engine: {engine_status}")
        print(f"Left door: {left_door_status}, Right door: {right_door_status}, Trunk: {trunk_status}")
        if (engine_status == "ON" and left_door_status == "CLOSED" and
            right_door_status == "CLOSED" and trunk_status == "CLOSED" and
            car_speed < 200):
            car_controller.accelerate()
            new_speed = car_controller.get_speed()
            print(f"Speed updated to {new_speed} km/h")
        else:
            print("[ERROR] Conditions not met for acceleration.")

    elif command == "BRAKE":
        print(f"Current speed: {car_speed} km/h, Engine: {engine_status}")
        if engine_status == "ON":
            car_controller.brake()
            new_speed = car_controller.get_speed()
            print(f"Braked to {new_speed} km/h")
        else:
            print("[ERROR] Engine must be ON to brake.")


    elif command == "LOCK":
        car_controller.lock_vehicle() # 차량잠금
        print("Vehicle locked")
        execute_command_callback("LEFT_DOOR_LOCK",car_controller)
        execute_command_callback("RIGHT_DOOR_LOCK",car_controller)
    elif command == "UNLOCK":
        car_controller.unlock_vehicle() # 차량잠금해제
        print("Vehicle unlocked")
        execute_command_callback("LEFT_DOOR_UNLOCK",car_controller)
        execute_command_callback("RIGHT_DOOR_UNLOCK",car_controller)
    
    elif command == "LEFT_DOOR_LOCK":
        if car_controller.get_left_door_lock() == "UNLOCKED" and car_speed == 0:
            car_controller.lock_left_door() # 왼쪽문 잠금
            print("Left door locked")

    elif command == "LEFT_DOOR_UNLOCK":
        if car_controller.get_lock_status() == False:
            car_controller.unlock_left_door() # 왼쪽문 잠금해제
            print("Left door unlocked")

    elif command == "LEFT_DOOR_OPEN":
        if car_controller.get_left_door_lock() == "UNLOCKED" :
            car_controller.open_left_door() # 왼쪽문 열기
            print("Left door opened")

    elif command == "LEFT_DOOR_CLOSE":
        car_controller.close_left_door() # 왼쪽문 닫기
        print("Left door closed")

    elif command == "RIGHT_DOOR_LOCK":
        car_controller.lock_right_door() # 오른쪽문 잠금
        print("Right door locked")

    elif command == "RIGHT_DOOR_UNLOCK":
        if car_controller.get_lock_status() == False :
            car_controller.unlock_right_door() # 오른쪽문 잠금해제
            print("Right door unlocked")

    elif command == "RIGHT_DOOR_OPEN":
        if car_controller.get_right_door_lock() == "UNLOCKED" :
            car_controller.open_right_door() # 오른쪽문 열기
            print("Right door open")

    elif command == "RIGHT_DOOR_CLOSE":
        car_controller.close_right_door() # 오른쪽문 닫기
        print("Right door opened")
    
    elif command == "TRUNK_OPEN":
        if car_controller.get_lock_status() == False :
            car_controller.open_trunk() # 트렁크 열기
            print("Trunk opened")

    elif command == "TRUNK_CLOSE":
        car_controller.close_trunk() # 트렁크 닫기
        print("Trunk closed")

    elif command == "SOS": # SOS 버튼
        while car_controller.get_speed() > 0:
            execute_command_callback("BRAKE",car_controller)
        execute_command_callback("UNLOCK",car_controller)
        execute_command_callback("TRUNK_OPEN",car_controller)
        print("SOS activated: Speed 0, doors unlocked, trunk opened")


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