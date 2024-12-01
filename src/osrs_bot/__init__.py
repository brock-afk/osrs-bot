from pynput import mouse, keyboard
from pynput.keyboard import KeyCode
from pynput.mouse import Controller, Button
import json
import time

recorded_clicks = []
stop_flag = False
mouse_controller = Controller()


def on_click(x: int, y: int, button: Button, is_pressed: int):
    global stop_flag
    if is_pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")
        recorded_clicks.append(
            {
                "time": time.time(),
                "x": x,
                "y": y,
                "button": button.name,
            }
        )


def on_key_press(key: KeyCode):
    global stop_flag
    try:
        if key == keyboard.Key.esc:
            stop_flag = True
    except AttributeError:
        pass


def record_mouse_clicks():
    global stop_flag
    print("Recording mouse clicks... Press 'Esc' to stop.")
    with (
        mouse.Listener(on_click=on_click) as mouse_listener,
        keyboard.Listener(on_press=on_key_press) as keyboard_listener,
    ):
        while not stop_flag:
            time.sleep(0.1)

        mouse_listener.stop()
        keyboard_listener.stop()

    with open("mouse_clicks.json", "w") as file:
        json.dump(recorded_clicks, file)

    print("Recording stopped. Events saved to mouse_clicks.json")


def replay_mouse_clicks():
    with open("mouse_clicks.json", "r") as file:
        clicks = json.load(file)

    print("Replaying mouse clicks...")
    start_time = clicks[0]["time"]
    for click in clicks:
        delay = click["time"] - start_time
        time.sleep(delay)
        start_time = click["time"]

        mouse_controller.position = (click["x"], click["y"])
        button = Button.left if click["button"] == "left" else Button.right
        mouse_controller.press(button)
        mouse_controller.release(button)
        print(f"Replayed click at ({click['x']}, {click['y']}) with {click['button']}")


def main():
    choice = input("Enter 'r' to record or 'p' to replay: ").strip().lower()
    if choice == "r":
        record_mouse_clicks()
    elif choice == "p":
        replay_mouse_clicks()
    else:
        print("Invalid choice. Use 'r' to record or 'p' to replay.")


if __name__ == "__main__":
    main()
