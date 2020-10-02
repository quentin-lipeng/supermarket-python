import tkinter as tk
from tkinter import ttk
from src import goods_stuff as gs
import asyncio

USER_MONEY = 0
#  用户购物车商品
USER_CARTS = []

total_price = 0


def main():
    win = root()

    user_mon_in(win)
    win.mainloop()


def root():
    win = tk.Tk()
    win.geometry('200x200')
    return win


#  用户输入账户钱的页面
#  待完善 输入必须全数字
def user_mon_in(window):
    fm_user_in = tk.Frame(window, height=300, width=300, bd=3)
    fm_user_in.place(x=0, y=0)

    la_user_money = tk.Label(fm_user_in, text='enter your money')
    la_user_money.place(x=30, y=30)
    en_user_money = tk.Entry(fm_user_in)
    en_user_money.place(x=30, y=60)

    def user_mon_in_enter():
        global USER_MONEY
        USER_MONEY = en_user_money.get()

        if USER_MONEY.isnumeric():
            fm_user_in.destroy()
            user_choose(window)
            tw_goods(window)
            window.geometry('440x350')
        else:
            en_user_money.delete(0, len(USER_MONEY))
            tk.Label(window, text='invalid input!').place(x=30, y=95)
            return

    btn_user_money = tk.Button(fm_user_in, text='enter', command=user_mon_in_enter)
    btn_user_money.place(x=115, y=90)


def la_user_mon(window):
    tk.Label(window, text=USER_MONEY).place(x=310, y=40)


def list_fm_good_cart():
    return []


def user_choose(window):
    user_choose_x_pos = 310

    la_goods_info_tittle = tk.Label(window, text='商品信息')
    la_goods_info_tittle.place(x=160, y=0)

    tk.Label(window, text='Your Money :').place(x=310, y=20)

    def change_view(v_name):
        if v_name == 'goods':
            fm_cart(window).destroy()
            tw_goods(window)
        elif v_name == 'carts':
            fm_goods(window).destroy()
            tw_cart(window)

    btn_goods_info = tk.Button(window, text='goods', width=7, command=lambda: change_view('goods'))
    btn_goods_info.place(x=30, y=25)
    btn_goods_cart = tk.Button(window, text='cart', width=7, command=lambda: change_view('carts'))
    btn_goods_cart.place(x=90, y=25)

    #  显示当前资资金
    la_user_mon(window)

    tk.Label(window, text='Id of goods').place(x=user_choose_x_pos, y=70)
    en_user_choose_id = tk.Entry(window, width=15)
    en_user_choose_id.place(x=user_choose_x_pos, y=95)

    tk.Label(window, text='Quantity of goods').place(x=user_choose_x_pos, y=120)
    en_user_choose_quantity = tk.Entry(window, width=15)
    en_user_choose_quantity.place(x=user_choose_x_pos, y=145)

    #  警告文字 如果用户输入的id不正确 要定义在按钮出发的方法内而不能在方法的方法内 会不更新数据
    s_var_warning = tk.StringVar(window, value='')

    def ids_of_goods():
        goods_view = tw_goods(window)
        return [goods_view.item(v)['values'][0] for v in goods_view.get_children()]

    def user_goods_purchase():
        in_id = en_user_choose_id.get()
        in_qua = en_user_choose_quantity.get()

        la_input_warning = tk.Label(window, textvariable=s_var_warning)
        la_input_warning.place(x=user_choose_x_pos, y=190)

        if int(in_id) in ids_of_goods():
            USER_CARTS.append([in_id, in_qua])
            s_var_warning.set('')
        else:
            s_var_warning.set('invalid input\nenter again')

        #  清空输入框
        en_user_choose_id.delete(0, len(in_id))
        en_user_choose_quantity.delete(0, len(in_qua))

    btn_user_choose_purchase = tk.Button(window, text='Purchase', command=user_goods_purchase)
    btn_user_choose_purchase.place(x=user_choose_x_pos, y=170)


fm_goods_ = None
fm_cart_ = None


def fm_(window):
    new_fm = tk.Frame(window, height=300, width=300, bd=3)
    new_fm.place(x=0, y=60)
    return new_fm


def fm_goods(window):
    return fm_(window)


def fm_cart(window):
    return fm_(window)


#  商品展示 TreeView
def tw_goods(window):
    info_headings = gs.goods_info_headings
    my_fm_goods = fm_goods(window)
    tw_goods_info = ttk.Treeview(my_fm_goods, columns=info_headings, show='headings', height=5)

    for i in range(len(info_headings)):
        tw_goods_info.heading(info_headings[i], text=info_headings[i])

    tw_goods_info.column(info_headings[0], width=50, anchor='center')
    tw_goods_info.column(info_headings[1], width=110, anchor='center')
    tw_goods_info.column(info_headings[2], width=80, anchor='center')
    tw_goods_info.place(x=20, y=30)

    scroll_goods = tk.Scrollbar(my_fm_goods, orient='vertical', command=tw_goods_info.yview())
    scroll_goods.configure(command=tw_goods_info.yview)
    scroll_goods.place(x=280, y=30)

    def load_goods(tree_view):
        for i_, v in enumerate(gs.all_goods):
            tree_view.insert('', i_, values=v)

    #  加载所有商品信息
    load_goods(tw_goods_info)
    return tw_goods_info


async def fund_warning():
    win_ = root()
    tk.Label(win_, text='Insufficient fund').place(x=20, y=30)
    await asyncio.sleep(2)


def tw_cart(window):
    #  总价格
    #  购物车的frame
    carts = gs.carts_info_headings
    my_fm_cart = fm_cart(window)

    tw_carts_info = ttk.Treeview(my_fm_cart, columns=carts, show='headings', height=5)

    for i in range(2):
        tw_carts_info.heading(carts[i], text=carts[i])

    tw_carts_info.column(carts[0], width=160, anchor='center')
    tw_carts_info.column(carts[1], width=80, anchor='center')
    tw_carts_info.place(x=20, y=30)

    scroll_carts = tk.Scrollbar(my_fm_cart, orient='vertical', command=tw_carts_info.yview())
    scroll_carts.configure(command=tw_carts_info.yview)
    scroll_carts.place(x=280, y=30)

    #  待完善 每次查询购物车中商品是否重复 重复就叠加起来 但意义不大
    def check_carts(carts_):
        pass

    def load_carts(tree_view):
        for i_, v in enumerate(USER_CARTS):
            tree_view.insert('', i_, values=v)

    load_carts(tw_carts_info)

    def ids_of_goods():
        goods_view = tw_goods(window)
        return [goods_view.item(v)['values'] for v in goods_view.get_children()]

    def carts_total():
        total_price_ = 0
        for carts_count in USER_CARTS:
            for price_good in ids_of_goods():
                if carts_count[0] == str(price_good[0]):
                    total_price_ += int(carts_count[1]) * price_good[2]
                    break
        return total_price_

    async def payment():
        global total_price
        global USER_MONEY
        #  购物车总金额
        total_price = carts_total()
        last_money = float(USER_MONEY) - total_price
        if last_money < 0:
            await fund_warning()
            window.destroy()
            return
        USER_MONEY = last_money
        tk.Label(window, text='total amount :' + str(total_price)).place(x=20, y=250)
        la_user_mon(window)

    tk.Button(my_fm_cart, text='check', command=lambda: asyncio.run(payment())).place(x=220, y=160)

    return tw_carts_info


main()
