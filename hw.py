import os
from tkinter import *
from tkinter import messagebox
import json
import requests


def load_config(file):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file, encoding='UTF-8') as cfg:
        return json.loads(cfg.read())


def send_password_to_tg(config):
    answer = {
        'chat_id': config['tg_chat_id'],
        'text': config['password']}
    requests.post(config['tg_main_url'] + config['tg_bot_token'] + config['tg_method'], json=answer)


def tries(action):
    if action == 'add':
        with open('tries.txt', 'a') as f:
            f.writelines('tries\n')
    elif action == 'reset':
        with open('tries.txt', 'w') as f:
            f.writelines('')
    elif action == 'check':
        with open('tries.txt', 'r') as f:
            lines = f.readlines()
        return len(lines)
    elif action == "create_file":
        with open('tries.txt', 'w') as f:
            f.writelines('')


def app(config):
    def greeting_new_user(event):
        login = entry_login.get()
        messagebox.showinfo(title=config['greeting_title'],
                            message=f"{config['greeting_prefix']}{login}")

    def clear_password_entry(event):
        entry_password.delete(0, 'end')

    def check_login(login, user_entry):
        if user_entry == login:
            return True
        return False

    def check_password(password, user_entry):
        if user_entry == password:
            return True
        return False

    def show_error_message(error):
        error_message = config["error_0"]
        if error == 1:
            error_message = config["error_1"]
        elif error == 2:
            error_message = config["error_2"]
        elif error == 3:
            error_message = config["error_3"]
        return error_message

    def auth(event):
        if check_login(config['login'], entry_login.get()):
            if check_password(config['password'], entry_password.get()):
                greeting_new_user(event)
                label_info['text'] = config['info_message']
                tries('reset')
            else:
                if tries('check') < config['tries_to_login']:
                    label_info['text'] = show_error_message(1)
                    clear_password_entry(event)
                    tries('add')
                else:
                    label_info['text'] = show_error_message(3)
                    clear_password_entry(event)
                    send_password_to_tg(config)
                    tries('reset')
        else:
            label_info['text'] = show_error_message(1)
            clear_password_entry(event)

    tries('create_file')

    root = Tk()

    root.title(config['title'])
    root.geometry(config['geometry'])

    if config['resizable_width'] == "False" and config['resizable_height'] == "False":
        resizable_width, resizable_height = False, False
    else:
        resizable_width, resizable_height = True, True

    root.resizable(resizable_width, resizable_height)

    label_program_name = Label(master=root, text=config['label_program_name'], font=config['big_font'])
    label_program_name.place(x=50, y=20, width=config['base_width'], height=config['base_height'])

    label_info = Label(master=root, text=config['info_message'], font=config['small_font'])
    label_info.place(x=50, y=230, width=config['base_width'], height=config['base_height'])

    label_login = Label(master=root, text="login", font=config['mid_font'])
    label_login.place(x=50, y=60, width=config['base_width'], height=config['base_height'])

    label_password = Label(master=root, text="password", font=config['mid_font'])
    label_password.place(x=50, y=160, width=config['base_width'], height=config['base_height'])

    entry_login = Entry(master=root, font=config['mid_font'])
    entry_login.place(x=50, y=90, width=config['base_width'], height=config['base_height'])

    entry_password = Entry(master=root, font=config['mid_font'], show='*')
    entry_password.place(x=50, y=190, width=config['base_width'], height=config['base_height'])

    button_submit = Button(master=root, text=config['button_submit_test'])
    button_submit.place(x=50, y=300, width=config['base_width'], height=config['base_height'])
    button_submit.bind("<Button-1>", auth)
    button_submit.bind("<Button-3>", clear_password_entry)

    root.mainloop()


if __name__ == '__main__':
    app(load_config('settings.json'))
