#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk
import dtp_database as dtp
import _sql_utils as sql
import webbrowser as web
import re

class DTP_UI:
    result_index = 0
    tresult_index = 0

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

    braketypes = []
    braketypes_ids = []

    def __init__(self, root_win):
        global result_dtp_disp
        global result_dtp_suffix
        global result_make_disp
        global result_type_disp
        global result_abs_disp
        global result_lsv_disp
        global result_gvw_disp
        global result_gtw_disp
        global result_ax1_disp
        global result_ax1_mod
        global result_ax2_disp
        global result_ax2_mod
        global result_ax3_disp
        global result_ax3_mod
        global result_ax4_disp
        global result_ax4_mod
        global result_ax5_disp
        global result_ax5_mod
        global result_brk_rtn_srv
        global result_brk_typ_srv
        global result_brk_rtn_sec
        global result_brk_typ_sec
        global result_brk_rtn_park
        global result_brk_typ_park
        global index_disp
        global srch_type

        # and now all the same again but for trailers instead
        global tresult_dtp_disp
        global tresult_type_disp
        global tresult_gvw_disp
        global tresult_taw_disp
        global tresult_ax1_disp
        global tresult_ax1_park
        global tresult_ax2_disp
        global tresult_ax2_park
        global tresult_ax3_disp
        global tresult_ax3_park
        global tresult_ax4_disp
        global tresult_ax4_park
        global tresult_abs_disp
        global tresult_ebs_disp
        global tresult_lsv_disp
        global tresult_typapp_disp
        global tindex_disp

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
        menu_help.add_command(label='Help', command=self.dtp_ui_help)
        menubar.add_cascade(menu=menu_help, label='Help')


        root_frame = ttk.Frame(root_win, padding="3 3 12 12", height=600, width=800)
        root_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        root_win.columnconfigure(0, weight=1)
        root_win.rowconfigure(0, weight=1)
        root_frame.columnconfigure(0, weight=1)

        n = ttk.Notebook(root_frame)
        search_frame=ttk.Frame(n)
        n.add(search_frame, text='Truck Search')
        results_frame=ttk.Frame(n)
        n.add(results_frame, text='Truck Results')
        trailer_frame=ttk.Frame(n)
        n.add(trailer_frame, text='Trailer Search')
        trailer_r_frame=ttk.Frame(n)
        n.add(trailer_r_frame, text='Trailer Results')
        n.grid(sticky='nsew')

        result_dtp_disp = tk.StringVar()
        result_dtp_suffix = tk.StringVar()
        result_make_disp = tk.StringVar()
        result_type_disp = tk.StringVar()
        result_abs_disp = tk.StringVar()
        result_lsv_disp = tk.StringVar()
        result_gvw_disp = tk.StringVar()
        result_gtw_disp = tk.StringVar()
        result_ax1_disp = tk.StringVar()
        result_ax2_disp = tk.StringVar()
        result_ax3_disp = tk.StringVar()
        result_ax4_disp = tk.StringVar()
        result_ax5_disp = tk.StringVar()
        result_ax1_mod = tk.StringVar()
        result_ax2_mod = tk.StringVar()
        result_ax3_mod = tk.StringVar()
        result_ax4_mod = tk.StringVar()
        result_ax5_mod = tk.StringVar()
        result_brk_rtn_srv = tk.StringVar()
        result_brk_typ_srv = tk.StringVar()
        result_brk_rtn_sec = tk.StringVar()
        result_brk_typ_sec = tk.StringVar()
        result_brk_rtn_park = tk.StringVar()
        result_brk_typ_park = tk.StringVar()
        index_disp = tk.StringVar()

        tresult_dtp_disp = tk.StringVar()
        tresult_type_disp = tk.StringVar()
        tresult_gvw_disp = tk.StringVar()
        tresult_taw_disp = tk.StringVar()
        tresult_kpin_disp = tk.StringVar()
        tresult_ax1_disp = tk.StringVar()
        tresult_ax1_park = tk.StringVar()
        tresult_ax2_disp = tk.StringVar()
        tresult_ax2_park = tk.StringVar()
        tresult_ax3_disp = tk.StringVar()
        tresult_ax3_park = tk.StringVar()
        tresult_ax4_disp = tk.StringVar()
        tresult_ax4_park = tk.StringVar()
        tresult_abs_disp = tk.StringVar()
        tresult_ebs_disp = tk.StringVar()
        tresult_lsv_disp = tk.StringVar()
        tresult_typapp_disp = tk.StringVar()
        tindex_disp = tk.StringVar()

                       ########################
                       #     Search frame     #
                       ########################

        ttk.Label(search_frame, text="DTp Number:").grid(column=1, row=1, sticky=(tk.W, tk.E))

        self.dtp_input = tk.StringVar()
        dtp_entry = ttk.Entry(search_frame, width=8, textvariable=self.dtp_input)
        dtp_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

        ttk.Button(search_frame, text="Search", command=self.dtp_numsearch).grid(column=2, row=2, sticky=tk.W)

        self.resultcount=tk.StringVar()
        self.resultcount.set("0")

        self.srch_manufacturer = tk.StringVar()
        self.srch_type = tk.StringVar()
        self.srch_gvw = tk.StringVar()
        self.srch_gtw = tk.StringVar()
        self.srch_srvbrk = tk.StringVar()
        self.srch_secbrk = tk.StringVar()
        self.srch_prkbrk = tk.StringVar()

        ttk.Label(search_frame, textvariable=self.resultcount).grid(row=3, column=1, sticky=tk.E)
        ttk.Label(search_frame, text="results found.").grid(row=3, column=2, sticky=(tk.W, tk.E))


        ttk.Separator(search_frame, orient=tk.HORIZONTAL).grid(row=4, columnspan=4, sticky=(tk.W, tk.E))
        ttk.Label(search_frame, text="Advanced Search").grid(row=5, column=1, columnspan=4)

        ttk.Label(search_frame, text="Manufacturer").grid(row=6, column=1, sticky=(tk.W, tk.E))
        self.manufcombo = ttk.Combobox(search_frame, width=20, textvariable=self.srch_manufacturer, state="readonly",
                     postcommand = self.update_manuflist)
        self.manufcombo.grid(row=6, column=2, sticky=(tk.W, tk.E))
        ttk.Label(search_frame, text="Type").grid(row=7, column=1, sticky=(tk.W, tk.E))
        ttk.Combobox(search_frame, textvariable=self.srch_type, state="readonly", values=self.typedesc).grid(row=7, column=2, sticky=(tk.W, tk.E))
        ttk.Label(search_frame, text="GVW (kg)").grid(row=8, column=1, sticky=(tk.W, tk.E))
        ttk.Entry(search_frame, width=20, textvariable=self.srch_gvw).grid(row=8, column=2, sticky=(tk.W, tk.E))

        ttk.Label(search_frame, text="GTW (kg)").grid(row=9, column=1, sticky=(tk.W, tk.E))
        ttk.Entry(search_frame, width=20, textvariable=self.srch_gtw).grid(row=9, column=2, sticky=(tk.W, tk.E))

        ttk.Label(search_frame, text="Service Brake Type").grid(row=10, column=1, sticky=(tk.W, tk.E))
        self.srvbrktype = ttk.Combobox(search_frame, width=20, textvariable=self.srch_srvbrk, state="readonly",
                                       postcommand = self.update_braketype)
        self.srvbrktype.grid(row=10, column=2, sticky=(tk.W, tk.E))

        ttk.Label(search_frame, text="Secondary Brake Type").grid(row=11, column=1, sticky=(tk.W, tk.E))
        self.secbrktype = ttk.Combobox(search_frame, width=20, textvariable=self.srch_secbrk, state="readonly",
                                       postcommand = self.update_braketype)
        self.secbrktype.grid(row=11, column=2, sticky=(tk.W, tk.E))

        ttk.Label(search_frame, text="Parking Brake Type").grid(row=12, column=1, sticky=(tk.W, tk.E))
        self.prkbrktype = ttk.Combobox(search_frame, width=20, textvariable=self.srch_prkbrk, state="readonly",
                                       postcommand = self.update_braketype)
        self.prkbrktype.grid(row=12, column=2, sticky=(tk.W, tk.E))

        ttk.Label(search_frame, textvariable=self.resultcount).grid(row=19, column=1, sticky=tk.E)
        ttk.Label(search_frame, text="results found.").grid(row=19, column=2, sticky=(tk.W, tk.E))

        ttk.Button(search_frame, text="Search", command=self.advancedsearch).grid(row=20, column=2, sticky=tk.W)
        ttk.Button(search_frame, text="Reset", command=self.advsrchreset).grid(row=20, column=3, sticky=tk.E)

        for child in search_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        search_frame.columnconfigure(2, weight=1)

                       ########################
                       #     Results frame    #
                       ########################

        ttk.Label(results_frame, text='DTP No.').grid(row=1, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_dtp_disp).grid(row=1, column=2, columnspan=2, sticky=tk.W)
        ttk.Label(results_frame, relief='sunken', width=4, textvariable=result_dtp_suffix).grid(row=1, column=4, sticky=tk.W)
        ttk.Label(results_frame, text='Make').grid(row=2, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=20, textvariable=result_make_disp).grid(row=2, column=2, columnspan=2, sticky=tk.W)
        ttk.Label(results_frame, relief='sunken', width=4, textvariable=result_abs_disp).grid(row=2, column=4, sticky=tk.W)
        ttk.Label(results_frame, text='Type').grid(row=3, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=20, textvariable=result_type_disp).grid(row=3, column=2, columnspan=2, sticky=tk.W)
        ttk.Label(results_frame, relief='sunken', width=4, textvariable=result_lsv_disp).grid(row=3, column=4, sticky=tk.W)
        ttk.Label(results_frame, text='GVW (kg)').grid(row=4, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_gvw_disp).grid(row=4, column=2, columnspan=2, sticky=tk.W)

        ttk.Label(results_frame, text='GTW (kg)').grid(row=4, column=3, sticky=tk.W)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_gtw_disp).grid(row=4, column=4, columnspan=2, sticky=tk.W)

        ttk.Label(results_frame, text='Axle 1 (kg)').grid(row=5, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_ax1_disp).grid(row=5, column=2, columnspan=2, sticky=tk.W)
        ttk.Label(results_frame, relief='sunken', width=10, textvariable=result_ax1_mod).grid(row=5, column=3, sticky=tk.W)
        ttk.Label(results_frame, text='Axle 2 (kg)').grid(row=6, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_ax2_disp).grid(row=6, column=2, columnspan=2, sticky=tk.W)
        ttk.Label(results_frame, relief='sunken', width=10, textvariable=result_ax2_mod).grid(row=6, column=3, sticky=tk.W)
        ttk.Label(results_frame, text='Axle 3 (kg)').grid(row=7, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_ax3_disp).grid(row=7, column=2, sticky=tk.W)
        ttk.Label(results_frame, relief='sunken', width=10, textvariable=result_ax3_mod).grid(row=7, column=3, sticky=tk.W)
        ttk.Label(results_frame, text='Axle 4 (kg)').grid(row=8, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_ax4_disp).grid(row=8, column=2, sticky=tk.W)
        ttk.Label(results_frame, relief='sunken', width=10, textvariable=result_ax4_mod).grid(row=8, column=3, sticky=tk.W)
        ttk.Label(results_frame, text='Axle 5 (kg)').grid(row=9, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_ax5_disp).grid(row=9, column=2, sticky=tk.W)
        ttk.Label(results_frame, relief='sunken', width=10, textvariable=result_ax5_mod).grid(row=9, column=3, sticky=tk.W)

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

                       ########################
                       #     Trailer Frame    #
                       ########################

        ttk.Label(trailer_frame, text="DTp Number:").grid(column=1, row=1, sticky=(tk.W, tk.E))
        self.trailer_dtp_input=tk.StringVar()
        trailer_dtp_entry = ttk.Entry(trailer_frame, width=8, textvariable=self.trailer_dtp_input)
        trailer_dtp_entry.grid(column = 2, row=1, sticky=(tk.W, tk.E))

        ttk.Button(trailer_frame, text="Search",
                   command=self.dtp_trailer_numsearch).grid(column=2, row=2, sticky=tk.W)

        for child in trailer_frame.winfo_children():
            child.grid_configure(padx = 5, pady = 5)

        trailer_frame.columnconfigure(1, weight=1)
        trailer_frame.columnconfigure(2, weight=3)


                       ########################
                       #   Trailer Results    #
                       ########################

        ttk.Label(trailer_r_frame, text="DTP No.:").grid(row=1, column=1, sticky=tk.E)
        ttk.Label(trailer_r_frame, relief='sunken', width=8, textvariable=tresult_dtp_disp).grid(row=1,
                                                                                                 column=2,
                                                                                                 columnspan=2,
                                                                                                 sticky=tk.W)

        ttk.Label(trailer_r_frame, text="Type:").grid(row=2, column=1, sticky=tk.E)
        ttk.Label(trailer_r_frame, relief='sunken', width=3, textvariable=tresult_type_disp).grid(row=2,
                                                                                                  column=2,
                                                                                                  columnspan=2,
                                                                                                  sticky=(tk.E, tk.W))

        ttk.Label(trailer_r_frame, text="GVW (kg):").grid(row=3, column=1, sticky=tk.E)
        ttk.Label(trailer_r_frame, relief='sunken', width=8, textvariable=tresult_gvw_disp).grid(row=3,
                                                                                                 column=2,
                                                                                                 columnspan=2,
                                                                                                 sticky=tk.W)

        self.trailer_taw_lbl=ttk.Label(trailer_r_frame, text="TAW (kg):")
        self.trailer_taw_lbl.grid(row=4, column=1, sticky=tk.E)
        ttk.Label(trailer_r_frame, relief='sunken', width=8, textvariable=tresult_taw_disp).grid(row=4,
                                                                                                   column=2,
                                                                                                   sticky=tk.W)

        self.trailer_kpw_lbl=ttk.Label(trailer_r_frame, text="Kingpin Weight (kg):")
        self.trailer_kpw_lbl.grid(row=4, column=3, sticky=tk.E)
        ttk.Label(trailer_r_frame, relief='sunken', width=8, textvariable=tresult_kpin_disp).grid(row=4,
                                                                                                  column=4,
                                                                                                  sticky=tk.W)

        ttk.Label(trailer_r_frame, relief='sunken', width=8, textvariable=tresult_abs_disp).grid(row=5, column=1,
                                                                                                 sticky=tk.E)
        ttk.Label(trailer_r_frame, relief='sunken', width=8, textvariable=tresult_ebs_disp).grid(row=5, column=2,
                                                                                                 sticky=tk.E)
        ttk.Label(trailer_r_frame, relief='sunken', width=8, textvariable=tresult_lsv_disp).grid(row=5, column=3,
                                                                                                 sticky=tk.E)
        ttk.Label(trailer_r_frame, relief='sunken', width=15, textvariable=tresult_typapp_disp).grid(row=5, column=4,
                                                                                                     sticky=tk.E)

        ttk.Separator(trailer_r_frame, orient=tk.HORIZONTAL).grid(row=6, columnspan=5, sticky=(tk.W, tk.E))

        ttk.Label(trailer_r_frame, text="Axle 1 (kg):").grid(row=7, column=1, sticky=tk.E)
        ttk.Label(trailer_r_frame, relief='sunken', width=8, textvariable=tresult_ax1_disp).grid(row=7,
                                                                                                 column=2,
                                                                                                 sticky=tk.W)
        ttk.Label(trailer_r_frame, relief='sunken', width=3, textvariable=tresult_ax1_park).grid(row=7,
                                                                                                 column=3)

        ttk.Label(trailer_r_frame, text="Axle 2 (kg):").grid(row=8, column=1, sticky=tk.E)
        ttk.Label(trailer_r_frame, relief='sunken', width=8, textvariable=tresult_ax2_disp).grid(row=8,
                                                                                                 column=2,
                                                                                                 sticky=tk.W)
        ttk.Label(trailer_r_frame, relief='sunken', width=3, textvariable=tresult_ax2_park).grid(row=8,
                                                                                                 column=3)

        ttk.Label(trailer_r_frame, text="Axle 3 (kg):").grid(row=9, column=1, sticky=tk.E)
        ttk.Label(trailer_r_frame, relief='sunken', width=8, textvariable=tresult_ax3_disp).grid(row=9,
                                                                                                 column=2,
                                                                                                 sticky=tk.W)
        ttk.Label(trailer_r_frame, relief='sunken', width=3, textvariable=tresult_ax3_park).grid(row=9,
                                                                                                 column=3)

        ttk.Label(trailer_r_frame, text="Axle 4 (kg):").grid(row=10, column=1, sticky=tk.E)
        ttk.Label(trailer_r_frame, relief='sunken', width=8, textvariable=tresult_ax4_disp).grid(row=10,
                                                                                                 column=2,
                                                                                                 sticky=tk.W)
        ttk.Label(trailer_r_frame, relief='sunken', width=3, textvariable=tresult_ax4_park).grid(row=10,
                                                                                                 column=3)


        trailer_prev_butt = ttk.Button(trailer_r_frame, text="Previous", command=self.tresult_prev).grid(column=1, row=20, sticky=tk.W)
        ttk.Label(trailer_r_frame, textvariable=index_disp).grid(row=20, column=2)
        trailer_next_butt = ttk.Button(trailer_r_frame, text="Next", command=self.tresult_next).grid(column=3, row=20, sticky=tk.E)

        for child in trailer_r_frame.winfo_children():
            child.grid_configure(padx = 5, pady = 5)

        trailer_r_frame.columnconfigure(1, weight=1)
        trailer_r_frame.columnconfigure(2, weight=1)
        trailer_r_frame.columnconfigure(4, weight=3)

        # Connect to the DB
        dtp.db_connect()
        dtp.get_vehMakes(self.vehmakes, self.vehmakes_ids)
        dtp.get_brakeTypes(self.braketypes, self.braketypes_ids)

    def result_prev(self, *args):
        if(int(self.resultcount.get()) > 0):
            if(self.result_index > 0):
                self.result_index -= 1
            else:
                self.result_index = int(self.resultcount.get()) - 1
            self.result_update(*args)
        return

    def result_next(self, *args):
        if(int(self.resultcount.get()) > 0):
            if(self.result_index < (int(self.resultcount.get()) - 1)):
                self.result_index += 1
            else:
                self.result_index = 0

            self.result_update(*args)
        return

    def tresult_prev(self, *args):
        if(int(self.tresultcount.get()) > 0):
            if(self.tresult_index > 0):
                self.tresult_index -= 1
            else:
                self.tresult_index = int(self.tresultcount.get()) - 1
            self.tresult_update(*args)
        return

    def tresult_next(self, *args):
        if(int(self.tresultcount.get()) > 0):
            if(self.result_index < (int(self.tresultcount.get()) - 1)):
                self.tresult_index += 1
            else:
                self.tresult_index = 0

            self.tresult_update(*args)
        return

    def result_update(self, *args):
        global result_dtp_disp
        global result_dtp_suffix
        global result_make_disp
        global result_type_disp
        global result_abs_disp
        global result_lsv_disp
        global result_gvw_disp
        global result_gtw_disp
        global result_ax1_disp
        global result_ax1_mod
        global result_ax2_disp
        global result_ax2_mod
        global result_ax3_disp
        global result_ax3_mod
        global result_ax4_disp
        global result_ax4_mod
        global result_ax5_disp
        global result_ax5_mod
        global result_brk_rtn_srv
        global result_brk_typ_srv
        global result_brk_rtn_sec
        global result_brk_typ_sec
        global result_brk_rtn_park
        global result_brk_typ_park
        global index_disp

        if(int(self.resultcount.get()) > 0):
            found = self.db_results[self.result_index]
            if(found["Type"] == "Trailer"):
                result_dtp_disp.set(found["DTP_Number"])
                result_dtp_suffix.set("")
                result_make_disp.set("")
                result_abs_disp.set(found["ABSFitted"]);
                result_lsv_disp.set(found["LSVFitted"]);
                result_gvw_disp.set(found["GVWDesign"])
                result_ax1_disp.set(str(found["Axle1Weight"]))
                result_ax1_mod.set("")
                result_ax2_disp.set(str(found["Axle2Weight"]))
                result_ax2_mod.set("")
                result_ax3_disp.set(str(found["Axle3Weight"]))
                result_ax3_mod.set("")
                result_ax4_disp.set(str(found["Axle4Weight"]))
                result_ax4_mod.set("")
                result_ax5_disp.set(str(found["Axle5Weight"]))
                result_ax5_mod.set("")
                result_gtw_disp.set(str(found["AxleWeightTotal"]))
                result_brk_rtn_srv.set(found["BrakeRoutine"][0])
                result_brk_typ_srv.set("")
                result_brk_rtn_sec.set(found["BrakeRoutine"][1])
                result_brk_typ_sec.set("")
                result_brk_rtn_park.set(found["BrakeRoutine"][2])
                result_brk_typ_park.set("")
            else:
                result_dtp_disp.set(found["DTP_Number"])
                result_dtp_suffix.set(found["Suffixes"])
                result_make_disp.set(found["Make"])
                result_abs_disp.set('ABS' if(found["ABSFitted"] == 'Yes') else "")
                result_type_disp.set(found["Type"])
                result_lsv_disp.set('LSV' if(found["LSVFitted"] == 'Yes') else "")
                result_gvw_disp.set(found["GVWDesign"])
                if(found["GTWDesign"]):
                    result_gtw_disp.set(found["GTWDesign"])
                else:
                    result_gtw_disp.set("")
                result_ax1_disp.set(str(found["Axle1Weight"]))
                result_ax1_mod.set('Modulated' if(found["Axle1Modulation"] == 'Yes') else "")
                result_ax2_disp.set(str(found["Axle2Weight"]))
                result_ax2_mod.set('Modulated' if(found["Axle2Modulation"] == 'Yes') else "")
                result_ax3_disp.set(str(found["Axle3Weight"]) if(found["Axle3Weight"]) else "")
                result_ax3_mod.set('Modulated' if(found["Axle3Modulation"] == 'Yes') else "")
                result_ax4_disp.set(str(found["Axle4Weight"]) if(found["Axle4Weight"]) else "")
                result_ax4_mod.set('Modulated' if(found["Axle4Modulation"] == 'Yes') else "")
                result_ax5_disp.set(str(found["Axle5Weight"]) if(found["Axle5Weight"]) else "")
                result_ax5_mod.set('Modulated' if(found["Axle5Modulation"] == 'Yes') else "")

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
            result_ax1_mod.set("")
            result_ax2_disp.set("")
            result_ax2_mod.set("")
            result_ax3_disp.set("")
            result_ax3_mod.set("")
            result_ax4_disp.set("")
            result_ax4_mod.set("")
            result_ax5_disp.set("")
            result_ax5_mod.set("")
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
        self.result_index = 0
        typexs = self.srch_type.get()
        typecode = ''
        manufid = ''
        if(len(typexs)> 0):
            typecode = self.typecodes[self.typedesc.index(typexs)]

        query = sql.Query()

        if(len(typecode) > 0 and re.match("[1234][CDS]", typecode)):
            # Trailer
            query.FROM('TrailerWeights').SELECT('*').WHERE(str('NrAxles=' + str(typecode[0])))
            tmp = dtp.db_curs.execute(str(query)).fetchall()
            results = []
            for row in tmp:
                results.append(dtp.dtp_rowparse_trailer(row))

        else:
            # Truck
            query.FROM('Master').SELECT('*')

            if (len(typexs) > 0):
                query.WHERE(str('TypeId="' + typecode + '"'))

                if (len(self.srch_manufacturer.get()) > 0):
                    manufid = str(self.vehmakes_ids[self.vehmakes.index(self.srch_manufacturer.get())])
                    query.WHERE(str('MakeId="' + manufid + '"'))

                if(len(self.srch_gvw.get()) > 0):
                    weight = int(self.srch_gvw.get())
                    query.WHERE(str('GVW_DesignWeight=' + str(weight/10)))

                if(len(self.srch_gtw.get()) > 0):
                    trainWeight = int(self.srch_gtw.get())
                    query.WHERE(str('GTW_DesignWeight=' + str(trainWeight/10)))

                if(len(self.srch_srvbrk.get()) > 0):
                    brakeType = str(self.braketypes.index(self.srch_srvbrk.get()))
                    query.WHERE(str('FoundServBrake=' + str(self.braketypes_ids[self.braketypes.index(self.srch_srvbrk.get())])))

                if(len(self.srch_prkbrk.get()) > 0):
                    brakeType = str(self.braketypes.index(self.srch_prkbrk.get()))
                    query.WHERE(str('FoundParkBrake=' + str(self.braketypes_ids[self.braketypes.index(self.srch_prkbrk.get())])))

            tmp = dtp.db_curs.execute(str(query)).fetchall()
            results = []
            for row in tmp:
                results.append(dtp.dtp_rowparse(row))

        self.db_results = results
        self.resultcount.set(len(results))
        self.result_update(*args)
        return

    def advsrchreset(self, *args):
        self.srch_manufacturer.set("")
        self.srch_type.set("")
        self.srch_gvw.set("")
        self.srch_gtw.set("")
        self.srch_srvbrk.set("")
        self.srch_secbrk.set("")
        self.srch_prkbrk.set("")
        self.dtp_input.set("")

    def trailersrchreset(self, *args):
        global tresult_dtp_disp
        global tresult_type_disp
        global tresult_gvw_disp
        global tresult_taw_disp
        global tresult_ax1_disp
        global tresult_ax1_park
        global tresult_ax2_disp
        global tresult_ax2_park
        global tresult_ax3_disp
        global tresult_ax3_park
        global tresult_ax4_disp
        global tresult_ax4_park
        global tresult_abs_disp
        global tresult_ebs_disp
        global tresult_lsv_disp
        global tresult_typapp_disp

        self.tresult_index = 0

        tresult_dtp_disp.set("")
        tresult_gvw_disp.set("")
        tresult_taw_disp.set("")
        tresult_ax1_disp.set("")
        tresult_ax2_disp.set("")
        tresult_ax3_disp.set("")
        tresult_ax4_disp.set("")
        tresult_ax1_park.set("")
        tresult_ax2_park.set("")
        tresult_ax3_park.set("")
        tresult_ax4_park.set("")
        tresult_type_disp.set("")
        tresult_abs_disp.set("")
        tresult_lsv_disp.set("")
        tresult_typapp_disp.set("")
        tresult_ebs_disp.set("")

    def dtp_trailer_numsearch(self, *args):
        global tresult_dtp_disp
        global tresult_type_disp
        global tresult_gvw_disp
        global tresult_taw_disp
        global tresult_ax1_disp
        global tresult_ax1_park
        global tresult_ax2_disp
        global tresult_ax2_park
        global tresult_ax3_disp
        global tresult_ax3_park
        global tresult_ax4_disp
        global tresult_ax4_park
        global tresult_abs_disp
        global tresult_ebs_disp
        global tresult_lsv_disp
        global tresult_typapp_disp

        self.trailersrchreset(*args)

        ## Next: Check given trailer DTP for validity,
        ## then work through it working out type, etc.
        tdtp = self.trailer_dtp_input.get()

        trailer = dtp.dtp_parse_trailer(tdtp)
        if trailer is not None:
            tresult_dtp_disp.set(tdtp)
            axlecount = int(trailer["Type"][0])
            tresult_type_disp.set(self.typedesc[self.typecodes.index(trailer["Type"])])
            tresult_gvw_disp.set(trailer["GVW"])
            if(trailer["TAW"]):
                self.trailer_taw_lbl.config(state="enabled")
                self.trailer_kpw_lbl.config(state="enabled")
                tresult_taw_disp.set(trailer["TAW"])
            else:
                self.trailer_taw_lbl.config(state="disabled")
                self.trailer_kpw_lbl.config(state="disabled")
                tresult_taw_disp.set("")


            tresult_ax1_disp.set("XX")
            tresult_ax1_park.set(trailer["Park"][0])

            if(axlecount > 1):
                tresult_ax2_disp.set("XX")
                tresult_ax2_park.set(trailer["Park"][1])

            if(axlecount > 2):
                tresult_ax3_disp.set("XX")
                tresult_ax3_park.set(trailer["Park"][2])

            if(axlecount > 3):
                tresult_ax4_disp.set("XX")
                tresult_ax4_park.set(trailer["Park"][3])

            tresult_abs_disp.set("ABS") if(trailer["ABS"] == "Yes") else tresult_abs_disp.set("")
            tresult_ebs_disp.set("EBS") if(trailer["EBS"] == "Yes") else tresult_ebs_disp.set("")
            tresult_lsv_disp.set("LSV") if(trailer["LSV"] == "Yes") else tresult_lsv_disp.set("")
            tresult_typapp_disp.set("Type Approved") if(trailer["TypeAppr"] == "Yes") else tresult_typapp_disp.set("")
        else:
            print("Wah!")


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

        ttk.Label(dlg, text="Source is available at:").grid(row=3, column=1)
        # Ugh. I hate that I'm hardcoding a colour here, but I can't
        # find a pre-set label style that would apply.
        link = ttk.Label(dlg, text="github.com/TamberP/dtp-base", cursor="hand2", foreground="blue2")
        link.grid(row=3, column=2)
        link.bind("<Button-1>", lambda e: web.open_new_tab("https://github.com/TamberP/dtp-base"))

        ttk.Label(dlg, text="DTP Database version:").grid(row=4, column=1)
        ttk.Label(dlg, text=dtp.db_version()[0]).grid(row=4, column=2)
        ttk.Button(dlg, text="Ok", command=dismiss).grid(row=5, column=2)

        dlg.protocol("WM_DELETE_WINDOW", dismiss)
        dlg.transient(root_win)
        dlg.wait_visibility()
        dlg.grab_set()
        dlg.wait_window()
        return

    def dtp_ui_help(self, *args):
        def dismiss ():
            dlg.grab_release()
            dlg.destroy()

        dlg = tk.Toplevel(root_win)
        dlg.title("Help")
        ttk.Label(dlg, text="Sorry. There's no help here yet. Maybe someday.").pack()
        ttk.Button(dlg, text="Ok...", command=dismiss).pack()
        dlg.protocol("WM_DELETE_WINDOW", dismiss)
        dlg.transient(root_win)
        dlg.wait_visibility()
        dlg.grab_set()
        dlg.wait_window()
        return

    def update_manuflist(self):
        self.manufcombo['values'] = self.vehmakes

    def update_braketype(self):
        self.srvbrktype['values'] = self.braketypes
        self.secbrktype['values'] = self.braketypes
        self.prkbrktype['values'] = self.braketypes

if __name__ == "__main__":
    root_win = tk.Tk()
    DTP_UI(root_win)
    root_win.mainloop()
