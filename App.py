# -*- coding: utf-8 -*-
import threading
import requests
from mttkinter import mtTkinter as mtk
from tkinter import scrolledtext, END, Frame, Tk
from tkinter.messagebox import showerror, showinfo
from datetime import datetime
import calendar
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import time
import os

datetime = calendar.datetime.datetime
timedelta = calendar.datetime.timedelta


class LoginPage(object):
    def __init__(self, master=None):
        self.loginPage = master
        self.loginPage.title("天兆房产")
        self.loginPage.geometry("370x340")
        self.createPage()

    def createPage(self):
        self.loginBox = mtk.LabelFrame(self.loginPage, text="账号登录", fg="blue")
        self.loginBox.place(x=30, y=30, width=300, height=280)

        self.userName = mtk.Label(self.loginBox, text="账号：")
        self.userName.place(x=20, y=20, width=50, height=30)
        self.userNameText = mtk.Entry(self.loginBox)
        self.userNameText.place(x=90, y=20, width=150, height=30)

        self.passWord = mtk.Label(self.loginBox, text="密码：")
        self.passWord.place(x=20, y=70, width=50, height=30)
        self.passWordText = mtk.Entry(self.loginBox)
        self.passWordText.place(x=90, y=70, width=150, height=30)

        # self.keyValue = mtk.Label(self.loginBox, text="KEY：")
        # self.keyValue.place(x=20, y=120, width=50, height=30)
        self.keyValueText = mtk.Entry(self.loginBox, show="*")
        self.keyValueText.place(x=90, y=120, width=150, height=30)

        self.loginBtn = mtk.Button(self.loginBox, text="登录", command=lambda: self.thread_it(self.login))
        self.loginBtn.place(x=150, y=180, width=80, height=30)

        self.logoutBtn = mtk.Button(self.loginBox, text="退出", command=lambda: self.thread_it(self.stop))
        self.logoutBtn.place(x=40, y=180, width=80, height=30)

    def checkKey(self):
        self.keyvalue = self.keyValueText.get().strip()
        check_url = "http://zhoulei8.f3322.net:7898/verify"

        response = requests.post(check_url, data={"code": self.keyvalue}, timeout=3).json()
        if response.get("status"):
            return True
        else:
            return False


    def login(self):
        if not self.checkKey():
            showerror("错误信息", "无效的KEY!")
            return

        self.sess = requests.Session()
        self.sess.headers = {
            'Host': 'xzspj.xianghe.gov.cn:8094',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://xzspj.xianghe.gov.cn:8094',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://xzspj.xianghe.gov.cn:8094/WeChat/login/login.html',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4'
        }

        loginname = self.userNameText.get().strip()
        if not loginname:
            showerror("错误信息", "请输入用户名!")
            return
        loginpwd = self.passWordText.get().strip()
        if not loginpwd:
            showerror("错误信息", "请输入密码!")
            return

        loginUrl = "http://xzspj.xianghe.gov.cn:8094/zwmh/servlet/MobileAccessService"
        formData = {
            "action": "GetUserDetailLogin",
            "sys": "V3WeChat",
            "area": "13",
            "loginname": loginname,
            "password": loginpwd,
            "type": "11"
        }
        try:
            response = self.sess.post(loginUrl, data=formData, timeout=5).json()
            # print(response)
            loginMsg = response.get("message")
            if loginMsg == "OK":
                self.loginBox.destroy()
                MainPage(response, self.sess, master=self.loginPage)
            else:
                showerror("错误信息", "用户密码错误!")
        except:
            showerror("错误信息", "登录错误!")


    def stop(self):
        os._exit(0)

    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()


