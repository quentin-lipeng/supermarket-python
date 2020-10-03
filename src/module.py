import tkinter as tk
from tkinter import ttk
from src import goods_stuff as gs
import asyncio


def fm_(win):
    new_fm = tk.Frame(win, height=300, width=300, bd=3)
    new_fm.place(x=0, y=35)
    return new_fm


def root():
    win_ = tk.Tk()
    win_.geometry('200x200')
    return win_


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


async def fund_warning():
    win_ = root()
    tk.Label(win_, text='Insufficient fund').place(x=20, y=30)
    await asyncio.sleep(2)


def scroll_tw(master, tw):
    scroll_ = tk.Scrollbar(master, orient='vertical', command=tw.yview())
    scroll_.configure(command=tw.yview)
    scroll_.place(x=280, y=30)
    return scroll_


class Module:
    def __init__(self, win):
        self.win = win
        self.USER_MONEY = 0
        self.user_choose_x_pos = 301
        self.var_user_mon = tk.StringVar()
        self.s_var_warning = tk.StringVar()
        self.la_user_mon = tk.Label(win, textvariable=self.var_user_mon).place(x=310, y=40)
        self.fm_carts = fm_(self.win)
        self.fm_goods = fm_(self.win)
        self.tw_carts = tw_(self.fm_carts, heading=gs.carts_info_headings, widths=[160, 80])
        self.tw_goods = tw_(self.fm_goods, heading=gs.goods_info_headings, widths=[50, 110, 80])
        self.v_name = ''
        self.scroll_goods = scroll_tw(self.fm_goods, self.tw_goods)
        self.scroll_carts = scroll_tw(self.fm_carts, self.tw_carts)
        self.__total_price_ = 0
        self.la_in_id_war = tk.Label(win, textvariable=self.s_var_warning)
        self.la_in_id_war.place(x=310, y=200)
        self.la_tittle = tk.Label(self.win, text='商品信息')
        self.la_tittle.place(x=160, y=0)

        self.la_mon_point = tk.Label(win, text='Your Money :').place(x=self.user_choose_x_pos, y=20)

        self.btn_goods_view = tk.Button(win, text='goods', width=7,
                                        command=lambda: self.set_v_name('goods')).place(x=30, y=25)
        self.btn_carts_view = tk.Button(win, text='cart', width=7,
                                        command=lambda: self.set_v_name('carts')).place(x=90, y=25)

    def set_user_mon(self, money):
        self.USER_MONEY = money
        self.var_user_mon.set(self.USER_MONEY)

    def __change_view(self):
        if self.v_name == 'goods':
            self.fm_carts.place_forget()
            self.fm_goods.place(x=0, y=35)
        elif self.v_name == 'carts':
            self.fm_goods.place_forget()
            self.fm_carts.place(x=0, y=35)

    def set_v_name(self, v_name):
        self.v_name = v_name
        self.__change_view()

    def load_goods(self):
        for i_, v in enumerate(gs.all_goods):
            self.tw_goods.insert('', i_, values=v)
        self.var_user_mon.set(self.USER_MONEY)

    def carts_total(self):
        #  循环次数为购物车条目数量
        for cart_item in self.info_of_carts():
            #  获取购物车的每条数据
            for price_good in self.info_of_goods():
                if cart_item[0] == price_good[0]:
                    self.__total_price_ += int(cart_item[1]) * price_good[2]
                    break
        return self.__total_price_

    def info_of_carts(self):
        return [self.tw_carts.item(item)['values'] for item in self.tw_carts.get_children()]

    def info_of_goods(self):
        return [self.tw_goods.item(item)['values'] for item in self.tw_goods.get_children()]

    async def payment(self):
        #  购物车总金额
        total_price = self.carts_total()
        last_money = float(self.USER_MONEY) - total_price
        if last_money < 0:
            await fund_warning()
            self.win.destroy()
            return

        # 每次结算清空购物车内商品
        [self.tw_carts.delete(item_) for item_ in self.tw_carts.get_children()]

        self.USER_MONEY = last_money
        tk.Label(self.fm_carts, text='total amount :' + str(total_price)).place(x=20, y=165)
        self.var_user_mon.set(self.USER_MONEY)
