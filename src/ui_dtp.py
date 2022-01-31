#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk
import dtp_database as dtp
import _sql_utils as sql

class DTP_UI:
    result_index = 0

    # TODO: Populate these from the DB instead. Not high priority, they're unlikely to change.
    typecodes = ('', '1C', '1D', '1S', '24', '25', '27', '2C', '2D', '2L', '2P', '2R', '2S', '2T',
                 '34', '35', '37', '3A', '3C', '3D', '3L', '3P', '3R', '3S', '3T', '4A', '4D',
                 '4L', '4P', '4R', '4S', '4T', 'SP')
    typedesc = ('', '1 AXLE CENTRE DRAW-BAR', '1 AXLE DRAWBAR TRAILER', '1 AXLE SEMI-TRAILER', '2 AXLE CLASS IV',
                '2 AXLE CLASS V', '2 AXLE CLASS VII', '2 AXLE CENTRE DRAW-BAR', '2 AXLE DRAWBAR TRAILER',
                '2 AXLE LIGHT MOTOR CAR', '2 AXLE PSV', '2 AXLE RIGID HGV', '2 AXLE SEMI-TRAILER',
                '2 AXLE TRACTOR UNIT', '3 AXLE CLASS IV', '3 AXLE CLASS V', '3 AXLE CLASS VII',
                '3 AXLE ARTICULATED PSV', '3 AXLE CENTRE DRAW-BAR', '3 AXLE DRAWBAR TRAILER', '3 AXLE LIGHT MOTOR CAR',
                '3 AXLE PSV', '3 AXLE RIGID HGV', '3 AXLE SEMI-TRAILER', '3 AXLE TRACTOR UNIT', '4 AXLE ARTICULATED PSV',
                '4 AXLE DRAWBAR TRAILER', '4 AXLE LIGHT MOTOR CAR', '4 AXLE PSV', '4 AXLE RIGID HGV',
                '4 AXLE SEMI-TRAILER', '4 AXLE TRACTOR UNIT', 'SPECIAL PURPOSE VEHICLE/TRAILER')
    vehmakes = []
    vehmakes_ids = []

    def __init__(self, root_win):
        global result_dtp_disp
        global result_make_disp
        global result_type_disp
        global result_gvw_disp
        global result_gtw_disp
        global result_ax1_disp
        global result_ax2_disp
        global result_ax3_disp
        global result_ax4_disp
        global result_ax5_disp
        global result_brk_rtn_srv
        global result_brk_typ_srv
        global result_brk_rtn_sec
        global result_brk_typ_sec
        global result_brk_rtn_park
        global result_brk_typ_park
        global index_disp
        global srch_type

        root_win.title("dtp-base")
        menubar = tk.Menu(root_win)
        root_win['menu'] = menubar

        # Take away the option to pull menus off into their own little window.
        # Weird old Motif-style behaviour that nothing even vaguely recent does.
        root_win.option_add('*tearOff', tk.FALSE)

        menu_main=tk.Menu(menubar)
        menu_main.add_command(label='Quit', command=self.dtp_ui_quit)
        menubar.add_cascade(menu=menu_main, label='Main')
        menu_help=tk.Menu(menubar, name='help')
        menu_help.add_command(label='About', command=self.dtp_ui_about)
        menubar.add_cascade(menu=menu_help, label='Help')

        root_frame = ttk.Frame(root_win, padding="3 3 12 12", height=600, width=800)
        root_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        root_win.columnconfigure(0, weight=1)
        root_win.rowconfigure(0, weight=1)
        root_frame.columnconfigure(0, weight=1)

        n = ttk.Notebook(root_frame)
        search_frame=ttk.Frame(n)
        n.add(search_frame, text='Search')
        adv_search_frame=ttk.Frame(n)
        n.add(adv_search_frame, text='Advanced Search')
        results_frame=ttk.Frame(n)
        n.add(results_frame, text='Results')
        n.grid(sticky='nsew')

        result_dtp_disp = tk.StringVar()
        result_make_disp = tk.StringVar()
        result_type_disp = tk.StringVar()
        result_gvw_disp = tk.StringVar()
        result_gtw_disp = tk.StringVar()
        result_ax1_disp = tk.StringVar()
        result_ax2_disp = tk.StringVar()
        result_ax3_disp = tk.StringVar()
        result_ax4_disp = tk.StringVar()
        result_ax5_disp = tk.StringVar()
        result_brk_rtn_srv = tk.StringVar()
        result_brk_typ_srv = tk.StringVar()
        result_brk_rtn_sec = tk.StringVar()
        result_brk_typ_sec = tk.StringVar()
        result_brk_rtn_park = tk.StringVar()
        result_brk_typ_park = tk.StringVar()
        index_disp = tk.StringVar()

        ## Search frame

        ttk.Label(search_frame, text="DTp Number:").grid(column=1, row=1, sticky=(tk.W, tk.E))

        self.dtp_input = tk.StringVar()
        dtp_entry = ttk.Entry(search_frame, width=8, textvariable=self.dtp_input)
        dtp_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

        ttk.Button(search_frame, text="Go", command=self.dtp_numsearch).grid(column=3, row=1, sticky=tk.W)

        self.resultcount=tk.StringVar()
        self.resultcount.set("0")
        ttk.Label(search_frame, textvariable=self.resultcount).grid(column=1, row=2, sticky=tk.E)
        ttk.Label(search_frame, text="results found.").grid(column=2, row=2, sticky=(tk.W, tk.E))

        ttk.Button(search_frame, text="Advanced Search", command=lambda: n.select(adv_search_frame)).grid(column = 2, row=3, sticky=(tk.W, tk.E))
        for child in search_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        search_frame.columnconfigure(2, weight=1)

        ## Advanced Search frame

        self.srch_manufacturer = tk.StringVar()
        self.srch_type = tk.StringVar()
        self.srch_gvw = tk.StringVar()


        ttk.Label(adv_search_frame, text="Manufacturer").grid(row=2, column=1, sticky=(tk.W, tk.E))
        self.manufcombo = ttk.Combobox(adv_search_frame, width=20, textvariable=self.srch_manufacturer, state="readonly",
                     postcommand = self.update_manuflist)
        self.manufcombo.grid(row=2, column=2, sticky=(tk.W, tk.E))
        ttk.Label(adv_search_frame, text="Type").grid(row=3, column=1, sticky=(tk.W, tk.E))
        ttk.Combobox(adv_search_frame, textvariable=self.srch_type, state="readonly", values=self.typedesc).grid(row=3, column=2, sticky=(tk.W, tk.E))
        ttk.Label(adv_search_frame, text="GVW (kg)").grid(row=4, column=1, sticky=(tk.W, tk.E))
        ttk.Entry(adv_search_frame, width=20, textvariable=self.srch_gvw).grid(row=4, column=2, sticky=(tk.W, tk.E))

        ttk.Label(adv_search_frame, textvariable=self.resultcount).grid(row=19, column=1, sticky=tk.E)
        ttk.Label(adv_search_frame, text="results found.").grid(row=19, column=2, sticky=(tk.W, tk.E))

        ttk.Button(adv_search_frame, text="Search", command=self.advancedsearch).grid(row=20, column=2, sticky=(tk.W, tk.E))

        for child in adv_search_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        adv_search_frame.columnconfigure(2, weight=1)

        ## Results frame

        ttk.Label(results_frame, text='DTP No.').grid(row=1, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_dtp_disp).grid(row=1, column=2, columnspan=2, sticky=tk.W)
        ttk.Label(results_frame, text='Make').grid(row=2, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=20, textvariable=result_make_disp).grid(row=2, column=2, columnspan=2, sticky=tk.W)
        ttk.Label(results_frame, text='Type').grid(row=3, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=20, textvariable=result_type_disp).grid(row=3, column=2, columnspan=2, sticky=tk.W)
        ttk.Label(results_frame, text='GVW (kg)').grid(row=4, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_gvw_disp).grid(row=4, column=2, columnspan=2, sticky=tk.W)

        ttk.Label(results_frame, text='GTW (kg)').grid(row=4, column=3, sticky=tk.W)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_gtw_disp).grid(row=4, column=4, columnspan=2, sticky=tk.W)

        ttk.Label(results_frame, text='Axle 1 (kg)').grid(row=5, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_ax1_disp).grid(row=5, column=2, columnspan=2, sticky=tk.W)
        ttk.Label(results_frame, text='Axle 2 (kg)').grid(row=6, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_ax2_disp).grid(row=6, column=2, columnspan=2, sticky=tk.W)
        ttk.Label(results_frame, text='Axle 3 (kg)').grid(row=7, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_ax3_disp).grid(row=7, column=2, sticky=tk.W)
        ttk.Label(results_frame, text='Axle 4 (kg)').grid(row=8, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_ax4_disp).grid(row=8, column=2, sticky=tk.W)
        ttk.Label(results_frame, text='Axle 5 (kg)').grid(row=9, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_ax5_disp).grid(row=9, column=2, sticky=tk.W)

        ttk.Label(results_frame, text='Brake Routine').grid(row=10, column=2, sticky=tk.W)
        ttk.Label(results_frame, text='Brake Type').grid(row=10, column=3, sticky=tk.E)

        # Service brake
        ttk.Label(results_frame, text='Service').grid(row=11, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=10, textvariable=result_brk_rtn_srv).grid(row=11, column=2, sticky=tk.W)
        ttk.Label(results_frame, relief='sunken', width=20, textvariable=result_brk_typ_srv).grid(row=11, column=3, columnspan=2, sticky=tk.W)
        # Secondary brake
        ttk.Label(results_frame, text='Secondary').grid(row=12, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=10, textvariable=result_brk_rtn_sec).grid(row=12, column=2, sticky=tk.W)
        ttk.Label(results_frame, relief='sunken', width=20, textvariable=result_brk_typ_sec).grid(row=12, column=3, columnspan=2, sticky=tk.W)
        # Park brake
        ttk.Label(results_frame, text='Parking').grid(row=13, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=10, textvariable=result_brk_rtn_park).grid(row=13, column=2, sticky=tk.W)
        ttk.Label(results_frame, relief='sunken', width=20, textvariable=result_brk_typ_park).grid(row=13, column=3, columnspan=2, sticky=tk.W)

        result_prev_butt = ttk.Button(results_frame, text="Previous", command=self.result_prev).grid(column=1, row=20, sticky=tk.W)
        ttk.Label(results_frame, textvariable=index_disp).grid(row=20, column=2)
        result_next_butt = ttk.Button(results_frame, text="Next", command=self.result_next).grid(column=3, row=20, sticky=tk.E)

        for child in results_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        results_frame.columnconfigure(1, weight=1)
        results_frame.columnconfigure(2, weight=3)

        # Connect to the DB
        dtp.db_connect()
        dtp.get_vehMakes(self.vehmakes, self.vehmakes_ids)

    def result_prev(self, *args):
        if(int(self.resultcount.get()) > 0):
            if(self.result_index > 0):
                self.result_index -= 1

                self.result_update(*args)
        return

    def result_next(self, *args):
        if(int(self.resultcount.get()) > 0):
            if(self.result_index < (int(self.resultcount.get()) - 1)):
                self.result_index += 1

                self.result_update(*args)
        return

    def result_update(self, *args):
        global result_dtp_disp
        global result_make_disp
        global result_type_disp
        global result_gvw_disp
        global result_gtw_disp
        global result_ax1_disp
        global result_ax2_disp
        global result_ax3_disp
        global result_ax4_disp
        global result_ax5_disp
        global result_brk_rtn_srv
        global result_brk_typ_srv
        global result_brk_rtn_sec
        global result_brk_typ_sec
        global result_brk_rtn_park
        global result_brk_typ_park
        global index_disp

        if(int(self.resultcount.get()) > 0):
            found = self.db_results[self.result_index]
            result_dtp_disp.set(found["DTP_Number"])
            result_make_disp.set(found["Make"])
            result_type_disp.set(found["Type"])
            result_gvw_disp.set(found["GVWDesign"])
            if(found["GTWDesign"]):
                result_gtw_disp.set(found["GTWDesign"])
            else:
                result_gtw_disp.set("")
            result_ax1_disp.set(str(found["Axle1Weight"]))
            result_ax2_disp.set(str(found["Axle2Weight"]))
            result_ax3_disp.set(str(found["Axle3Weight"]) if(found["Axle3Weight"]) else "")
            result_ax4_disp.set(str(found["Axle4Weight"]) if(found["Axle4Weight"]) else "")
            result_ax5_disp.set(str(found["Axle5Weight"]) if(found["Axle5Weight"]) else "")

            result_brk_rtn_srv.set(found["BrakeRoutine"][0])
            result_brk_typ_srv.set(found["ServiceType"])
            result_brk_rtn_sec.set(found["BrakeRoutine"][1])
            result_brk_typ_sec.set(found["SecondaryType"])
            result_brk_rtn_park.set(found["BrakeRoutine"][2])
            result_brk_typ_park.set(found["ParkType"])

            index_disp.set(str(self.result_index + 1) + " of " + self.resultcount.get())
        else:
            # Cleanup time!
            result_dtp_disp.set("")
            result_make_disp.set("")
            result_type_disp.set("")
            result_gvw_disp.set("")
            result_gtw_disp.set("")
            result_ax1_disp.set("")
            result_ax2_disp.set("")
            result_ax3_disp.set("")
            result_ax4_disp.set("")
            result_ax5_disp.set("")
            result_brk_rtn_srv.set("")
            result_brk_typ_srv.set("")
            result_brk_rtn_sec.set("")
            result_brk_typ_sec.set("")
            result_brk_rtn_park.set("")
            result_brk_typ_park.set("")
            index_disp.set("No Records")
            self.result_index = 0
        return

    def dtp_numsearch(self, *args):
        self.result_index = 0 # Clear our previous results
        results = dtp.dtp_get(self.dtp_input.get())
        self.resultcount.set(len(results))
        self.db_results = results
        self.result_update(*args)

    def advancedsearch(self, *args):
        typexs = self.srch_type.get()
        typecode = ''
        manufid = ''
        query = sql.Query()
        query.FROM('Master').SELECT('*')

        if (len(typexs) > 0):
            typecode = self.typecodes[self.typedesc.index(typexs)]
            query.WHERE(str('TypeId="' + typecode + '"'))

        if (len(self.srch_manufacturer.get()) > 0):
            manufid = str(self.vehmakes_ids[self.vehmakes.index(self.srch_manufacturer.get())])
            query.WHERE(str('MakeId="' + manufid + '"'))

        if(len(self.srch_gvw.get()) > 0):
            weight = int(self.srch_gvw.get())
            query.WHERE(str('GVW_DesignWeight=' + str(weight/10)))

        tmp = dtp.db_curs.execute(str(query)).fetchall()
        results = []
        for row in tmp:
            results.append(dtp.dtp_rowparse(row))

        self.db_results = results
        self.resultcount.set(len(results))
        self.result_update(*args)
        return

    def dtp_ui_quit(self, *args):
        root_win.destroy()
        return

    def dtp_ui_about(self, *args):
        def dismiss ():
            dlg.grab_release()
            dlg.destroy()

        dlg = tk.Toplevel(root_win)
        dlg.title("About dtp-base")
        ttk.Label(dlg, text="dtp-base: For searching through the DVSA's brake roller test procedure database.\nWritten by Tamber <tamber@furryhelix.co.uk>").grid(row=2, column=1, columnspan=3)
        ttk.Label(dlg, text="DTP Database version:").grid(row=3, column=1)
        ttk.Label(dlg, text=dtp.db_version()[0]).grid(row=3, column=2)
        ttk.Button(dlg, text="Ok", command=dismiss).grid(row=4, column=2)
        dlg.protocol("WM_DELETE_WINDOW", dismiss)
        dlg.transient(root_win)
        dlg.wait_visibility()
        dlg.grab_set()
        dlg.wait_window()
        return

    def dtp_ui_help(self, *args):
        return

    def update_manuflist(self):
        self.manufcombo['values'] = self.vehmakes

if __name__ == "__main__":
    root_win = tk.Tk()
    DTP_UI(root_win)
    root_win.mainloop()
