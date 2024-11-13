# from scipy.special import functions
# from scipy.constants import value
from shiny import render, reactive, ui
import matplotlib.pyplot as plt
import pandas as pd
# import math
import random
# from functions_old import Functions, target_function_list_choices
# from shiny_files.functions_old import TargetFunctions
from shiny_files.functions import *
from shiny_files.calculations import *


# für das Anlegen der OOP-Objekte
# new_restriction = None
# new_target_function = None
# Listen mit OOP-Objekten
# restrictions_object_list = []
# target_functions_object_list = []
# Listen mit Unterlisten aller Funktionen und Atrribute OHNE OOP
# restrictions_list = []
# target_functions_list = []
# all_functions_list = []
# Dictionaries für die Auswahl-Fenster nach User-Eingaben


# alle_funktionen_reactive_list = reactive.Value([])

def server(input, output, session):
    #######################################################
    ##################reactive Values######################
    #######################################################

    target_function_dict = reactive.Value({})
    nebenbedingung_dict = reactive.Value({})

    zielfunktion_reactive_list = reactive.Value([])
    nebenbedingung_reactive_list = reactive.value([])

    selected_nebenbedingungen_reactive_list = reactive.Value([])
    selected_zielfunktion_reactive_list = reactive.Value([])

    solved_problems_list = reactive.Value([])

    xlim_var = reactive.Value([])
    ylim_var = reactive.Value([])

    xlim_var_dict = reactive.Value({})
    ylim_var_dict = reactive.Value({})

    function_colors = reactive.Value({})

    art_of_optimization_reactive = reactive.Value("")

    fig_reactive = reactive.Value(None)

    #liste_geraden_punkte_sets_reactive = reactive.Value([])

    #   global new_restricton
    #   global new_target_function
    #   global restrictions_object_list
    #   global target_functions_object_list
    # global restrictions_list
    # global target_functions_list
    # global all_functions_list
    # global target_function_dict
    # global nebenbedingung_dict

    # global nebenbedingung_reactive_list
    # global zielfunktion_reactive_list
    # global alle_funktionen_reactive_list
    # global solved_problems_list

    # global xlim_var
    # global ylim_var

    # global xlim_var_dict
    # global ylim_var_dict

    # global function_colors

    #########################################################################
    ##############Modal windows - Anfang#####################################
    #########################################################################

    #######################################################
    ##################Modal1 Anfang########################
    #######################################################
    @reactive.effect
    @reactive.event(input.button_zfkt_eingeben)
    def modal1():
        m = ui.modal(
            "Please enter your data:",
            ui.HTML("<br><br>"),
            ui.row(
                ui.column(6,
                          ui.input_numeric("zfkt_x1", "x1 eingeben", 1, min=None, max=None, step=0.01)),
                ui.column(6, ui.input_select(
                    "zfkt_select_attribute_1",
                    "Zahlenbereich:",
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                )),
            ),
            ui.row(
                ui.column(6, ui.input_numeric("zfkt_x2", "x2 eingeben", 1, min=None, max=None, step=0.01)),
                ui.column(6, ui.input_select(
                    "zfkt_select_attribute_2",
                    "Zahlenbereich:",
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                )
                          )
            ),
            ui.input_text("zfkt_name", "Name eingeben", "Zielfunktion-Name"),
            ui.input_select(
                "zfkt_select_minmax",
                "Art der Optimierung:",
                {"min": "Minimierung", "max": "Maximierung"},
            ),
            footer=ui.div(
                ui.input_action_button(id="cancel_button", label="Abbrechen"),
                ui.input_action_button(id="submit_button", label="Übermitteln"),
            ),
            title="Zielfunktion",
            easy_close=False,
        )
        ui.modal_show(m)

    #######################################################
    ##################Modal1 Ende##########################
    #######################################################

    #######################################################
    ##################Modal2 Anfang########################
    #######################################################

    @reactive.effect
    @reactive.event(input.action_button_restriktionen_eingeben)
    def modal2():
        m2 = ui.modal(
            "Bitte Daten eingeben:",
            ui.HTML("<br><br>"),
            ui.row(
                ui.column(6,
                          ui.input_numeric("rest_x1", "x1 eingeben", 1, min=None, max=None,
                                           step=0.01)),
                ui.column(6, ui.input_select(
                    "rest_select_attribute_1",
                    "Zahlenbereich:",
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                )),
            ),
            ui.row(
                ui.column(6, ui.input_numeric("rest_x2", "x2 eingeben", 2, min=None, max=None, step=0.01)),
                ui.column(6, ui.input_select(
                    "rest_select_attribute_2",
                    "Zahlenbereich:",
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                )
                          )
            ),
            ui.input_text("rest_name", "Name eingeben", "Restriktion-Name"),

            ui.row(
                ui.column(6,
                          ui.input_select(
                              "select_wertebereich_nebenbedingung",
                              "Select Wertebereich",
                              {"≤": "≤", "≥": "≥",
                               "=": "="},
                          )
                          ),
                ui.column(6,
                          ui.input_numeric("numeric_wertebereich_nebenbedingungen", "Wert", 1.11, min=None, max=None,
                                           step=0.01),
                          )
            ),

            footer=ui.div(
                ui.input_action_button(id="cancel_button_2", label="Abbrechen"),
                ui.input_action_button(id="submit_button_2", label="Übermitteln"),
            ),
            title="Restriktion",
            easy_close=False,
        )
        ui.modal_show(m2)

    #######################################################
    ##################Modal2 Ende##########################
    #######################################################
    #######################################################
    ##################Modal 3 Anfang#######################
    #######################################################
    @reactive.effect
    @reactive.event(input.action_button_zielfunktion_ändern)
    def modal3():
        m3 = ui.modal(
            ui.row(
                ui.column(6, ui.input_select(
                    "select_target_function_for_change",
                    "Bitte Zielfunktion wählen:",
                    #ui.HTML("<br><br>"),
                    choices=target_function_dict.get(),
                ), ),
                # ui.column(6, ui.input_radio_buttons(
                #    "radio_target_function",
                #    "Bitte Aktion wählen",
                #   {"option_löschen": "löschen", "option_ändern": "ändern"},
                # ), ),
                ui.HTML("<b>""Aktuelle Werte vorausgefüllt. Bei Bedarf ändern. ""</b>"),
                ui.HTML("<br><br>")
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""x1: ""</b>")),
                #               ui.column(8, ui.input_numeric("zfkt_x1_update", None, target_functions_list[0][1], min=None, max=None,
                #                                            step=0.01)),
                ui.column(8, ui.input_numeric("zfkt_x1_update", None, zielfunktion_reactive_list.get()[0][1], min=None,
                                              max=None,
                                              step=0.01)),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Eigenschaft x1""</b>")),
                ui.column(8, ui.input_select(
                    "zfkt_select_attribute_1_update",
                    None,
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                    selected=zielfunktion_reactive_list.get()[0][2]
                ))
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""x2""</b>")),
                ui.column(8, ui.input_numeric("zfkt_x2_update", None, zielfunktion_reactive_list.get()[0][3], min=None,
                                              max=None,
                                              step=0.01)),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Eigenschaft x2""</b>")),
                ui.column(8, ui.input_select(
                    "zfkt_select_attribute_2_update",
                    None,
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                    selected=zielfunktion_reactive_list.get()[0][4]
                ))
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""min-max""</b>")),
                ui.column(8, ui.input_select(
                    "zfkt_select_minmax_update",
                    None,
                    {"min": "Minimierung", "max": "Maximierung"},
                    selected=zielfunktion_reactive_list.get()[0][5]
                ))
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Name""</b>")),
                ui.column(8,
                          ui.input_text("zfkt_name_update", None, zielfunktion_reactive_list.get()[0][0]))
            ),
            footer=ui.div(
                ui.input_action_button(id="cancel_button_3", label="Abbrechen"),
                ui.input_action_button(id="submit_button_3", label="Übermitteln"),
            ),
            title="Zielfunktion ändern",
            easy_close=False,
            style="width: 100%;"
        )

        ui.modal_show(m3)

    ########################################################
    ##################Modal 3 nde###########################
    ########################################################
    ########################################################
    ##################Modal 4 Anfang########################
    ########################################################

    @reactive.effect
    @reactive.event(input.action_button_zielfunktion_löschen)
    def modal4():
        m4 = ui.modal(
            ui.row(
                ui.column(5, ui.input_select(
                    "select_target_function_for_delete",
                    "Zielfunktion wählen:",
                    #ui.HTML("<br><br>"),
                    choices=target_function_dict.get(),
                ), ),
                ui.column(7, ui.output_text(id="mod4_text"))
            ),
            footer=ui.div(
                ui.input_action_button(id="cancel_button_4", label="Abbrechen"),
                ui.input_action_button(id="submit_button_4", label="löschen"),
            ),
            title="Zielfunktion löschen",
            easy_close=False,
            style="width: 100%;"
        )
        ui.modal_show(m4)

    ########################################################
    ##################Modal 4 nde###########################
    ########################################################
    ########################################################
    ##################Modal 5 Anfang########################
    ########################################################

    @reactive.effect
    @reactive.event(input.action_button_restriktionen_ändern)
    def modal5():
        m5 = ui.modal(
            ui.row(
                ui.column(6, ui.input_select(
                    "select_rest_function_mod5",
                    "Bitte Nebenbedingung wählen:",
                    #ui.HTML("<br><br>"),
                    choices=nebenbedingung_dict.get(),
                ), ),
                # ui.column(6, ui.input_radio_buttons(
                #    "radio_target_function",
                #    "Bitte Aktion wählen",
                #   {"option_löschen": "löschen", "option_ändern": "ändern"},
                # ), ),
                ui.HTML("<b>""Aktuelle Werte vorausgefüllt. Bei Bedarf ändern. ""</b>"),
                ui.HTML("<br>""<br>")
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""x1: ""</b>")),
                ui.column(8,
                          ui.input_numeric("rest_x1_update", None, nebenbedingung_reactive_list.get()[0][1], min=None,
                                           max=None,
                                           step=0.01)),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Eigenschaft x1""</b>")),
                ui.column(8, ui.input_select(
                    "rest_select_attribute_1_update",
                    None,
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                    selected=nebenbedingung_reactive_list.get()[0][2]
                ))
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""x2""</b>")),
                ui.column(8,
                          ui.input_numeric("rest_x2_update", None, nebenbedingung_reactive_list.get()[0][3], min=None,
                                           max=None,
                                           step=0.01)),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Eigenschaft x2""</b>")),
                ui.column(8, ui.input_select(
                    "rest_select_attribute_2_update",
                    None,
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                    selected=nebenbedingung_reactive_list.get()[0][4]
                ))
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Wertebereich""</b>")),
                ui.column(8, ui.input_select(
                    "rest_select_wertebereich_update",
                    None,
                    {"≤": "≤", "≥": "≥",
                     "=": "="},
                    selected=nebenbedingung_reactive_list.get()[0][5]
                ))
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Wert""</b>")),
                ui.column(8,
                          ui.input_numeric("rest_wert_update", None, nebenbedingung_reactive_list.get()[0][6], min=None,
                                           max=None,
                                           step=0.01)),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Name""</b>")),
                ui.column(8,
                          ui.input_text("rest_name_update", None, nebenbedingung_reactive_list.get()[0][0]))
            ),
            footer=ui.div(
                ui.input_action_button(id="cancel_button_5", label="Abbrechen"),
                ui.input_action_button(id="submit_button_5", label="Übermitteln"),
            ),
            title="Nebenbedingung ändern",
            easy_close=False,
            style="width: 100%;"
        )

        ui.modal_show(m5)

    ########################################################
    ##################Modal 5 Ende##########################
    ########################################################
    ########################################################
    ##################Modal 6 Anfang########################
    ########################################################
    @reactive.effect
    @reactive.event(input.action_button_restriktionen_löschen)
    def modal6():
        m6 = ui.modal(
            ui.row(
                ui.column(5, ui.input_select(
                    "select_restriction_for_delete",
                    "Restriktion wählen:",
                    choices=nebenbedingung_dict.get(),
                ), ),
                ui.column(7, ui.output_text(id="mod6_text"))
            ),
            footer=ui.div(
                ui.input_action_button(id="cancel_button_6", label="Abbrechen"),
                ui.input_action_button(id="submit_button_6", label="löschen"),
            ),
            title="Restriktion löschen",
            easy_close=False,
            style="width: 100%;"
        )
        ui.modal_show(m6)

    ########################################################
    ##################Modal 6 Ende##########################
    ########################################################
    ########################################################
    ##################Modal 7 Anfang########################
    ########################################################
    @reactive.effect
    @reactive.event(input.save_graph_png)
    def modal7():

        m7 = ui.modal(
            ui.row(
                ui.column(4, ui.HTML("<b>""Name Graph""</b>")),
                ui.column(8, ui.input_text("name_graph", None, "Enter name of graph")),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Speicherpfad""</b>")),
                ui.column(8, ui.input_text("speicherpfad_graph", None, "Bsp.: C:/Users/.../Desktop")),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Bitte Wahl treffen""</b>")),
                ui.column(8,
                          ui.input_radio_buttons(
                              "radio_graph_dpi",
                              None,
                              {"vordefinierte_dpi": "vordefinierte DPI", "selbst_dpi": "DPI selbst wählen"},
                          )),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Wähle DPI""</b>")),
                ui.column(8,
                          ui.input_select(
                              "select_dpi",
                              None,
                              {"72": 72, "150": 150, "300": 300, "600": 600},
                          )),
            ),
            ui.row(
                ui.HTML("<b>""oder (je nach obiger Wahl)""</b>"),
                ui.HTML("<br><br>")
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Bitte DPI eingeben""</b>")),
                ui.column(8,
                          ui.input_numeric("numeric_dpi", None, 1, min=1, max=None, step=1)),
            ),
            footer=ui.div(
                ui.input_action_button(id="cancel_button_7", label="Abbrechen"),
                ui.input_action_button(id="submit_button_7", label="Übermitteln"),
            ),
            title="Save Graph as PNG",
            easy_close=False,
            style="width: 100%;"
        )
        ui.modal_show(m7)


        ########################################################
        ##################Modal 7 Ende##########################
        ########################################################
    #########################################################################
    ##############Modal windows - Ende#######################################
    #########################################################################

    #######################################################
    ##################Cancel Button########################
    #######################################################

    @reactive.effect
    @reactive.event(input.cancel_button)
    def close_modal_cancel():
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.cancel_button_2)
    def close_modal2_cancel():
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.cancel_button_3)
    def close_modal3_cancel():
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.cancel_button_4)
    def close_modal4_cancel():
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.cancel_button_5)
    def close_modal5_cancel():
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.cancel_button_6)
    def close_modal6_cancel():
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.cancel_button_7)
    def close_modal7_cancel():
        ui.modal_remove()

    ########################################################################
    ##################Submit Button#########################################
    ########################################################################
    #######################################################
    ##################Submit Button 1######################
    #######################################################
    @reactive.effect
    @reactive.event(input.submit_button)
    def create_target_function():


        if not zielfunktion_reactive_list.get():
            name = input.zfkt_name()
        else:
            detected = False
            for function in zielfunktion_reactive_list.get():
                if input.zfkt_name() in function[0]:
                    detected = True
                    counter = 0
                    for entry in zielfunktion_reactive_list.get():
                        if input.zfkt_name() in entry[0]:
                            counter += 1
                    name = input.zfkt_name() + "_" + str(counter)
            if detected == False:
                name = input.zfkt_name()

        x1 = input.zfkt_x1()
        attribute_1 = input.zfkt_select_attribute_1()
        x2 = input.zfkt_x2()
        attribute_2 = input.zfkt_select_attribute_2()
        min_max = input.zfkt_select_minmax()

        updated_zielfunktion_reactive_list = zielfunktion_reactive_list.get().copy()
        updated_zielfunktion_reactive_list.append([name, x1, attribute_1, x2, attribute_2, min_max])
        zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)


        ui.update_action_button("action_button_zielfunktion_ändern", disabled=False)
        ui.update_action_button("action_button_zielfunktion_löschen", disabled=False)
        print(len(zielfunktion_reactive_list.get()))

        print(zielfunktion_reactive_list.get())

        #update_target_function_choices()
        copy_target_function_dict = target_function_dict.get().copy()
        for target_function in zielfunktion_reactive_list.get():
            copy_target_function_dict[target_function[0]] = target_function[0]
        target_function_dict.set(copy_target_function_dict)
            #target_function_dict[target_function[0]] = target_function[0]
        print(target_function_dict)
        ui.update_select("select_target_function", choices=target_function_dict.get())

        ui.modal_remove()




    #######################################################
    ##################Submit Button 2######################
    #######################################################

    @reactive.effect
    @reactive.event(input.submit_button_2)
    def create_restriction():


        if not nebenbedingung_reactive_list.get():
            name = input.rest_name()
        else:
            detected = False
            for function in nebenbedingung_reactive_list.get():
                if input.rest_name() in function[0]:
                    detected = True
                    counter = 0
                    for entry in nebenbedingung_reactive_list.get():
                        if input.rest_name() in entry[0]:
                            counter += 1
                    name = input.rest_name() + "_" + str(counter)
            if detected == False:
                name = input.rest_name()
        x1 = input.rest_x1()
        attribute_1 = input.rest_select_attribute_1()
        x2 = input.rest_x2()
        attribute_2 = input.rest_select_attribute_2()
        wertebereich_symbol = input.select_wertebereich_nebenbedingung()
        wertebereich_wert = input.numeric_wertebereich_nebenbedingungen()

        updated_nebenbedingung_reactive_list = nebenbedingung_reactive_list.get().copy()
        updated_nebenbedingung_reactive_list.append([name, x1, attribute_1, x2, attribute_2, wertebereich_symbol, wertebereich_wert])
        nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)

        ui.update_action_button("action_button_restriktionen_ändern", disabled=False)
        ui.update_action_button("action_button_restriktionen_löschen", disabled=False)

        print(function_as_text(nebenbedingung_reactive_list.get()[0]))
        print(len(nebenbedingung_reactive_list.get()))

        print(nebenbedingung_reactive_list.get())

        #update_restriction_choices()
        copy_nebenbedingung_reactive_dict = nebenbedingung_dict.get().copy()
        for restriction in nebenbedingung_reactive_list.get():
            copy_nebenbedingung_reactive_dict[restriction[0]] = restriction[0]
        nebenbedingung_dict.set(copy_nebenbedingung_reactive_dict)
            #nebenbedingung_dict[restriction[0]] = restriction[0]
        print(nebenbedingung_dict)
        ui.update_selectize("selectize_nebenbedingung", choices=nebenbedingung_dict.get())


        ui.modal_remove()

    #######################################################
    ##################Submit Button 3######################
    #######################################################

    @reactive.effect
    @reactive.event(input.submit_button_3)
    def close_modal3_by_uebermitteln():
        selected_function_name = input.select_target_function_for_change()
        counter = 0
        for target_function in zielfunktion_reactive_list.get():
            if target_function[0] == selected_function_name:
                updated_zielfunktion_reactive_list = zielfunktion_reactive_list.get().copy()
                if input.zfkt_x1_update() != target_function[1]:
                    updated_zielfunktion_reactive_list[counter][1] = input.zfkt_x1_update()
                    zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
                    # zielfunktion_reactive_list.get()[counter][1] = input.zfkt_x1_update()
                if input.zfkt_select_attribute_1_update() != target_function[2]:
                    updated_zielfunktion_reactive_list[counter][2] = input.zfkt_select_attribute_1_update()
                    zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
                    # zielfunktion_reactive_list.get()[counter][2] = input.zfkt_select_attribute_1_update()
                if input.zfkt_x2_update() != target_function[3]:
                    updated_zielfunktion_reactive_list[counter][3] = input.zfkt_x2_update()
                    zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
                    # zielfunktion_reactive_list.get()[counter][3] = input.zfkt_x2_update()
                if input.zfkt_select_attribute_2_update() != target_function[4]:
                    updated_zielfunktion_reactive_list[counter][4] = input.zfkt_select_attribute_2_update()
                    zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
                    # zielfunktion_reactive_list.get()[counter][4] = input.zfkt_select_attribute_2_update()
                if input.zfkt_select_minmax_update() != target_function[5]:
                    updated_zielfunktion_reactive_list[counter][5] = input.zfkt_select_minmax_update()
                    zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
                    # zielfunktion_reactive_list.get()[counter][5] = input.zfkt_select_minmax_update()
                if input.zfkt_name_update() != target_function[0]:
                    updated_zielfunktion_reactive_list[counter][0] = input.zfkt_name_update()
                    zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
                    # zielfunktion_reactive_list.get()[counter][0] = input.zfkt_name_update()
                    copy_target_function_dict = target_function_dict.get().copy()
                    #copy_target_function_dict[target_function[0]] = input.zfkt_name_update()
                    copy_target_function_dict[input.zfkt_name_update()] = input.zfkt_name_update()
                    print(target_function_dict)
                    del copy_target_function_dict[selected_function_name]
                    target_function_dict.set(copy_target_function_dict)
                    print(target_function_dict)

                ui.update_select("select_target_function", choices=target_function_dict.get())

                print(function_as_text(target_function))
                print(zielfunktion_reactive_list.get())
                # print(alle_funktionen_reactive_list.get())
            counter += 1
        ui.modal_remove()

    #######################################################
    ##################Submit Button 4######################
    #######################################################

    @reactive.effect
    @reactive.event(input.submit_button_4)
    def delete_target_function():
        updated_zielfunktion_reactive_list = zielfunktion_reactive_list.get().copy()
        copy_target_function_dict = target_function_dict.get().copy()
        for function in zielfunktion_reactive_list.get():
            if function[0] == input.select_target_function_for_delete():
                updated_zielfunktion_reactive_list.remove(function)
                zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
                # zielfunktion_reactive_list.get().remove(function)
                # updated_alle_funktionen_reactive_list.remove(function)
                # alle_funktionen_reactive_list.set(updated_alle_funktionen_reactive_list)
                # alle_funktionen_reactive_list.get().remove(function)
                del copy_target_function_dict[input.select_target_function_for_delete()]
                target_function_dict.set(copy_target_function_dict)
        #print(target_function_dict)
        #print(zielfunktion_reactive_list.get())
        # print(alle_funktionen_reactive_list.get())
        ui.update_select("select_target_function", choices=target_function_dict.get())
        if not zielfunktion_reactive_list.get():
            ui.update_action_button("action_button_zielfunktion_ändern", disabled=True)
            ui.update_action_button("action_button_zielfunktion_löschen", disabled=True)
        # ui.update_text("zfkt_text", choices=target_function_dict)
        ui.modal_remove()

        #######################################################
        ##################Submit Button 5######################
        #######################################################

    @reactive.effect
    @reactive.event(input.submit_button_5)
    def close_modal5_by_uebermitteln():
        selected_function_name = input.select_rest_function_mod5()
        counter = 0
        for restriction in nebenbedingung_reactive_list.get():
            if restriction[0] == selected_function_name:
                updated_nebenbedingung_reactive_list = nebenbedingung_reactive_list.get().copy()
                if input.rest_x1_update() != restriction[1]:
                    updated_nebenbedingung_reactive_list[counter][1] = input.rest_x1_update()
                    nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                    # nebenbedingung_reactive_list.get()[counter][1] = input.rest_x1_update()
                if input.rest_select_attribute_1_update() != restriction[2]:
                    updated_nebenbedingung_reactive_list[counter][2] = input.rest_select_attribute_1_update()
                nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                # nebenbedingung_reactive_list.get()[counter][2] = input.rest_select_attribute_1_update()
                if input.rest_x2_update() != restriction[3]:
                    updated_nebenbedingung_reactive_list[counter][3] = input.rest_x2_update()
                    nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                    # nebenbedingung_reactive_list.get()[counter][3] = input.rest_x2_update()
                if input.rest_select_attribute_2_update() != restriction[4]:
                    updated_nebenbedingung_reactive_list[counter][4] = input.rest_select_attribute_2_update()
                    nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                    # nebenbedingung_reactive_list.get()[counter][4] = input.rest_select_attribute_2_update()
                if input.rest_select_wertebereich_update() != restriction[5]:
                    updated_nebenbedingung_reactive_list[counter][5] = input.rest_select_wertebereich_update()
                    nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                    # nebenbedingung_reactive_list.get()[counter][5] = input.rest_select_wertebereich_update()
                if input.rest_wert_update() != restriction[6]:
                    updated_nebenbedingung_reactive_list[counter][6] = input.rest_wert_update()
                    nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                    # nebenbedingung_reactive_list.get()[counter][6] = input.rest_wert_update()
                if input.rest_name_update() != restriction[0]:
                    updated_nebenbedingung_reactive_list[counter][0] = input.rest_name_update()
                    nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                    # nebenbedingung_reactive_list.get()[counter][0] = input.rest_name_update()
                    copy_nebenbedingung_reactive_dict = nebenbedingung_dict.get().copy()
                    copy_nebenbedingung_reactive_dict[input.rest_name_update()] = input.rest_name_update()
                    del copy_nebenbedingung_reactive_dict[selected_function_name]
                    nebenbedingung_dict.set(copy_nebenbedingung_reactive_dict)


                ui.update_select("selectize_nebenbedingung", choices=nebenbedingung_dict.get())

                #print(function_as_text(restriction))
                #print(nebenbedingung_reactive_list.get())
            counter += 1
        ui.modal_remove()

        #######################################################
        ##################Submit Button 6######################
        #######################################################

    @reactive.effect
    @reactive.event(input.submit_button_6)
    def delete_restriction():
        updated_nebenbedingung_reactive_list = nebenbedingung_reactive_list.get().copy()
        copy_nebenbedingung_dict = nebenbedingung_dict.get().copy()
        for function in nebenbedingung_reactive_list.get():
            if function[0] == input.select_restriction_for_delete():
                updated_nebenbedingung_reactive_list.remove(function)
                nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                # nebenbedingung_reactive_list.get().remove(function)
                #  updated_alle_funktionen_reactive_list.remove(function)
                #  alle_funktionen_reactive_list.set(updated_alle_funktionen_reactive_list)
                # alle_funktionen_reactive_list.get().remove(function)
                del copy_nebenbedingung_dict[input.select_restriction_for_delete()]
                nebenbedingung_dict.set(copy_nebenbedingung_dict)
        ui.update_selectize("selectize_nebenbedingung", choices=nebenbedingung_dict.get())
        if not nebenbedingung_reactive_list.get():
            ui.update_action_button("action_button_restriktionen_ändern", disabled=True)
            ui.update_action_button("action_button_restriktionen_löschen", disabled=True)
        # ui.update_text("zfkt_text", choices=target_function_dict)
        ui.modal_remove()

        ########################################################################
        ##################Submit Button Ende####################################
        ########################################################################

        ########################################################################
        ##################Render Text Outputs###################################
        ########################################################################

    @output
    @render.ui
    def rest_text():
        return rest_text_reactive()

    # @reactive.event(nebenbedingung_reactive_list)
    @reactive.Calc
    def rest_text_reactive():
        summarized_text_rest = ""
        for function in nebenbedingung_reactive_list.get():
            summarized_text_rest += "<br>" + function_as_text(function) + "<br>"
        return ui.HTML(summarized_text_rest)

    @output
    @render.ui
    def zfkt_text():
        return zfkt_text_reactive()

    # @reactive.event(input.submit_button, input.submit_button_4)
    # @reactive.event(zielfunktion_reactive_list)
    @reactive.Calc
    def zfkt_text_reactive():
        summarized_text = ""
        for function in zielfunktion_reactive_list.get():
            summarized_text += "<br>" + function_as_text(function) + "<br>"
        return ui.HTML(summarized_text)

    @reactive.effect
    @reactive.event(input.select_target_function_for_change)
    def update_target_function_changing_placeholder():
        selected_function_name = input.select_target_function_for_change()
        for target_function in zielfunktion_reactive_list.get():
            if target_function[0] == selected_function_name:
                ui.update_text("zfkt_name_update", value=target_function[0])
                ui.update_numeric("zfkt_x1_update", value=target_function[1])
                ui.update_select("zfkt_select_attribute_1_update", selected=target_function[2])
                ui.update_numeric("zfkt_x2_update", value=target_function[3])
                ui.update_select("zfkt_select_attribute_2_update", selected=target_function[4])
                ui.update_select("zfkt_select_minmax_update", selected=target_function[5])

    @output
    @render.text
    def mod4_text():
        return update_mod4_text()

    @reactive.event(input.select_target_function_for_delete)
    def update_mod4_text():
        for function in zielfunktion_reactive_list.get():
            if function[0] == input.select_target_function_for_delete():
                return function_as_text(function)

    @reactive.effect
    @reactive.event(input.select_rest_function_mod5)
    def update_restriction_changing_placeholder():
        selected_function_name = input.select_rest_function_mod5()
        for restriction in nebenbedingung_reactive_list.get():
            if restriction[0] == selected_function_name:
                ui.update_text("rest_name_update", value=restriction[0])
                ui.update_numeric("rest_x1_update", value=restriction[1])
                ui.update_select("rest_select_attribute_1_update", selected=restriction[2])
                ui.update_numeric("rest_x2_update", value=restriction[3])
                ui.update_select("rest_select_attribute_2_update", selected=restriction[4])
                ui.update_select("rest_select_wertebereich_update", selected=restriction[5])
                ui.update_numeric("rest_wert_update", value=restriction[6])

    @output
    @render.text
    def mod6_text():
        return update_mod6_text()

    @reactive.event(input.select_restriction_for_delete)
    def update_mod6_text():
        for function in nebenbedingung_reactive_list.get():
            if function[0] == input.select_restriction_for_delete():
                return function_as_text(function)







    @output
    @render.ui
    def finale_auswahl_text():
        return update_finale_auswahl_text()

    # @reactive.event(nebenbedingung_reactive_list)
    @reactive.event(input.selectize_nebenbedingung, input.select_target_function, input.lineare_optimierung_button)
    def update_finale_auswahl_text():
        update_art_of_optimization_reactive = ""
        #selected_nebenbedingungen = reactive.Value([])
        #selected_zielfunktion = reactive.Value([])
        updated_selected_nebenbedingungen_reactive_list = selected_nebenbedingungen_reactive_list.get().copy()
        updated_selected_zielfunktion_reactive_list = selected_zielfunktion_reactive_list.get().copy()

        for nebenbedingung in nebenbedingung_reactive_list.get():
            if nebenbedingung[0] in input.selectize_nebenbedingung() and nebenbedingung not in selected_nebenbedingungen_reactive_list.get():
                updated_selected_nebenbedingungen_reactive_list.append(nebenbedingung)
                selected_nebenbedingungen_reactive_list.set(updated_selected_nebenbedingungen_reactive_list)

        for zielfunktion in zielfunktion_reactive_list.get():
            if zielfunktion[0] in input.select_target_function() and zielfunktion not in selected_zielfunktion_reactive_list.get():
                updated_selected_zielfunktion_reactive_list.append(zielfunktion)
                selected_zielfunktion_reactive_list.set(updated_selected_zielfunktion_reactive_list)

        if not selected_zielfunktion_reactive_list.get() and not selected_nebenbedingungen_reactive_list.get():
            update_art_of_optimization_reactive = "not defined"
            art_of_optimization_reactive.set(update_art_of_optimization_reactive)
            return ui.HTML(
                '<div style="text-align: center;"><b>Bitte Zielfunktion und Nebenbedingung(en) auswählen.</b></div>')


        elif selected_zielfunktion_reactive_list.get() or selected_nebenbedingungen_reactive_list.get():
            summarized_text_rest = "<br>Durch die Auswahl der Zielfunktionen<br> <br>und Nebenbedingungen ergibt sich<br> <br>folgende finale Auswahl für Ihr Problem:<br>"


            eigenschaften_liste = []
            for function in selected_zielfunktion_reactive_list.get():
                eigenschaften_liste.append([function[2], "x1"])
                eigenschaften_liste.append([function[4], "x2"])

            for function in selected_nebenbedingungen_reactive_list.get():
                eigenschaften_liste.append([function[2], "x1"])
                eigenschaften_liste.append([function[4], "x2"])

            eigenschaften_liste_nur_wertebereiche = [entry[0] for entry in eigenschaften_liste]

            if "int" in eigenschaften_liste_nur_wertebereiche and not "kon" in eigenschaften_liste_nur_wertebereiche:
                summarized_text_rest += "<br><b>Integer Linear Programming (ILP)</b><br>innerhalb dieses Wertebereiches:<br> <br><div style='text-align: center;'><b>x1 e No ; x2 e No</b></div>"
                update_art_of_optimization_reactive = "ILP"
                art_of_optimization_reactive.set(update_art_of_optimization_reactive)
            elif "kon" in eigenschaften_liste_nur_wertebereiche and not "int" in eigenschaften_liste_nur_wertebereiche:
                summarized_text_rest += "<br><b>Linear Programming (LP)</b><br>innerhalb dieses Wertebereiches:<br> <br><div style='text-align: center;'><b>x1 ≥ 0 ; x2 ≥ 0</b></div>"
                update_art_of_optimization_reactive = "LP"
                art_of_optimization_reactive.set(update_art_of_optimization_reactive)
            elif "int" in eigenschaften_liste_nur_wertebereiche and "kon" in eigenschaften_liste_nur_wertebereiche:
                summarized_text_rest += "<br><b>Mixed Integer Linear Programming (MILP)</b>"

                x1_int_counter = 0
                x1_kon_counter = 0
                x2_int_counter = 0
                x2_kon_counter = 0
                for entry in eigenschaften_liste:
                    if entry[1] == "x1" and entry[0] == "int":
                        x1_int_counter +=1
                    elif entry[1] == "x1" and entry[0] == "kon":
                        x1_kon_counter +=1
                    elif entry[1] == "x2" and entry[0] == "int":
                        x2_int_counter +=1
                    elif entry[1] == "x2" and entry[0] == "kon":
                        x2_kon_counter +=1

                if (len(eigenschaften_liste) / 2 ) == x1_int_counter and (len(eigenschaften_liste) / 2 ) == x2_kon_counter:
                    summarized_text_rest += "<br>innerhalb dieses Wertebereiches:<br> <br><div style='text-align: center;'><b>x1 e No ; x2 ≥ 0</b></div>"
                    update_art_of_optimization_reactive = "MILP_x1_int_x2_kon"
                    art_of_optimization_reactive.set(update_art_of_optimization_reactive)
                elif (len(eigenschaften_liste) / 2 ) == x1_kon_counter and (len(eigenschaften_liste) / 2 ) == x2_int_counter:
                    summarized_text_rest += "<br>innerhalb dieses Wertebereiches:<br> <br><div style='text-align: center;'><b>x1 ≥ 0 ; x2 e No</b></div>"
                    update_art_of_optimization_reactive = "MILP_x1_kon_x2_int"
                    art_of_optimization_reactive.set(update_art_of_optimization_reactive)
                else:
                    summarized_text_rest += "<br>innerhalb dieses Wertebereiches:<br> <br><div style='text-align: center;'><b>Pleases set x1 and x2 only to one Wert</b></div>"
                    update_art_of_optimization_reactive = "not defined"
                    art_of_optimization_reactive.set(update_art_of_optimization_reactive)




            return ui.HTML(f'<div style="text-align: center;">{summarized_text_rest}</div>')



        ########################################################################
        ##################Render DataFrames#####################################
        ########################################################################

    @output
    @render.data_frame
    def zahlenbereiche_df_output():
        return update_zahlenbereiche_df_output()

    @reactive.Calc
    def update_zahlenbereiche_df_output():

        zahlenbereiche_df = pd.DataFrame(columns=["Name", "x1", "x2", "Total"])

        for function in zielfunktion_reactive_list.get():

            eigenschaft_total = None
            if function[2] == "int" and function[4] == "int":
                eigenschaft_total = "integer lp (ILP)"
            elif (function[2] == "int" and function[4] == "kon") or (function[2] == "kon" and function[4] == "int"):
                eigenschaft_total = "mixed integer lp (MILP)"
            elif function[2] == "kon" and function[4] == "kon":
                eigenschaft_total = "lineare Programmierung (LP)"

            zahlenbereiche_df.loc[len(zahlenbereiche_df)] = [function[0], function[2], function[4], eigenschaft_total]
            # zahlenbereiche_df = zahlenbereiche_df.append({"Name": entry[0], "x1": entry[1], "Eigenschaft x1": entry[2], "x2": entry[3], "Eigenschaft x2": entry[4], "min-max": entry[5]}, ignore_index=True)

        for function in nebenbedingung_reactive_list.get():

            eigenschaft_total = None
            if function[2] == "int" and function[4] == "int":
                eigenschaft_total = "integer lp (ILP)"
            elif (function[2] == "int" and function[4] == "kon") or (function[2] == "kon" and function[4] == "int"):
                eigenschaft_total = "mixed integer lp (MILP)"
            elif function[2] == "kon" and function[4] == "kon":
                eigenschaft_total = "lineare Programmierung (LP)"

            zahlenbereiche_df.loc[len(zahlenbereiche_df)] = [function[0], function[2], function[4], eigenschaft_total]

        return render.DataGrid(zahlenbereiche_df)

    @output
    @render.data_frame
    def lp_results_df():
        return update_lp_results_df()

    @reactive.Calc
    def update_lp_results_df():

        if not solved_problems_list.get():
            result_df = pd.DataFrame({
                "Name": [""],
                "x1": [""],
                "x2": [""]
            })

            return render.DataTable(result_df)

        if solved_problems_list.get():
            name_column = ""
            for zielfunktion in zielfunktion_reactive_list.get():
                if zielfunktion[0] in input.select_target_function():
                    name_column = zielfunktion[0]

            result_df = pd.DataFrame({
                name_column: [solved_problems_list.get()[0][6]],
                "x1": [solved_problems_list.get()[1][0]],
                "x2": [solved_problems_list.get()[1][1]]
            })

            return render.DataTable(result_df)

    ########################################################################
    ##################Render Plot###########################################
    ########################################################################

   # @reactive.Calc
    #def select_target_function_and_nebenbedingung_watcher():
      #  copy_selected_nebenbedingungen_reactive_list = selected_nebenbedingungen_reactive_list.get().copy()
      #  copy_selected_zielfunktion_reactive_list = selected_zielfunktion_reactive_list.get().copy()
      #  for entry in selected_nebenbedingungen_reactive_list.get():
      #      if entry not in input.selectize_nebenbedingung():
       #         copy_selected_nebenbedingungen_reactive_list.remove(entry)
       #         selected_nebenbedingungen_reactive_list.set(copy_selected_nebenbedingungen_reactive_list)

       # for entry in selected_zielfunktion_reactive_list.get():
       #     if entry not in input.select_target_function():
       #         copy_selected_zielfunktion_reactive_list.remove(entry)
        #        selected_zielfunktion_reactive_list.set(copy_selected_zielfunktion_reactive_list)


    @reactive.effect
    @reactive.event(input.selectize_nebenbedingung, input.select_target_function)
    def update_selected_lists():
        # Aktualisierte Listen initialisieren
        updated_selected_nebenbedingungen_reactive_list = []
        updated_selected_zielfunktion_reactive_list = []

        # Füge nur die tatsächlich ausgewählten Nebenbedingungen hinzu
        for nebenbedingung in nebenbedingung_reactive_list.get():
            if nebenbedingung[0] in input.selectize_nebenbedingung():
                updated_selected_nebenbedingungen_reactive_list.append(nebenbedingung)

        # Füge nur die tatsächlich ausgewählte Zielfunktion hinzu
        for zielfunktion in zielfunktion_reactive_list.get():
            if zielfunktion[0] == input.select_target_function():
                updated_selected_zielfunktion_reactive_list.append(zielfunktion)

        # Setze die aktualisierten Listen
        selected_nebenbedingungen_reactive_list.set(updated_selected_nebenbedingungen_reactive_list)
        selected_zielfunktion_reactive_list.set(updated_selected_zielfunktion_reactive_list)

        # Debug-Ausgabe, um zu prüfen, ob die Listen korrekt aktualisiert werden
        print("Aktualisierte Nebenbedingungen:", selected_nebenbedingungen_reactive_list.get())
        print("Aktualisierte Zielfunktion:", selected_zielfunktion_reactive_list.get())

        solved_problems_list.set([])
        print("Solved Problems List:", solved_problems_list.get())







    @output
    @render.plot()
    def optimierung_plot():
        optimierung_plot_reactive()

    @reactive.event(input.selectize_nebenbedingung, input.select_target_function, input.lineare_optimierung_button)
    def optimierung_plot_reactive():
        if not input.selectize_nebenbedingung() and not input.select_target_function():
            fig, ax = plt.subplots()
            ax.spines["top"].set_color("none")
            ax.spines["right"].set_color("none")
            ax.grid(True, ls="--")
            ax.set_xlabel("x1-axis")
            ax.set_ylabel("x2-axis")
            ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
            ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ui.update_action_button("lineare_optimierung_button", disabled=True)
            ui.update_action_button("save_graph_png", disabled=True)
            return fig
        # elif not nebenbedingung_reactive_list.get():
        # return None
        else:
            ui.update_action_button("save_graph_png", disabled=False)
            print("------vorher-------")
            print(target_function_dict.get())
            print(nebenbedingung_dict.get())
            print(zielfunktion_reactive_list.get())
            print(len(zielfunktion_reactive_list.get()))
            print(nebenbedingung_reactive_list.get())
            print(len(nebenbedingung_reactive_list.get()))
            print(selected_zielfunktion_reactive_list.get())
            print(len(selected_zielfunktion_reactive_list.get()))
            print(selected_nebenbedingungen_reactive_list.get())
            print(len(selected_nebenbedingungen_reactive_list.get()))
            print(xlim_var.get())
            print(len(xlim_var.get()))
            print(ylim_var.get())
            print(len(ylim_var.get()))
            print(xlim_var_dict.get())
            print(ylim_var_dict.get())
            print(function_colors.get())
            print("-------------")
            #selected_nebenbedingungen = reactive.Value([])
            #selected_zielfunktion = reactive.Value([])
            #updated_selected_nebenbedingungen = selected_nebenbedingungen.get().copy()
            #updated_selected_zielfunktion = selected_zielfunktion.get().copy()

            #for nebenbedingung in nebenbedingung_reactive_list.get():
                #if nebenbedingung[0] in input.selectize_nebenbedingung():
                  #  updated_selected_nebenbedingungen.append(nebenbedingung)
                   # selected_nebenbedingungen.set(updated_selected_nebenbedingungen)
            #print("Plot Auswahl Nebenbedingungen: " + str(len(selected_nebenbedingungen.get())))
            #print(selected_nebenbedingungen.get())

            #for zielfunktion in zielfunktion_reactive_list.get():
               # if zielfunktion[0] in input.select_target_function():
                   # updated_selected_zielfunktion.append(zielfunktion)
                   # selected_zielfunktion.set(updated_selected_zielfunktion)
            #print("Plot Auswahl Zielfunktion: " + str(len(selected_zielfunktion.get())))
            #print(selected_zielfunktion.get())

            fig, ax = plt.subplots()

            ax.spines["top"].set_color("none")
            ax.spines["right"].set_color("none")
            ax.grid(True, ls="--")
            ax.set_xlabel("x1-axis")
            ax.set_ylabel("x2-axis")


            xlim_var_update = []  # xlim_var.get().copy()
            ylim_var_update = []  # ylim_var.get().copy()
            function_colors_update = {}  # function_colors.get().copy()
            xlim_var_dict_update = {}  # xlim_var_dict.get().copy()
            ylim_var_dict_update = {}  # ylim_var_dict.get().copy()


            print(f"vor for-Schleife neben{selected_nebenbedingungen_reactive_list.get()}")
            for nebenbedingung in selected_nebenbedingungen_reactive_list.get():
                print(f"in for-Schleife neben{selected_nebenbedingungen_reactive_list.get()}")



                schnittpunkt_x1 = calculate_schnittpunkte_x1_x2_axis(nebenbedingung)[0]
                schnittpunkt_x2 = calculate_schnittpunkte_x1_x2_axis(nebenbedingung)[1]

                random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

                ax.plot([0, schnittpunkt_x1], [schnittpunkt_x2, 0], label=nebenbedingung[0], color=random_color)

                #selected_nebenbedingungen_names = [nebenbedingung[0] for nebenbedingung in selected_nebenbedingungen_reactive_list.get()]
                #previous_xlim_var = [entry[1] for entry in xlim_var_update]
                #previous_ylim_var = [entry[1] for entry in ylim_var_update]

                #if [schnittpunkt_x1, nebenbedingung[0]] not in xlim_var.get():
                #for nebenbedingung_name in selected_nebenbedingungen_names:
                    #if nebenbedingung_name in previous_xlim_var:
                        #continue
                    #elif nebenbedingung_name not in previous_xlim_var:
                xlim_var_update.append([schnittpunkt_x1, nebenbedingung[0]])

                #if [schnittpunkt_x2, nebenbedingung[0]] not in ylim_var.get():
                #for nebenbedingung_name in selected_nebenbedingungen_names:
                    #if nebenbedingung_name in previous_ylim_var:
                        #continue
                    #elif nebenbedingung_name not in previous_ylim_var:
                ylim_var_update.append([schnittpunkt_x2, nebenbedingung[0]])

                xlim_var_dict_update[nebenbedingung[0]] = schnittpunkt_x1
                ylim_var_dict_update[nebenbedingung[0]] = schnittpunkt_x2

                function_colors_update[nebenbedingung[0]] = random_color

                xlim_var.set(xlim_var_update)
                ylim_var.set(ylim_var_update)

                xlim_var_dict.set(xlim_var_dict_update)
                ylim_var_dict.set(ylim_var_dict_update)

                function_colors.set(function_colors_update)

            #print("Schnittpunkte x1: " + str(len(xlim_var.get())))
           # print("Schnittpunkte x2: " + str(len(ylim_var.get())))
           # print(xlim_var.get())
            #print(ylim_var.get())
            # ax.set_xlim(0,calculate_highest_xlim_ylim(xlim_var.get(), ylim_var.get())[0])
            # ax.set_ylim(0,calculate_highest_xlim_ylim(xlim_var.get(), ylim_var.get())[1])
            print(f"vor for-Schleife ziel{selected_zielfunktion_reactive_list.get()}")
            for zielfunktion in selected_zielfunktion_reactive_list.get():
                print(f"in for-Schleife ziel{selected_zielfunktion_reactive_list.get()}")

                #xlim_var_update = xlim_var.get().copy()
                #ylim_var_update = ylim_var.get().copy()

                #xlim_var_dict_update = xlim_var_dict.get().copy()
                #ylim_var_dict_update = ylim_var_dict.get().copy()

                #function_colors_update = function_colors.get().copy()

                schnittpunkt_x1, schnittpunkt_x2 = calculate_schnittpunkte_x1_x2_axis(zielfunktion, xlim_var_update,
                                                                                      ylim_var_update)

                #print(schnittpunkt_x1)
                #print(schnittpunkt_x2)

                ax.plot([0, schnittpunkt_x1], [schnittpunkt_x2, 0], label=zielfunktion[0] + " (dummy)", color="#00FF00",
                        ls="--")


                #selected_zielfunktionen_names = [zielfunktion[0] for zielfunktion in selected_zielfunktion_reactive_list.get()]
                #previous_xlim_var = [entry[1] for entry in xlim_var_update]
                #previous_ylim_var = [entry[1] for entry in ylim_var_update]


                #if [schnittpunkt_x1, zielfunktion[0]] not in xlim_var.get():
                #for zielfunktion_name in selected_zielfunktionen_names:
                    #if zielfunktion_name in previous_xlim_var:
                        #continue
                    #elif zielfunktion_name not in previous_xlim_var:
                xlim_var_update.append([schnittpunkt_x1, zielfunktion[0]])

                #if [schnittpunkt_x2, zielfunktion[0]] not in ylim_var.get():
                #for zielfunktion_name in selected_zielfunktionen_names:
                    #if zielfunktion_name in previous_ylim_var:
                        #continue
                    #elif zielfunktion_name not in previous_ylim_var:
                ylim_var_update.append([schnittpunkt_x2, zielfunktion[0]])

                xlim_var_dict_update[zielfunktion[0]] = schnittpunkt_x1
                ylim_var_dict_update[zielfunktion[0]] = schnittpunkt_x2

                function_colors_update[zielfunktion[0]] = "#00FF00"

                xlim_var.set(xlim_var_update)
                ylim_var.set(ylim_var_update)

                xlim_var_dict.set(xlim_var_dict_update)
                ylim_var_dict.set(ylim_var_dict_update)


                function_colors.set(function_colors_update)

            ax.set_xlim(0, math.ceil(((calculate_highest_xlim_ylim(xlim_var.get(), ylim_var.get())[0]) * 1.1)))
            ax.set_ylim(0, math.ceil(((calculate_highest_xlim_ylim(xlim_var.get(), ylim_var.get())[1]) * 1.1)))

            # ax.plot(calculate_highest_xlim_ylim(xlim_var.get(), ylim_var.get())[0], 0, ">k", transform=ax.get_yaxis_transform(), clip_on = False)
            # ax.plot(0, calculate_highest_xlim_ylim(xlim_var.get(), ylim_var.get())[1], "^k", transform=ax.get_xaxis_transform(), clip_on = False)

            ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
            ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
            # schnittpunkte_x1_axis = [[0, 4]]
            # schnittpunkte_x2_axis = [[6, 0]]
            # schnittpunkte_x1_axis_2 = [[0, 2]]
            # schnittpunkte_x2_axis_2 = [[3, 0]]
            # ax.plot(schnittpunkte_x1_axis, schnittpunkte_x2_axis, label="Linie durch (4,0) und (0,6)", color = "black")
            # ax.plot(schnittpunkte_x1_axis_2, schnittpunkte_x2_axis_2, label="Linie durch (2,0) und (0,3)", color = "black")

            # ax.annotate('Zulässiger\nBereich', [2, 2])

            # ax.plot([2.5, 2.5], [3.5, 3.5], color = 'blue', ls = "--")
            # ax.arrow(2.5, 3.5, -1, -0.5, head_width=0.2, head_length=0.2, fc='blue', ec='blue')
            # ax.annotate("Zielfunktion_optimal", [2.5, 3.5], color = "blue")

            # ax.plot(2,5, "or", markersize = 8)
            # ax.arrow(4.5, 5.5, -1, -0.5, head_width=0.2, head_length=0.2, fc='red', ec='red')
            # ax.annotate("Optimale Lösung", [4.5, 5.5], color = "red")

            # fig.savefig("Name.png", dpi =150)

            ui.update_action_button("lineare_optimierung_button", disabled=False)









            # zulässiger Bereich
            if input.selectize_nebenbedingung():
                new_liste_geraden_punkte_sets_reactive = []

                for nebenfunktion in selected_nebenbedingungen_reactive_list.get():
                    punkte = set()

                    if nebenfunktion[5] == "≤":
                        start_wert = 0
                    elif nebenfunktion[5] == "≥":
                        start_wert = 0 #NOCH BEARBEITEN!!!!!! AUCH MIT ===============!!!!!!!!!!
                    elif nebenfunktion[5] == "=":
                        start_wert = 0 #NOCH BEARBEITEN!!!!!! AUCH MIT ===============!!!!!!!!!!



                    x_range = np.linspace(start_wert, xlim_var_dict.get()[nebenfunktion[0]], 1000)
                    for x in x_range:
                        y_max = y_ergebnis_an_geradengleichung(xlim_var_dict.get()[nebenfunktion[0]], ylim_var_dict.get()[nebenfunktion[0]], x)
                        for y in np.linspace(start_wert, y_max, 500):
                            punkte.add(
                                (math.trunc(x), math.trunc(y)))


                    new_liste_geraden_punkte_sets_reactive.append(punkte)
                    #liste_geraden_punkte_sets_reactive.set(new_liste_geraden_punkte_sets_reactive)

                schnittmenge_punkte = None
                counter = 0
                #for set_entry in liste_geraden_punkte_sets_reactive.get():
                for set_entry in new_liste_geraden_punkte_sets_reactive:
                    if counter == 0:
                        schnittmenge_punkte = set_entry
                    elif counter > 0:
                        schnittmenge_punkte = schnittmenge_punkte.intersection(set_entry)
                    counter += 1

                gemeinsame_x1_werte = [punkt[0] for punkt in schnittmenge_punkte]
                gemeinsame_x2_werte = [punkt[1] for punkt in schnittmenge_punkte]

                print("Gemeinsame x1-Werte: " + str(len(gemeinsame_x1_werte)))
                print("Gemeinsame x2-Werte: " + str(len(gemeinsame_x2_werte)))


                ax.scatter(gemeinsame_x1_werte, gemeinsame_x2_werte, color='lightgrey', s=2, alpha= 0.2)


















            if solved_problems_list.get():
                function_colors_update = function_colors.get().copy()
                # xlim_var_update = xlim_var.get().copy()
                # ylim_var_update = ylim_var.get().copy()
                schnittpunkt_x1 = calculate_schnittpunkte_x1_x2_axis(solved_problems_list.get()[0])[0]
                schnittpunkt_x2 = calculate_schnittpunkte_x1_x2_axis(solved_problems_list.get()[0])[1]
                ax.plot([0, schnittpunkt_x1], [schnittpunkt_x2, 0],
                        label=solved_problems_list.get()[0][0] + " (optimiert)", color="#0000FF", ls="--")
                # xlim_var_update.append(schnittpunkt_x1)
                # ylim_var_update.append(schnittpunkt_x2)
                # xlim_var.set(xlim_var_update)
                # ylim_var.set(ylim_var_update)

                ax.plot(solved_problems_list.get()[1][0], solved_problems_list.get()[1][1], "or", markersize=8)







                # Erstellung des roten Pfeils und der BEschriftung "Optimale Lösung". Dynamsiche Skalierung durch Abstand der x- und y-Achsen-Ticks
                x_axis_ticks = ax.get_xticks()
                y_axis_ticks = ax.get_yticks()
                abstand_zweier_xticks = x_axis_ticks[2] - x_axis_ticks[1]
                abstand_zweier_yticks = y_axis_ticks[2] - y_axis_ticks[1]
                opt_lösung_arrow_start_x = solved_problems_list.get()[1][0] + abstand_zweier_xticks
                opt_lösung_arrow_start_y = solved_problems_list.get()[1][1] + abstand_zweier_yticks
                ax.arrow(opt_lösung_arrow_start_x, opt_lösung_arrow_start_y, abstand_zweier_xticks * 0.9 * -1, abstand_zweier_yticks * 0.9 * -1, color = "red", width = (((abstand_zweier_xticks + abstand_zweier_yticks) / 2) * (1/50)), head_width = abstand_zweier_xticks * 0.05, head_length = abstand_zweier_yticks * 0.15, length_includes_head = True)
                ax.annotate("Optimale Lösung", [opt_lösung_arrow_start_x, opt_lösung_arrow_start_y], color = "red")







                # Erstellung des grünen Pfeils und der Beschriftung "Verschiebung". Indem die Geradengleichung der dummy-Zielfunktion berechnet wird (mx +b)
                steigung_zielfunktion_dummy = ((ylim_var_dict.get()[selected_zielfunktion_reactive_list.get()[0][0]] - 0) / (0 - xlim_var_dict.get()[selected_zielfunktion_reactive_list.get()[0][0]]))
                b_dummy = (-1) * steigung_zielfunktion_dummy * xlim_var_dict.get()[selected_zielfunktion_reactive_list.get()[0][0]]

                # die VAriablen die für die Berechnung der Koordinaten des Lotfußpunktes benötigt werden
                b = 1 * xlim_var_dict.get()[selected_zielfunktion_reactive_list.get()[0][0]]
                a = steigung_zielfunktion_dummy * xlim_var_dict.get()[selected_zielfunktion_reactive_list.get()[0][0]] * (-1)
                c = b_dummy * xlim_var_dict.get()[selected_zielfunktion_reactive_list.get()[0][0]] * (-1)
                x0 = solved_problems_list.get()[1][0]
                y0 = solved_problems_list.get()[1][1]

                # anschließend werden die Koordinaten des Lotfußpunktes berechnet
                coord_lot_x1 = ((b * ((b * x0) - (a * y0))) - (a * c)) / ((a * a) + (b * b))
                coord_lot_x2 = ((a * ((((-1) * b) * x0) + (a * y0))) - (b * c)) / ((a * a) + (b * b))

                # anschließend wird der Abstand des Lotfußpunktes zur optimalen Lösung berechnet
                x1_abstand_lot_x1_zu_opt_lös_punkt = solved_problems_list.get()[1][0] - coord_lot_x1
                x2_abstand_lot_x2_zu_opt_lös_punkt = solved_problems_list.get()[1][1] - coord_lot_x2

                #Je nach Zielfunktion wird der Pfeil in die entsprechende Richtung gezeichnet
                if selected_zielfunktion_reactive_list.get()[0][5] == "max":

                    ax.arrow(coord_lot_x1, coord_lot_x2, x1_abstand_lot_x1_zu_opt_lös_punkt * 0.9, x2_abstand_lot_x2_zu_opt_lös_punkt * 0.9, color = "#00FF00", width = (((abstand_zweier_xticks + abstand_zweier_yticks) / 2) * (1/50)), head_width = abstand_zweier_xticks * 0.05, head_length = abstand_zweier_yticks * 0.15, length_includes_head = True)
                    ax.annotate("Verschiebung", [coord_lot_x1, coord_lot_x2], color="#00FF00")
                elif selected_zielfunktion_reactive_list.get()[0][5] == "min":

                    ax.arrow(coord_lot_x1, coord_lot_x2, x1_abstand_lot_x1_zu_opt_lös_punkt * 0.9, x2_abstand_lot_x2_zu_opt_lös_punkt * 0.9, color = "#00FF00", width = (((abstand_zweier_xticks + abstand_zweier_yticks) / 2) * (1/50)), head_width = abstand_zweier_xticks * 0.05, head_length = abstand_zweier_yticks * 0.15, length_includes_head = True)
                    ax.annotate("Verschiebung", [coord_lot_x1, coord_lot_x2], color="#00FF00")








                function_colors_update[solved_problems_list.get()[0][0]] = "#0000FF"
                function_colors.set(function_colors_update)

















            ax.legend()

            print("------nachher-------")
            print(target_function_dict.get())
            print(nebenbedingung_dict.get())
            print(zielfunktion_reactive_list.get())
            print(len(zielfunktion_reactive_list.get()))
            print(nebenbedingung_reactive_list.get())
            print(len(nebenbedingung_reactive_list.get()))
            print(selected_zielfunktion_reactive_list.get())
            print(len(selected_zielfunktion_reactive_list.get()))
            print(selected_nebenbedingungen_reactive_list.get())
            print(len(selected_nebenbedingungen_reactive_list.get()))
            print(xlim_var.get())
            print(len(xlim_var.get()))
            print(ylim_var.get())
            print(len(ylim_var.get()))
            print(xlim_var_dict.get())
            print(ylim_var_dict.get())
            print(function_colors.get())
            print("-------------")


            fig_reactive.set(fig)


            return fig

    ########################################################################
    ##################Lineare Optimierung Button############################
    ########################################################################

    @reactive.effect
    @reactive.event(input.lineare_optimierung_button)
    def initialize_lin_opt():
        updated_solved_problems_list = []
        #selected_nebenbedingungen = reactive.Value([])
        #selected_zielfunktion = reactive.Value([])
        #updated_selected_nebenbedingungen = selected_nebenbedingungen.get().copy()
        #updated_selected_zielfunktion = selected_zielfunktion.get().copy()

        #for nebenbedingung in nebenbedingung_reactive_list.get():
            #if nebenbedingung[0] in input.selectize_nebenbedingung():
              #  updated_selected_nebenbedingungen.append(nebenbedingung)
              #  selected_nebenbedingungen.set(updated_selected_nebenbedingungen)

      #  for zielfunktion in zielfunktion_reactive_list.get():
          #  if zielfunktion[0] in input.select_target_function():
             #   updated_selected_zielfunktion.append(zielfunktion)
              #  selected_zielfunktion.set(updated_selected_zielfunktion)
              #  print(selected_zielfunktion.get())
        print("---------Art of Optimization---------")
        print("Art of Optimization: " + art_of_optimization_reactive.get())
        print("---------Art of Optimization---------")
        erg, schnittpunkte = solve_linear_programming_problem(selected_zielfunktion_reactive_list.get()[0],
                                                              selected_nebenbedingungen_reactive_list.get(), art_of_optimization_reactive.get())
        #print(erg)
        #print(schnittpunkte)
        #updated_solved_problems_list = solved_problems_list.get().copy()
        #if solved_problems_list.get():
            #del updated_solved_problems_list[0]
            #solved_problems_list.set(updated_solved_problems_list)
            #updated_solved_problems_list = solved_problems_list.get().copy()
        #updated_solved_problems_list = solved_problems_list.get().copy()

        solved_target_function = [selected_zielfunktion_reactive_list.get()[0][0], selected_zielfunktion_reactive_list.get()[0][1],
                                  selected_zielfunktion_reactive_list.get()[0][2], selected_zielfunktion_reactive_list.get()[0][3],
                                  selected_zielfunktion_reactive_list.get()[0][4], "=", erg]

        updated_solved_problems_list.append(solved_target_function)
        updated_solved_problems_list.append(schnittpunkte)
        solved_problems_list.set(updated_solved_problems_list)

        print(solved_problems_list.get())
    #  @output
    #   @render.ui
    #   def zfkt_text():
    #       return zfkt_text_reactive()
    #   #@reactive.event(input.submit_button, input.submit_button_4)
    #   @reactive.event(input.submit_button, input.cancel_button)
    #   def zfkt_text_reactive():
    #       summarized_text = ""
    #       for function in target_functions_list:
    #           summarized_text += "<br>" + function_as_text(function) + "<br>"
    #       return ui.HTML(summarized_text)

    # return function_as_text([find_function_by_dict_entry(input.select_target_function_for_delete())])

    ########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################

    # return function_as_text([find_function_by_dict_entry(input.select_target_function_for_delete())])

    # for function in nebenbedingung_reactive_list.get():
    # summarized_text_rest += "<br>" + function_as_text(function) + "<br>"

    # @reactive.effect
    #  @reactive.event(input.select_target_function)
    #   def update_modul3_placeholder():
    #        ui.update_numeric("zfkt_x1_update", value=target_function[1])
    @output
    @render.ui
    def beschreibung_text():
        return update_beschreibung_text()

    # @reactive.event(nebenbedingung_reactive_list)
    @reactive.event(input.selectize_nebenbedingung, input.select_target_function, input.lineare_optimierung_button)
    def update_beschreibung_text():

        #selected_nebenbedingungen = reactive.Value([])
        #selected_zielfunktion = reactive.Value([])
        #updated_selected_nebenbedingungen = selected_nebenbedingungen.get().copy()
        #updated_selected_zielfunktion = selected_zielfunktion.get().copy()

        #for nebenbedingung in nebenbedingung_reactive_list.get():
            #if nebenbedingung[0] in input.selectize_nebenbedingung():
               # updated_selected_nebenbedingungen.append(nebenbedingung)
               # selected_nebenbedingungen.set(updated_selected_nebenbedingungen)

        #for zielfunktion in zielfunktion_reactive_list.get():
            #if zielfunktion[0] in input.select_target_function():
               # updated_selected_zielfunktion.append(zielfunktion)
               # selected_zielfunktion.set(updated_selected_zielfunktion)

        if not selected_zielfunktion_reactive_list.get() and not selected_nebenbedingungen_reactive_list.get():
            return ui.HTML(
                '<div style="text-align: center;"><b>Bitte Zielfunktion und Nebenbedingung(en) auswählen.</b></div>')

        elif selected_zielfunktion_reactive_list.get() or selected_nebenbedingungen_reactive_list.get():
            summarized_text_rest = ""

            if solved_problems_list.get():
                summarized_text_rest += f'Die optimale Lösung für die Zielfunktion <p style="color: #0000FF;">{solved_problems_list.get()[0][0]} (optimiert)</p> schneidet die <b>x1-axis</b> bei <b>{solved_problems_list.get()[1][0]}</b> und die <b>x2-axis</b> bei <b>{solved_problems_list.get()[1][1]}</b> und hat den optimalen Wert <p style="color: #FF0000;">{solved_problems_list.get()[0][6]}</p>.<br><br>'

            for zielfunktion in selected_zielfunktion_reactive_list.get():
                summarized_text_rest += f'Die <p style="color: #00FF00;">(Dummy)-Zielfunktion {zielfunktion[0]}</p> schneidet die <b>x1-axis</b> bei <b>{xlim_var_dict.get()[zielfunktion[0]]}</b> und die <b>x2-axis</b> bei <b>{ylim_var_dict.get()[zielfunktion[0]]}</b>.<br><br>'

            for nebenbedingung in selected_nebenbedingungen_reactive_list.get():
                summarized_text_rest += f'Die <p style="color: {function_colors.get()[nebenbedingung[0]]};">Nebenbedingung {nebenbedingung[0]}</p> schneidet die <b>x1-axis</b> bei <b>{xlim_var_dict.get()[nebenbedingung[0]]}</b> und die <b>x2-axis</b> bei <b>{ylim_var_dict.get()[nebenbedingung[0]]}</b>.<br><br>'

                # if "int" in eigenschaften_liste and not "kon" in eigenschaften_liste:
                #    summarized_text_rest += "<br><br><b>Integer Linear Programming (ILP)</b>"
                # elif "kon" in eigenschaften_liste and not "int" in eigenschaften_liste:
                #     summarized_text_rest += "<br><br><b>Linear Programming (LP)</b>"
                # elif "int" in eigenschaften_liste and "kon" in eigenschaften_liste:
                #     summarized_text_rest += "<br><br><b>Mixed Integer Linear Programming (MILP)</b>"

            return ui.HTML(f'<div style="text-align: center;">{summarized_text_rest}</div>')




    @reactive.effect
    @reactive.event(input.submit_button_7)
    def save_graph_png_and_close_mod7():
        fig = fig_reactive.get()
        speicherpfad = input.speicherpfad_graph()
        if speicherpfad[-1] != "/":
            speicherpfad += "/"

        dpi_wahl = 0

        if input.radio_graph_dpi() == "vordefinierte_dpi":
            dpi_wahl = input.select_dpi()
        elif input.radio_graph_dpi() == "selbst_dpi":
            dpi_wahl = input.numeric_dpi()

        if fig is None:
            print("Fehler: Keine Figur vorhanden zum Speichern.")
        print(f"dpi-wahl:{dpi_wahl}")
        fig.savefig(speicherpfad + input.name_graph() + ".png", dpi=int(dpi_wahl))

        ui.modal_remove()