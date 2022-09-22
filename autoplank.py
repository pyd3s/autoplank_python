#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@date: 2022-09-19
#@mail: pydes.wu@gmail.com
#@desc: auto plank

# TODO: import
import subprocess
import sys
import time

# TODO: check base software
base_sw = (
    'xdotool',
    'xrandr',
    'dconf',
    'plank',
)

# TODO: has sw
def has_sw(sw):
    try:
        cmd = f'''which {sw}'''
        subprocess.check_output(cmd, shell=True)
        return True
    except Exception as e:
        return False

# TODO: get mouse location
def get_mouse_location():
    try:
        cmd = '''xdotool getmouselocation'''
        get_ot = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split()
        ot_dict = {}
        for each_key_value in get_ot:
            key, value = each_key_value.split(':')
            ot_dict[key] = int(value)
        return ot_dict
    except Exception as e:
        return False

# TODO: get display
def get_display():
    try:
        cmd = '''xrandr'''
        get_display = subprocess.check_output(cmd, shell=True).decode('utf-8')
        display_list = []
        for each_line in get_display.split('\n'):
            if 'connected' in each_line:
                each_line_list = each_line.split()
                xy = each_line_list[2]
                if each_line_list[1] == 'connected':
                    connect_status = True
                else:
                    connect_status = False
                    xy = False
                if each_line_list[2] == 'primary':
                    primary_tag = True
                    xy = each_line_list[3]
                else:
                    primary_tag = False
                if xy:
                    axis_x, axis_y, offset_x, offset_y = xy.replace('x', ' ').replace('+', ' ').split(' ')
                else:
                    axis_x = 0
                    axis_y = 0
                    offset_x = 0
                    offset_y = 0
                display_list.append(
                    {
                        'display': each_line_list[0],
                        'connected':  connect_status,
                        'primary': primary_tag,
                        'axis_x': int(axis_x),
                        'axis_y': int(axis_y),
                        'offset_x': int(offset_x),
                        'offset_y': int(offset_y),
                    }
                )
        return display_list
    except Exception as e:
        return False

# TODO: read plank display
def get_plank_display():
    try:
        cmd = '''dconf read /net/launchpad/plank/docks/dock1/monitor'''
        get_display = subprocess.check_output(cmd, shell=True).decode('utf-8').replace('\n', '')
        return get_display
    except Exception as e:
        return False

# TODO: write plank display
def set_plank_display(display_value):
    try:
        cmd = f'''dconf write /net/launchpad/plank/docks/dock1/monitor "'{display_value}'" '''
        set_display = subprocess.check_output(cmd, shell=True).decode('utf-8')
        return True
    except Exception as e:
        return False

# TODO: killall plank
def kill_plank():
    try:
        cmd = '''killall plank'''
        kill_plank = subprocess.check_output(cmd, shell=True).decode('utf-8')
        return True
    except Exception as e:
        return False

# TODO: start plank
def start_plank():
    try:
        cmd = '''plank'''
        run_plank = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        return False

# TODO: within display
def within_display(display, x, y):
    return x > display.get('offset_x') and\
           x < display.get('offset_x') + display.get('axis_x') and \
           y > display.get('offset_y') and \
           y < display.get('offset_y') + display.get('axis_y')

# TODO: isbottom display
def isbottom_display(display, y):
    return y < display.get('offset_y') + display.get('axis_y') and \
           y > display.get('offset_y') + display.get('axis_y') - 20

# TODO: has sw need
def has_sw_need():
    tag = True
    for each_sw in base_sw:
        has_sw_action = has_sw(sw=each_sw)
        if not has_sw_action:
            msg = f'''{each_sw} not found in PATH'''
            #print(msg)
            tag = False
            break
    return tag

display_found = []

# TODO: loop event
def run_loop():
    while 1:
        get_mouse_location_action = get_mouse_location()
        if get_mouse_location_action:
            for each_display in display_found:
                if each_display.get('connected'):
                    x = get_mouse_location_action.get('x')
                    y = get_mouse_location_action.get('y')
                    is_within = within_display(each_display, x, y)
                    is_isbottom = isbottom_display(each_display, y)
                    if  is_within and is_isbottom:
                        print(f'''within: {is_within}, isbottom: {is_isbottom}, display: {each_display.get('display')}''')
                        get_plank_display_action = get_plank_display()
                        get_d = get_plank_display_action.replace("'",'').strip()
                        if get_d != each_display.get('display'):
                            set_plank_display_action = set_plank_display(each_display.get('display'))
                            kill_plank_action = kill_plank()
                            print(f'>_ kill plank: {kill_plank_action}')
                            start_plank_action = start_plank()
                            print(f'>_ start plank: {start_plank_action}')
                            print('>_ change display: ', each_display.get('display'))
                        else:
                            pass
                            #print('>_ pass: ', each_display.get('display'))
                    else:
                        pass
        time.sleep(2)

# TODO: main
def main():
    has_sw_need_action = has_sw_need()
    if has_sw_need_action:
        get_display_action = get_display()
        if get_display_action:
            global display_found
            display_found = get_display_action
            start_plank_action = start_plank()
            if start_plank_action:
                run_loop()
            else:
                msg = '''start plank error'''
                #print(msg)
                sys.exit(0)
        else:
            msg = '''get display error'''
            #print(msg)
            sys.exit(0)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()

# TODO: test
# get_mouse_location_action = get_mouse_location()
# print(get_mouse_location_action)
# get_display_action = get_display()
# print(get_display_action)
# get_plank_display_action = get_plank_display()
# print(get_plank_display_action)
# set_plank_display_action = set_plank_display('eDP-1')
# print(set_plank_display_action)