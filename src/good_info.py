import tkinter as tk
from tkinter import ttk
from src import goods_stuff as gs
import asyncio


#  程序主入口
def main():
    user_mon_in(win)
    win.mainloop()


#  用户输入账户钱的页面 入口界面
def user_mon_in(window):
    fm_user_in = fm_()

    tk.Label(fm_user_in, text='enter your money').place(x=30, y=30)
    #  用户金额输入框
    en_user_money = tk.Entry(fm_user_in)
    en_user_money.place(x=30, y=60)

    #  输入验证 检测是否为全数字
    def user_mon_in_enter():
        global USER_MONEY
        USER_MONEY = en_user_money.get()

        if USER_MONEY.isnumeric():
            #  销毁输入金额的frame
            fm_user_in.destroy()
            user_choose()
            tw_cart()
            tw_goods()
            window.geometry('440x260')
        else:
            en_user_money.delete(0, len(USER_MONEY))
            tk.Label(fm_user_in, text='invalid input!').place(x=30, y=90)
            return

    btn_user_money = tk.Button(fm_user_in, text='enter', command=user_mon_in_enter)
    btn_user_money.place(x=115, y=90)


def user_choose():
    var_user_mon.set(USER_MONEY)
    user_choose_x_pos = 310

    la_goods_info_tittle = tk.Label(win, text='商品信息')
    la_goods_info_tittle.place(x=160, y=0)

    tk.Label(win, text='Your Money :').place(x=user_choose_x_pos, y=20)

    def change_view(v_name):
        if v_name == 'goods':
            fm_cart.place_forget()
            fm_goods.place(x=0, y=35)
        elif v_name == 'carts':
            fm_goods.place_forget()
            fm_cart.place(x=0, y=35)

    tk.Button(win, text='goods', width=7, command=lambda: change_view('goods')).place(x=30, y=25)
    tk.Button(win, text='cart', width=7, command=lambda: change_view('carts')).place(x=90, y=25)

    tk.Label(win, text='Id of goods').place(x=user_choose_x_pos, y=70)
    en_user_choose_id = tk.Entry(win, width=15)
    en_user_choose_id.place(x=user_choose_x_pos, y=95)

    tk.Label(win, text='Quantity of goods').place(x=user_choose_x_pos, y=120)
    en_user_choose_quantity = tk.Entry(win, width=15)
    en_user_choose_quantity.place(x=user_choose_x_pos, y=145)

    #  警告文字 如果用户输入的id不正确 要定义在按钮出发的方法内而不能在方法的方法内 会不更新数据
    s_var_warning = tk.StringVar(win, value='')

    def user_goods_purchase():
        in_id = en_user_choose_id.get()
        in_qua = en_user_choose_quantity.get()

        #  非法输入的警告Label
        tk.Label(win, textvariable=s_var_warning).place(x=user_choose_x_pos, y=190)

        if int(in_id) in [good_id[0] for good_id in info_of_goods()]:
            s_var_warning.set('')
            tw_cart_info_.insert('', 'end', values=(in_id, in_qua))
        else:
            s_var_warning.set('invalid input\nenter again')

        #  清空输入框
        en_user_choose_id.delete(0, len(in_id))
        en_user_choose_quantity.delete(0, len(in_qua))

    tk.Button(win, text='Purchase', command=user_goods_purchase).place(x=user_choose_x_pos, y=170)


async def fund_warning():
    win_ = root()
    tk.Label(win_, text='Insufficient fund').place(x=20, y=30)
    await asyncio.sleep(2)


#  滚动条
def scroll_tw(master, tw):
    scroll_ = tk.Scrollbar(master, orient='vertical', command=tw.yview())
    scroll_.configure(command=tw.yview)
    scroll_.place(x=280, y=30)
    return scroll_


#  商品展示 TreeView
def tw_goods():
    global fm_goods

    scroll_tw(fm_goods, tw_goods_info_)

    def load_goods(tree_view):
        for i_, v in enumerate(gs.all_goods):
            tree_view.insert('', i_, values=v)

    #  加载所有商品信息
    load_goods(tw_goods_info_)


def tw_cart():
    scroll_tw(fm_cart, tw_cart_info_)

    def carts_total():
        total_price_ = 0

        #  循环次数为购物车条目数量
        for cart_item in info_of_carts():
            #  获取购物车的每条数据
            for price_good in info_of_goods():
                if cart_item[0] == price_good[0]:
                    total_price_ += int(cart_item[1]) * price_good[2]
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
            win.destroy()
            return

        # 每次结算清空购物车内商品
        [tw_cart_info_.delete(item_) for item_ in tw_cart_info_.get_children()]

        USER_MONEY = last_money
        tk.Label(fm_cart, text='total amount :' + str(total_price)).place(x=20, y=165)
        var_user_mon.set(USER_MONEY)

    tk.Button(fm_cart, text='check', command=lambda: asyncio.run(payment())).place(x=220, y=160)


def tw_(master, **kwargs):
    """
    :kwargs
        heading(list): 列名
        widths(list): 列宽度
    """
    heading = kwargs['heading']
    widths = kwargs['widths']
    tw = ttk.Treeview(master, columns=heading, show='headings', height=5)

    for i in range(len(heading)):
        tw.heading(heading[i], text=heading[i])
        tw.column(heading[i], width=widths[i], anchor='center')

    tw.place(x=20, y=30)
    return tw


def fm_():
    new_fm = tk.Frame(win, height=300, width=300, bd=3)
    new_fm.place(x=0, y=35)
    return new_fm


#  从treeView获取商品信息
def info_of_goods():
    return [tw_goods_info_.item(item)['values'] for item in tw_goods_info_.get_children()]


#  从treeView获取购物车信息
def info_of_carts():
    return [tw_cart_info_.item(item)['values'] for item in tw_cart_info_.get_children()]


def root():
    win_ = tk.Tk()
    win_.geometry('200x200')
    return win_


USER_MONEY = 0
total_price = 0
win = root()
fm_goods = fm_()
fm_cart = fm_()
var_user_mon = tk.StringVar()
#  用户金额
la_user_mon = tk.Label(win, textvariable=var_user_mon).place(x=310, y=40)
tw_cart_info_ = tw_(fm_cart, heading=gs.carts_info_headings, widths=[160, 80])
tw_goods_info_ = tw_(fm_goods, heading=gs.goods_info_headings, widths=[50, 110, 80])

main()
