from src import goods_stuff as gs
import tkinter as tk


class Goods:
    def __init__(self, master):
        self.master = master
        self.tw_goods = None
        self.goods_info = []

    #  加载商品页面信息
    def load_goods(self):
        for i_, v in enumerate(gs.all_goods):
            self.tw_goods.insert('', i_, values=v)

    #  商品viewTree
    def tw_goods(self):
        return self.tw_goods

    # 商品信息
    def goods_info(self, goods_info=gs.all_goods):
        self.goods_info = goods_info
        return self.goods_info


class InMoney:
    def __init__(self, parent, master):
        self.master = master
        self.parent = parent
        self.la_mon_tittle()
        self.en_mon = self.en_user_mon()
        self.btn_enter = self.btn_mon()

    def la_mon_tittle(self):
        la_in_tittle = tk.Label(self.parent, text='enter your money')
        la_in_tittle.place(x=30, y=30)
        return la_in_tittle

    def en_user_mon(self):
        en_user_money = tk.Entry(self.parent)
        en_user_money.place(x=30, y=60)
        return en_user_money

    def btn_mon(self):
        btn_enter = tk.Button(self.parent, text='enter',
                              command=self.btn_mon_function)
        btn_enter.place(x=115, y=90)
        return btn_enter

    def btn_mon_function(self):
        user_money = self.en_mon.get()

        if user_money.isnumeric():
            #  销毁输入金额的frame
            self.parent.destroy()
            self.master.geometry('440x260')
        else:
            self.en_mon.delete(0, len(user_money))
            tk.Label(self.parent, text='invalid input!').place(x=30, y=90)
            return


class Choose:
    def __init__(self, master):
        self.master = master
        self.la_id = tk.Label(self.master, text='Id of goods').place(x=310, y=70)
        self.la_quantity = tk.Label(self.master, text='Quantity of goods').place(x=310, y=120)
        self.en_in_id = self.en_in_id()
        self.en_in_quantity = self.en_in_quantity()
        self.btn_purchase = self.btn_purchase()
        pass

    def en_in_id(self):
        en_user_choose_id = tk.Entry(self.master, width=15)
        en_user_choose_id.place(x=310, y=95)
        return en_user_choose_id

    def en_in_quantity(self):
        en_user_choose_quantity = tk.Entry(self.master, width=15)
        en_user_choose_quantity.place(x=310, y=145)
        return en_user_choose_quantity

    def btn_purchase(self):
        btn_purchase = tk.Button(self.master, text='Purchase', command=self.__purchase)
        btn_purchase.place(x=310, y=170)
        return btn_purchase

    #  警告文字 如果用户输入的id不正确 要定义在按钮出发的方法内而不能在方法的方法内 会不更新数据
    def __purchase(self):
        in_id = self.en_in_id.get()
        in_qua = self.en_in_quantity.get()

        #  非法输入的警告Label
        # if int(in_id) in [good_id[0] for good_id in module.info_of_goods()]:
        #     module.s_var_warning.set('')
        #     module.tw_carts.insert('', 'end', values=(in_id, in_qua))
        # else:
        #     module.s_var_warning.set('invalid input\nenter again')

        #  清空输入框
        self.en_in_id.delete(0, len(in_id))
        self.en_in_quantity.delete(0, len(in_qua))


def root():
    win_ = tk.Tk()
    win_.geometry('200x200')
    return win_


def fm_(win):
    new_fm = tk.Frame(win, height=300, width=300, bd=3)
    new_fm.place(x=0, y=35)
    return new_fm
