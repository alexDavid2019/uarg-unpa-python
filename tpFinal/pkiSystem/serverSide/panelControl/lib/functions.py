# -*- coding: UTF-8 -*-

def set_window_center(window, width, height):
    w_s = window.winfo_screenwidth()
    h_s = window.winfo_screenheight()
    x_co = (w_s - width) / 2
    y_co = (h_s - height) / 2 - 50
    window.geometry("%dx%d+%d+%d" % (width, height, x_co, y_co))
    window.minsize(width, height)

def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()

def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    # print(tv.get_children(''))
    l.sort(reverse=reverse)
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column(
        tv, col, not reverse))