class InputFrame(Frame):
    def __init__(self, response, session, master=None):
        super(InputFrame, self).__init__()
        self.sess = session
        self.CARD_NO = response.get("data")[0].get("CARD_NO")
        self.PHONE = response.get("data")[0].get("PHONE")
        self.NAME = response.get("data")[0].get("NAME")
        self.root = master
        # 设置窗口大小和位置
        self.root.geometry('650x600')
        self.root.title(f"天兆房产 - - 您好, {self.NAME}")
        self.createPage()
        self.uptime()


    def createPage(self):
        self.baseInfo = mtk.LabelFrame(self.root, text="当前用户", fg="blue")
        self.baseInfo.place(x=30, y=50, width=250, height=150)

        self.userName = mtk.Label(self.baseInfo, text="姓 名：")
        self.userName.place(x=20, y=10, width=80, height=25)
        self.userNameText = mtk.Entry(self.baseInfo)
        self.userNameText.place(x=110, y=10, width=100, height=25)
        self.userNameText.insert(0, self.NAME)
        self.userNameText.bind(sequence="<Return>", func=lambda x: self.thread_it(self.updateName))
        self.taskName = mtk.Label(self.baseInfo, text="预约业务：")
        self.taskName.place(x=20, y=45, width=80, height=25)
        self.taskNameText = mtk.Label(self.baseInfo, text="人才引进落户申请")
        self.taskNameText.place(x=110, y=45, width=100, height=25)

        self.seetings = mtk.LabelFrame(self.root, text="设 置", fg="blue")
        self.seetings.place(x=320, y=50, width=250, height=150)

        self.taskDate = mtk.Label(self.seetings, text="预约日期：")
        self.taskDate.place(x=10, y=10, width=80, height=25)
        self.taskDateText = mtk.Entry(self.seetings)
        self.taskDateText.place(x=100, y=10, width=100, height=25)
        self.taskDateText.bind(sequence="<Double-Button-1>", func=lambda x: self.thread_it(self.getDate))

        self.timeChoose = mtk.Label(self.seetings, text="预约时间：")
        self.timeChoose.place(x=10, y=50, width=80, height=25)
        self.timeChooseText = ttk.Combobox(self.seetings)
        self.timeChooseText.place(x=100, y=50, width=100, height=25)
        self.timeChooseText["values"] = ["09:00-12:00", "13:00-70:00"]

        self.taskSleep = mtk.Label(self.seetings, text="延时设置：")
        self.taskSleep.place(x=10, y=90, width=80, height=25)
        self.taskSleepText = mtk.Entry(self.seetings)
        self.taskSleepText.place(x=100, y=90, width=100, height=25)

        self.startBtn = mtk.Button(self.root, text="预约", command=lambda: self.thread_it(self.startTask))
        self.startBtn.place(x=470, y=440, width=100, height=30)

        self.stopBtn = mtk.Button(self.root, text="暂停", command=lambda: self.thread_it(self.stop))
        self.stopBtn.place(x=470, y=490, width=100, height=30)

        self.timeNow = mtk.LabelFrame(self.root, text="当前时间：", fg="blue")
        self.timeNow.place(x=450, y=270, width=150, height=120)

        self.timeNowText = mtk.Label(self.timeNow, fg="green")
        self.timeNowText.place(x=20, y=20, width=110, height=60)
        self.timeNowText["text"] = datetime.now().strftime('%Y-%m-%d \n\n %H:%M:%S')

        self.logInfo = mtk.LabelFrame(self.root, text="日志信息", fg="blue")
        self.logInfo.place(x=30, y=230, width=400, height=350)

        self.logTxt = scrolledtext.ScrolledText(self.logInfo, fg="green")
        self.logTxt.place(x=20, y=15, width=360, height=290)

    def uptime(self):
        self.timeNowText["text"] = datetime.now().strftime('%Y-%m-%d \n\n %H:%M:%S')
        self.root.after(100, self.uptime)

    def updateName(self):
        newName = self.userNameText.get().strip()
        self.NAME = newName
        self.root.title(f"天兆房产 - - 您好, {self.NAME}")

    def updateSleep(self):
        try:
            self.timeSleep = float(self.taskSleepText.get().strip())

        except:
            showerror("错误信息", "请输入正确的时间!")

    def getDate(self):
        for date in [Calendar().selection()]:
            if date:
                self.taskDateText.insert(0, date)

    def startTask(self):
        self.status = True
        self.workOn = False
        self.tokenStatus = True
        self.token = False
        taskDate = self.taskDateText.get().strip()
        if not taskDate:
            showerror("错误提示", "请选择预约日期!")
            return
        taskTime = self.timeChooseText.get().strip()
        if not taskTime:
            showerror("错误提示", "请选择预约时间!")
            return
        try:
            sleep1 = self.taskSleepText.get().strip()
            if not sleep1:
                self.timeSleep = 1
            else:
                self.timeSleep = float(sleep1)
        except:
            showerror("错误信息", "请输入正确的时间!")
            return

        while not self.token:
            try:
                url = "http://xzspj.xianghe.gov.cn:8094/zwmh/servlet/MobileAccessService?action=yyGetToken&methodType=POST&sys=V3WeChat&area=161&yyArgs={%22Service%22:%22QueueCity.Login%22,%22account%22:%22xhadmin%22,%22password%22:%2274a216f24d7bd7a89254f76dac76b119%22}"
                response = self.sess.get(url, timeout=10).json()
                token = response.get("token")
                if token:
                    self.token = True
                else:
                    self.logTxt.insert(END,
                                       f"{datetime.now().strftime('%Y:%m:%d %H:%M:%S')}\t\t{response.get('errors')[0].get('message')}.\n")
                    self.logTxt.yview_moveto(1.0)
            except:
                continue

        # while not self.workOn:
        #     try:
        #         check_url = "http://xzspj.xianghe.gov.cn:8094/zwmh/servlet/MobileAccessService?action=yyGetDepartList&methodType=POST&sys=V3WeChat&area=161&yyArgs={%22Service%22:%22Queue.GetBizDepts%22,%22Reserve%22:true,%22token%22:%22TOKEN%22}"
        #         url = check_url.replace("TOKEN", token)
        #         response = self.sess.get(url, timeout=10).json()
        #         # print(2222, response)
        #         result = response.get("Succ")
        #         if "true" in result:
        #             self.workOn = True
        #             url = "http://xzspj.xianghe.gov.cn:8094/zwmh/servlet/MobileAccessService?action=yyListBusiness&methodType=POST&sys=V3WeChat&area=161&yyArgs={%22Service%22:%22Reserve.ListBusiness%22,%20%22Date%22:%22DATE%22,%20%22DeptName%22:%22%E5%85%AC%E5%AE%89%E5%B1%80%22,%22token%22:%22TOKEN%22}"
        #             url = url.replace("TOKEN", token).replace("DATE", taskDate)
        #             response = self.sess.get(url).json()
        #             BizID = response.get("Biz")[0].get("BizID")
        #             BizName = response.get("Biz")[0].get("BizName")
        #             ITEM_CODE = response.get("Biz")[0].get("ItemList")[0].get("ITEM_CODE")
        #             ITEM_NAME = response.get("Biz")[0].get("ItemList")[0].get("ITEM_NAME")
        #         else:
        #             msg = response.get('Msg').strip('。')
        #             if msg:
        #                 self.logTxt.insert(END,
        #                                    f"{datetime.now().strftime('%Y:%m:%d %H:%M:%S')}\t\t{msg}.\n")
        #                 self.logTxt.yview_moveto(1.0)
        #             else:
        #                 self.logTxt.insert(END,
        #                                    f"{datetime.now().strftime('%Y:%m:%d %H:%M:%S')}\t\t{response.get('errors')[0].get('message')}.\n")
        #                 self.logTxt.yview_moveto(1.0)
        #     except Exception as e:
        #         print(e.args)
        #         continue
        #
        #     time.sleep(self.timeSleep)

        while self.tokenStatus:
            try:
                url = "http://xzspj.xianghe.gov.cn:8094/zwmh/servlet/MobileAccessService?action=yyListBusiness&methodType=POST&sys=V3WeChat&area=161&yyArgs={%22Service%22:%22Reserve.ListBusiness%22,%20%22Date%22:%22DATE%22,%20%22DeptName%22:%22%E5%85%AC%E5%AE%89%E5%B1%80%22,%22token%22:%22TOKEN%22}"
                url = url.replace("TOKEN", token).replace("DATE", taskDate)
                response = self.sess.get(url, timeout=10).json()
                if response.get("Succ") == "true":
                    BizID = response.get("Biz")[0].get("BizID")
                    BizName = response.get("Biz")[0].get("BizName")
                    ITEM_CODE = response.get("Biz")[0].get("ItemList")[0].get("ITEM_CODE")
                    ITEM_NAME = response.get("Biz")[0].get("ItemList")[0].get("ITEM_NAME")
                    self.tokenStatus = False

                if response.get("errors"):
                    self.logTxt.insert(END,
                                       f"{datetime.now().strftime('%Y:%m:%d %H:%M:%S')}\t\t{response.get('errors')[0].get('message')}.\n")
                    self.logTxt.yview_moveto(1.0)
            except:
                continue

        while self.status:
            try:
                url = "http://xzspj.xianghe.gov.cn:8094/zwmh/servlet/MobileAccessService?action=yyAddRecord&sys=V3WeChat&area=161&methodType=POST&yyArgs={%22BizID%22:%22BIZID%22,%22BizName%22:%22BIZNAME%22,%22DeptName%22:%22%E5%85%AC%E5%AE%89%E5%B1%80%22,%22ITEM_CODE%22:%22ITEMCODE%22,%22ITEM_NAME%22:%22ITEMNAME%22,%22Date%22:%22TASKDATE%22,%22Time%22:%22TASKTIME0%22,%22DateTime%22:%22TASKDATE%20TASKTIME1%22,%22token%22:%22TOKEN%22,%22IDCard%22:%22IDCARDNO%22,%22WeChat%22:%22PHONENO%22,%22Phone%22:%22PHONENO%22,%22PersonName%22:%22USERNAME%22,%22ENTNAME%22:%22%22,%22Service%22:%22Reserve.AddRecord%22}"
                url = url.replace("BIZID", BizID)
                url = url.replace("BIZNAME", BizName)
                url = url.replace("ITEMCODE", ITEM_CODE)
                url = url.replace("ITEMNAME", ITEM_NAME)
                url = url.replace("TASKDATE", taskDate)
                url = url.replace("TASKTIME0", taskTime.split('-')[0])
                url = url.replace("TASKTIME1", taskTime)
                url = url.replace("TOKEN", token)
                url = url.replace("IDCARDNO", self.CARD_NO)
                url = url.replace("PHONENO", self.PHONE)
                url = url.replace("USERNAME", self.NAME)
                response = self.sess.get(url, timeout=10)
                # print(44444, response.text)
                if "预约失败" in response.text:
                    self.logTxt.insert(END,
                                       f"{datetime.now().strftime('%Y:%m:%d %H:%M:%S')}\t\t{response.json().get('Msg').strip('。')}.\n")
                    self.logTxt.yview_moveto(1.0)
                elif response.json().get("errors"):
                    self.logTxt.insert(END,
                                        f"{datetime.now().strftime('%Y:%m:%d %H:%M:%S')}\t\t{response.json().get('errors')[0].get('message')}.\n")
                    self.logTxt.yview_moveto(1.0)

                else:
                    self.status = False
                    showinfo("提示信息", "预约成功!")
                time.sleep(self.timeSleep)
            except:
                continue

    def stop(self):
        self.workOn = True
        self.status = False

    def out(self):
        os._exit(0)

    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()


