import threading
import tkinter as tk

class CarSimulatorGUI:
    def __init__(self, car_controller, execute_command_callback):
        self.car_controller = car_controller
        self.execute_command_callback = execute_command_callback  # execute_command 콜백
        self.window = tk.Tk()
        self.window.title("Car Simulator")

        # 창의 크기를 더 크게 설정
        self.window.geometry("900x700")

        # 상단 상태 정보 (엔진, 속도, 차량 잠금 상태)
        self.create_top_status()

        # 이미지 로드 및 배치
        self.load_image()

        # GUI 요소 생성
        self.create_widgets()

        # 상태 인디케이터와 메시지 생성
        self.create_indicator()

    def create_top_status(self):
        """엔진, 속도, 차량 전체 잠금 상태를 상단에 표시"""
        self.engine_button = tk.Button(self.window, text="Engine OFF", bg="red", fg="white", font=("Helvetica", 24),
                                       width=20, height=2)
        self.engine_button.pack(padx=20, pady=10)

        self.lock_label = tk.Label(self.window, text="Vehicle Locked", font=("Helvetica", 24))
        self.lock_label.pack(padx=20, pady=10)

        self.speed_label = tk.Label(self.window, text="Speed: 0 km/h", font=("Helvetica", 24))
        self.speed_label.pack(padx=20, pady=10)

    def load_image(self):
        """이미지를 로드하여 캔버스에 표시"""
        self.car_photo = tk.PhotoImage(file="car.png")  # 이미지 경로로 설정

        # 캔버스에 이미지 배치
        self.canvas = tk.Canvas(self.window, width=800, height=350)
        self.canvas.create_image(400, 200, image=self.car_photo)
        self.canvas.pack()

    # GUI 위젯 생성 및 배치
    def create_widgets(self):
        """트렁크와 좌우 도어 상태 표시"""
        self.status_frame = tk.Frame(self.window)
        self.status_frame.pack(pady=10)

        # 트렁크 상태 레이블 (이미지 바로 아래)
        self.trunk_label = tk.Label(self.status_frame, text="Trunk: Closed", font=("Helvetica", 24))
        self.trunk_label.grid(row=0, column=1, padx=10, pady=10)

        # 좌측 도어 상태와 잠금 상태 레이블 (이미지 왼쪽)
        self.left_status_frame = tk.Frame(self.window)
        self.left_status_frame.place(x=20, y=400)
        self.left_door_label = tk.Label(self.left_status_frame, text="Left Door: Closed", font=("Helvetica", 20))
        self.left_door_label.pack(pady=5)
        self.left_door_lock_label = tk.Label(self.left_status_frame, text="Left Door Lock: Locked",
                                             font=("Helvetica", 20))
        self.left_door_lock_label.pack(pady=5)

        # 우측 도어 상태와 잠금 상태 레이블 (이미지 오른쪽)
        self.right_status_frame = tk.Frame(self.window)
        self.right_status_frame.place(x=580, y=400)
        self.right_door_label = tk.Label(self.right_status_frame, text="Right Door: Closed", font=("Helvetica", 20))
        self.right_door_label.pack(pady=5)
        self.right_door_lock_label = tk.Label(self.right_status_frame, text="Right Door Lock: Locked",
                                              font=("Helvetica", 20))
        self.right_door_lock_label.pack(pady=5)

    # 상태 인디케이터 생성 및 배치
    def create_indicator(self):
        """우측 상단에 인디케이터와 상태 메시지 표시"""
        self.indicator_canvas = tk.Canvas(self.window, width=30, height=30)
        self.indicator_canvas.place(x=850, y=10)
        self.indicator = self.indicator_canvas.create_oval(5, 5, 25, 25, fill="green")

        self.status_label = tk.Label(self.window, text="[Ready]", font=("Helvetica", 16))
        self.status_label.place(x=810, y=50)

    # 상태 업데이트
    def update_gui(self):
        """차량의 모든 상태를 업데이트"""
        # 엔진 상태 업데이트
        if self.car_controller.get_engine_status():
            self.engine_button.config(bg="blue", text="Engine ON")
        else:
            self.engine_button.config(bg="red", text="Engine OFF")

        # 차량 잠금 상태 업데이트
        if self.car_controller.get_lock_status():
            self.lock_label.config(text="Vehicle Locked")
        else:
            self.lock_label.config(text="Vehicle Unlocked")

        # 속도 상태 업데이트
        self.speed_label.config(text=f"Speed: {self.car_controller.get_speed()} km/h")

        # 트렁크 상태 업데이트
        if self.car_controller.get_trunk_status():
            self.trunk_label.config(text="Trunk: Closed")
        else:
            self.trunk_label.config(text="Trunk: Opened")

        # 좌측 도어 상태 업데이트
        if self.car_controller.get_left_door_status() == "OPEN":
            self.left_door_label.config(text="Left Door: Open")
        else:
            self.left_door_label.config(text="Left Door: Closed")

        # 좌측 도어 잠금 상태 업데이트
        if self.car_controller.get_left_door_lock() == "LOCKED":
            self.left_door_lock_label.config(text="Left Door Lock: Locked")
        else:
            self.left_door_lock_label.config(text="Left Door Lock: Unlocked")

        # 우측 도어 상태 업데이트
        if self.car_controller.get_right_door_status() == "OPEN":
            self.right_door_label.config(text="Right Door: Open")
        else:
            self.right_door_label.config(text="Right Door: Closed")

        # 우측 도어 잠금 상태 업데이트
        if self.car_controller.get_right_door_lock() == "LOCKED":
            self.right_door_lock_label.config(text="Right Door Lock: Locked")
        else:
            self.right_door_lock_label.config(text="Right Door Lock: Unlocked")

        # 인디케이터 상태를 녹색으로 돌림
       # self.indicator_canvas.itemconfig(self.indicator, fill="green")
       # self.status_label.config(text="[Ready]", fg="green")

        self.window.update()

    # 명령 실행 함수 (스레드를 사용해 명령어 처리)
    def execute_command(self, command):
        """명령어에 따라 차량 상태를 제어"""
        # 처리 중임을 나타내기 위해 인디케이터와 상태 메시지 업데이트
        self.indicator_canvas.itemconfig(self.indicator, fill="red")
        self.status_label.config(text="[Processing]", fg="red")
        self.window.update()  # GUI 상태를 즉시 반영

        # 명령어 처리 스레드 시작
        thread = threading.Thread(target=self._run_command, args=(command,))
        thread.start()

    def _run_command(self, command):
        """백그라운드에서 명령어를 처리하는 함수"""
        self.execute_command_callback(command)
        # 명령 처리 완료 후 GUI 업데이트
        self.window.after(0, self.update_gui)

    # 명령어 파일을 처리하는 함수
    def process_commands(self, file_path):
        """파일에서 명령어를 읽어와 처리"""
        try:
            with open(file_path, 'r') as file:
                commands = [line.strip() for line in file]

            current_command_index = 0

            def execute_next_command():
                nonlocal current_command_index
                if current_command_index < len(commands):
                    command = commands[current_command_index]
                    self.execute_command(command)  # 명령 실행
                    current_command_index += 1
                    self.window.after(2000, execute_next_command)  # 3초 대기 후 다음 명령 실행
                else:

                    self.indicator_canvas.itemconfig(self.indicator, fill="green")
                    self.status_label.config(text="[Ready]", fg="green")
                    self.window.update()

                    print("All commands executed.")

            execute_next_command()

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # GUI 시작 함수
    def start(self):
        self.window.mainloop()
