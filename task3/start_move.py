from pynput import mouse, keyboard
from move_mouse import mouse_status

if __name__ == '__main__':
    print("Press Esp to stop recoder")
    mc = mouse_status()
    keyboard_listener = keyboard.Listener(on_press=mc.on_press)
    mouse_listener = mouse.Listener(on_move=mc.on_move, on_click=mc.on_click)
    keyboard_listener.start()
    mouse_listener.start()
    while mouse_listener.running:
        pass
    print('exit')