class MainPage(object):
    def __init__(self, response, session, master=None):
        self.root = master
        self.root.geometry('%dx%d' % (1025, 500))
        self.createPage(response, session)

    def createPage(self, response, session):
        self.inputPage = InputFrame(response, session, self.root)

        self.inputPage.pack()

    def inputData(self):
        self.inputPage.pack()



class Calendar:

    def __init__(s, point=None, position=None):
        # point    提供一个基点，来确定窗口位置
        # position 窗口在点的位置 'ur'-右上, 'ul'-左上, 'll'-左下, 'lr'-右下
        # s.master = tk.Tk()
        s.master = tk.Toplevel()
        s.master.withdraw()
        fwday = calendar.SUNDAY

        year = datetime.now().year
        month = datetime.now().month
        locale = None
        sel_bg = '#ecffc4'
        sel_fg = '#05640e'

        s._date = datetime(year, month, 1)
        s._selection = None  # 设置为未选中日期

        s.G_Frame = ttk.Frame(s.master)

        s._cal = s.__get_calendar(locale, fwday)

        s.__setup_styles()  # 创建自定义样式
        s.__place_widgets()  # pack/grid 小部件
        s.__config_calendar()  # 调整日历列和安装标记
        # 配置画布和正确的绑定，以选择日期。
        s.__setup_selection(sel_bg, sel_fg)

        # 存储项ID，用于稍后插入。
        s._items = [s._calendar.insert('', 'end', values='') for _ in range(6)]

        # 在当前空日历中插入日期
        s._update()

        s.G_Frame.pack(expand=1, fill='both')
        s.master.overrideredirect(1)
        s.master.update_idletasks()
        width, height = s.master.winfo_reqwidth(), s.master.winfo_reqheight()
        if point and position:
            if position == 'ur':
                x, y = point[0], point[1] - height
            elif position == 'lr':
                x, y = point[0], point[1]
            elif position == 'ul':
                x, y = point[0] - width, point[1] - height
            elif position == 'll':
                x, y = point[0] - width, point[1]
        else:
            x, y = (s.master.winfo_screenwidth() - width) / 2, (s.master.winfo_screenheight() - height) / 2
        s.master.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中
        s.master.after(300, s._main_judge)
        s.master.deiconify()
        s.master.focus_set()
        s.master.wait_window()  # 这里应该使用wait_window挂起窗口，如果使用mainloop,可能会导致主程序很多错误

    def __get_calendar(s, locale, fwday):
        # 实例化适当的日历类
        if locale is None:
            return calendar.TextCalendar(fwday)
        else:
            return calendar.LocaleTextCalendar(fwday, locale)

    def __setitem__(s, item, value):
        if item in ('year', 'month'):
            raise AttributeError("attribute '%s' is not writeable" % item)
        elif item == 'selectbackground':
            s._canvas['background'] = value
        elif item == 'selectforeground':
            s._canvas.itemconfigure(s._canvas.text, item=value)
        else:
            s.G_Frame.__setitem__(s, item, value)

    def __getitem__(s, item):
        if item in ('year', 'month'):
            return getattr(s._date, item)
        elif item == 'selectbackground':
            return s._canvas['background']
        elif item == 'selectforeground':
            return s._canvas.itemcget(s._canvas.text, 'fill')
        else:
            r = ttk.tclobjs_to_py({item: ttk.Frame.__getitem__(s, item)})
            return r[item]

    def __setup_styles(s):
        # 自定义TTK风格
        style = ttk.Style(s.master)
        arrow_layout = lambda dir: (
            [('Button.focus', {'children': [('Button.%sarrow' % dir, None)]})]
        )
        style.layout('L.TButton', arrow_layout('left'))
        style.layout('R.TButton', arrow_layout('right'))

    def __place_widgets(s):
        # 标头框架及其小部件
        Input_judgment_num = s.master.register(s.Input_judgment)  # 需要将函数包装一下，必要的
        hframe = ttk.Frame(s.G_Frame)
        gframe = ttk.Frame(s.G_Frame)
        bframe = ttk.Frame(s.G_Frame)
        hframe.pack(in_=s.G_Frame, side='top', pady=5, anchor='center')
        gframe.pack(in_=s.G_Frame, fill=tk.X, pady=5)
        bframe.pack(in_=s.G_Frame, side='bottom', pady=5)

        lbtn = ttk.Button(hframe, style='L.TButton', command=s._prev_month)
        lbtn.grid(in_=hframe, column=0, row=0, padx=12)
        rbtn = ttk.Button(hframe, style='R.TButton', command=s._next_month)
        rbtn.grid(in_=hframe, column=5, row=0, padx=12)

        s.CB_year = ttk.Combobox(hframe, width=5, values=[str(year) for year in
                                                          range(datetime.now().year, datetime.now().year - 11, -1)],
                                 validate='key', validatecommand=(Input_judgment_num, '%P'))
        s.CB_year.current(0)
        s.CB_year.grid(in_=hframe, column=1, row=0)
        s.CB_year.bind('<KeyPress>', lambda event: s._update(event, True))
        s.CB_year.bind("<<ComboboxSelected>>", s._update)
        tk.Label(hframe, text='年', justify='left').grid(in_=hframe, column=2, row=0, padx=(0, 5))

        s.CB_month = ttk.Combobox(hframe, width=3, values=['%02d' % month for month in range(1, 13)], state='readonly')
        s.CB_month.current(datetime.now().month - 1)
        s.CB_month.grid(in_=hframe, column=3, row=0)
        s.CB_month.bind("<<ComboboxSelected>>", s._update)
        tk.Label(hframe, text='月', justify='left').grid(in_=hframe, column=4, row=0)

        # 日历部件
        s._calendar = ttk.Treeview(gframe, show='', selectmode='none', height=7)
        s._calendar.pack(expand=1, fill='both', side='bottom', padx=5)

        ttk.Button(bframe, text="确 定", width=6, command=lambda: s._exit(True)).grid(row=0, column=0, sticky='ns',
                                                                                    padx=20)
        ttk.Button(bframe, text="取 消", width=6, command=s._exit).grid(row=0, column=1, sticky='ne', padx=20)

        tk.Frame(s.G_Frame, bg='#565656').place(x=0, y=0, relx=0, rely=0, relwidth=1, relheigh=2 / 200)
        tk.Frame(s.G_Frame, bg='#565656').place(x=0, y=0, relx=0, rely=198 / 200, relwidth=1, relheigh=2 / 200)
        tk.Frame(s.G_Frame, bg='#565656').place(x=0, y=0, relx=0, rely=0, relwidth=2 / 200, relheigh=1)
        tk.Frame(s.G_Frame, bg='#565656').place(x=0, y=0, relx=198 / 200, rely=0, relwidth=2 / 200, relheigh=1)

    def __config_calendar(s):
        # cols = s._cal.formatweekheader(3).split()
        cols = ['日', '一', '二', '三', '四', '五', '六']
        s._calendar['columns'] = cols
        s._calendar.tag_configure('header', background='grey90')
        s._calendar.insert('', 'end', values=cols, tag='header')
        # 调整其列宽
        font = tkFont.Font()
        maxwidth = max(font.measure(col) for col in cols)
        for col in cols:
            s._calendar.column(col, width=maxwidth, minwidth=maxwidth,
                               anchor='center')

    def __setup_selection(s, sel_bg, sel_fg):
        def __canvas_forget(evt):
            canvas.place_forget()
            s._selection = None

        s._font = tkFont.Font()
        s._canvas = canvas = tk.Canvas(s._calendar, background=sel_bg, borderwidth=0, highlightthickness=0)
        canvas.text = canvas.create_text(0, 0, fill=sel_fg, anchor='w')

        canvas.bind('<Button-1>', __canvas_forget)
        s._calendar.bind('<Configure>', __canvas_forget)
        s._calendar.bind('<Button-1>', s._pressed)

    def _build_calendar(s):
        year, month = s._date.year, s._date.month

        # update header text (Month, YEAR)
        header = s._cal.formatmonthname(year, month, 0)

        # 更新日历显示的日期
        cal = s._cal.monthdayscalendar(year, month)
        for indx, item in enumerate(s._items):
            week = cal[indx] if indx < len(cal) else []
            fmt_week = [('%02d' % day) if day else '' for day in week]
            s._calendar.item(item, values=fmt_week)

    def _show_select(s, text, bbox):
        """为新的选择配置画布。"""
        x, y, width, height = bbox

        textw = s._font.measure(text)

        canvas = s._canvas
        canvas.configure(width=width, height=height)
        canvas.coords(canvas.text, (width - textw) / 2, height / 2 - 1)
        canvas.itemconfigure(canvas.text, text=text)
        canvas.place(in_=s._calendar, x=x, y=y)

    def _pressed(s, evt=None, item=None, column=None, widget=None):
        """在日历的某个地方点击。"""
        if not item:
            x, y, widget = evt.x, evt.y, evt.widget
            item = widget.identify_row(y)
            column = widget.identify_column(x)

        if not column or not item in s._items:
            # 在工作日行中单击或仅在列外单击。
            return

        item_values = widget.item(item)['values']
        if not len(item_values):  # 这个月的行是空的。
            return

        text = item_values[int(column[1]) - 1]
        if not text:  # 日期为空
            return

        bbox = widget.bbox(item, column)
        if not bbox:  # 日历尚不可见
            s.master.after(20, lambda: s._pressed(item=item, column=column, widget=widget))
            return

        # 更新，然后显示选择
        text = '%02d' % text
        s._selection = (text, item, column)
        s._show_select(text, bbox)

    def _prev_month(s):
        """更新日历以显示前一个月。"""
        s._canvas.place_forget()
        s._selection = None

        s._date = s._date - timedelta(days=1)
        s._date = datetime(s._date.year, s._date.month, 1)
        s.CB_year.set(s._date.year)
        s.CB_month.set(s._date.month)
        s._update()

    def _next_month(s):
        """更新日历以显示下一个月。"""
        s._canvas.place_forget()
        s._selection = None

        year, month = s._date.year, s._date.month
        s._date = s._date + timedelta(
            days=calendar.monthrange(year, month)[1] + 1)
        s._date = datetime(s._date.year, s._date.month, 1)
        s.CB_year.set(s._date.year)
        s.CB_month.set(s._date.month)
        s._update()

    def _update(s, event=None, key=None):
        """刷新界面"""
        if key and event.keysym != 'Return': return
        year = int(s.CB_year.get())
        month = int(s.CB_month.get())
        if year == 0 or year > 9999: return
        s._canvas.place_forget()
        s._date = datetime(year, month, 1)
        s._build_calendar()  # 重建日历

        if year == datetime.now().year and month == datetime.now().month:
            day = datetime.now().day
            for _item, day_list in enumerate(s._cal.monthdayscalendar(year, month)):
                if day in day_list:
                    item = 'I00' + str(_item + 2)
                    column = '#' + str(day_list.index(day) + 1)
                    s.master.after(100, lambda: s._pressed(item=item, column=column, widget=s._calendar))

    def _exit(s, confirm=False):
        """退出窗口"""
        if not confirm: s._selection = None
        s.master.destroy()

    def _main_judge(s):
        """判断窗口是否在最顶层"""
        try:
            # s.master 为 TK 窗口
            # if not s.master.focus_displayof(): s._exit()
            # else: s.master.after(10, s._main_judge)

            # s.master 为 toplevel 窗口
            if s.master.focus_displayof() == None or 'toplevel' not in str(s.master.focus_displayof()):
                s._exit()
            else:
                s.master.after(10, s._main_judge)
        except:
            s.master.after(10, s._main_judge)

        # s.master.tk_focusFollowsMouse() # 焦点跟随鼠标

    def selection(s):
        """返回表示当前选定日期的日期时间。"""
        if not s._selection: return None

        year, month = s._date.year, s._date.month
        return str(datetime(year, month, int(s._selection[0])))[:10]

    def Input_judgment(s, content):
        """输入判断"""
        # 如果不加上==""的话，就会发现删不完。总会剩下一个数字
        if content.isdigit() or content == "":
            return True
        else:
            return False


if __name__ == '__main__':
    root = Tk()
    root.title('天兆房产')
    LoginPage(root)
    root.mainloop()

