import tkinter as tk

root_ = tk.Tk()


class window:
    def __init__(self, root):
        self.root = root
        self.root.geometry('400x400')
        self.root.title('SuperMarket')


def main():
    win = window(root_)

    def f1_order():
        fm2.place_forget()
        fm1.place(x=10, y=30)

    def f2_order():
        fm1.place_forget()
        fm2.place(x=10, y=30)
    tk.Button(win.root, text='F1', command=f1_order).place(x=20, y=0)
    tk.Button(win.root, text='F2', command=f2_order).place(x=60, y=0)

    fm1 = tk.Frame(win.root, height=150, width=150, borderwidth=3, bg='red')
    fm1.place(x=10, y=30)
    fm2 = tk.Frame(win.root, height=150, width=150, borderwidth=3, bg='red')

    tk.Label(fm1, text='frame1').place(x=10, y=10)
    tk.Label(fm2, text='frame2').place(x=10, y=10)

    win.root.mainloop()


if __name__ == '__main__':
    main()
