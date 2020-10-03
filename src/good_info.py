from src.module import *


#  用户输入账户钱的页面 入口界面
def user_mon_in(window):
    fm_user_in = fm_(win)

    tk.Label(fm_user_in, text='enter your money').place(x=30, y=30)
    #  用户金额输入框
    en_user_money = tk.Entry(fm_user_in)
    en_user_money.place(x=30, y=60)

    #  输入验证 检测是否为全数字
    def user_mon_in_enter():
        user_money = en_user_money.get()

        if user_money.isnumeric():
            #  销毁输入金额的frame
            fm_user_in.destroy()
            user_choose().set_user_mon(user_money)
            window.geometry('440x260')
        else:
            en_user_money.delete(0, len(user_money))
            tk.Label(fm_user_in, text='invalid input!').place(x=30, y=90)
            return

    tk.Button(fm_user_in, text='enter', command=user_mon_in_enter).place(x=115, y=90)


def user_choose():
    module = Module(win)
    module.var_user_mon.set(module.USER_MONEY)
    module.load_goods()

    tk.Label(win, text='Id of goods').place(x=module.user_choose_x_pos, y=70)
    en_user_choose_id = tk.Entry(win, width=15)
    en_user_choose_id.place(x=module.user_choose_x_pos, y=95)

    tk.Label(win, text='Quantity of goods').place(x=module.user_choose_x_pos, y=120)
    en_user_choose_quantity = tk.Entry(win, width=15)
    en_user_choose_quantity.place(x=module.user_choose_x_pos, y=145)

    #  警告文字 如果用户输入的id不正确 要定义在按钮出发的方法内而不能在方法的方法内 会不更新数据
    def user_goods_purchase():
        in_id = en_user_choose_id.get()
        in_qua = en_user_choose_quantity.get()

        #  非法输入的警告Label
        if int(in_id) in [good_id[0] for good_id in module.info_of_goods()]:
            module.s_var_warning.set('')
            module.tw_carts.insert('', 'end', values=(in_id, in_qua))
        else:
            module.s_var_warning.set('invalid input\nenter again')

        #  清空输入框
        en_user_choose_id.delete(0, len(in_id))
        en_user_choose_quantity.delete(0, len(in_qua))

    tk.Button(win, text='Purchase', command=user_goods_purchase).place(x=module.user_choose_x_pos, y=170)
    tk.Button(module.fm_carts, text='check', command=lambda: asyncio.run(module.payment())).place(x=220, y=160)
    return module


def main():
    user_mon_in(win)
    win.mainloop()


win = root()

if __name__ == '__main__':
    main()
