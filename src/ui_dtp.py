#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk
import dtp_database

class DTP_UI:
    result_index = 0

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
        global result_brk_rtn
        global index_disp
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
        result_brk_rtn = tk.StringVar()
        index_disp = tk.StringVar()

        ## Search frame

        ttk.Label(search_frame, text="DTp Number:").grid(column=1, row=1, sticky=(tk.W, tk.E))

        self.dtp_input = tk.StringVar()
        dtp_entry = ttk.Entry(search_frame, width=8, textvariable=self.dtp_input)
        dtp_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

        ttk.Button(search_frame, text="Go", command=self.dtp_numsearch).grid(column=3, row=1, sticky=tk.W)

        self.resultcount=tk.StringVar()

        ttk.Label(search_frame, textvariable=self.resultcount).grid(column=1, row=2, sticky=tk.E)
        ttk.Label(search_frame, text="results found.").grid(column=2, row=2, sticky=(tk.W, tk.E))

        ttk.Button(search_frame, text="Advanced Search", command=self.advancedsearch).grid(column = 2, row=3, sticky=(tk.W, tk.E))
        for child in search_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        search_frame.columnconfigure(2, weight=1)

        ## Results frame

        ttk.Label(results_frame, text='DTP No.').grid(row=1, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_dtp_disp).grid(row=1, column=2, columnspan=2, sticky=tk.W)
        ttk.Label(results_frame, text='Make').grid(row=2, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=20, textvariable=result_make_disp).grid(row=2, column=2, columnspan=2, sticky=tk.W)
        ttk.Label(results_frame, text='Type').grid(row=3, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=20, textvariable=result_type_disp).grid(row=3, column=2, columnspan=2, sticky=tk.W)
        ttk.Label(results_frame, text='GVW (kg)').grid(row=4, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=8, textvariable=result_gvw_disp).grid(row=4, column=2, columnspan=2, sticky=tk.W)

        ttk.Label(results_frame, text='GTW (kg)').grid(row=4, column=3, sticky=tk.E)
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

        ttk.Label(results_frame, text='Brake Routine').grid(row=10, column=1, sticky=tk.E)
        ttk.Label(results_frame, relief='sunken', width=20, textvariable=result_brk_rtn).grid(row=10, column=2, sticky=tk.W)

        result_prev_butt = ttk.Button(results_frame, text="Previous", command=self.result_prev).grid(column=1, row=20, sticky=tk.W)
        ttk.Label(results_frame, textvariable=index_disp).grid(row=20, column=2)
        result_next_butt = ttk.Button(results_frame, text="Next", command=self.result_next).grid(column=3, row=20, sticky=tk.E)

        for child in results_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        results_frame.columnconfigure(1, weight=1)
        results_frame.columnconfigure(2, weight=3)

        # Connect to the DB
        dtp_database.db_connect()

    def result_prev(self, *args):
        if(self.result_index > 0):
            self.result_index -= 1

        self.result_update()
        return

    def result_next(self, *args):
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
        global result_brk_rtn
        global index_disp
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

        result_brk_rtn.set(found["BrakeRoutine"])

        index_disp.set(str(self.result_index + 1) + " of " + self.resultcount.get())
        return

    def dtp_numsearch(self, *args):
        results = dtp_database.dtp_get(self.dtp_input.get())
        self.resultcount.set(len(results))
        self.db_results = results

    def advancedsearch(self, *args):
        # do nothing right now
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
        ttk.Label(dlg, text="dtp-base").grid(row=1, column=2)
        ttk.Label(dlg, text="For searching the DVSA's brake roller test procedure database.\nWritten by Tamber <tamber@furryhelix.co.uk>").grid(row=2, column=1, columnspan=3)
        ttk.Button(dlg, text="Ok", command=dismiss).grid(row=3, column=2)
        dlg.protocol("WM_DELETE_WINDOW", dismiss)
        dlg.transient(root_win)
        dlg.wait_visibility()
        dlg.grab_set()
        dlg.wait_window()
        return

    def dtp_ui_help(self, *args):
        return

if __name__ == "__main__":
    root_win = tk.Tk()
    DTP_UI(root_win)
    root_win.mainloop()
