from shiny import ui
from server import target_function_dict
from server import nebenbedingung_dict

app_ui = ui.page_navbar(
    ui.nav_panel("Lineare Optimierung",
                 ui.layout_sidebar(
                     ui.sidebar(
                         ui.row(
                             ui.card(
                                 ui.card_header("User Inputs"),
                                 ui.card(
                                     ui.input_action_button(id="button_zfkt_eingeben",
                                                            label="Zielfunktion eingeben"
                                                            ),
                                     ui.input_action_button(id="action_button_zielfunktion_ändern",
                                                            label="Zielfunktion ändern",
                                                            disabled=True
                                                            ),
                                     ui.input_action_button(id="action_button_zielfunktion_löschen",
                                                            label="Zielfunktion löschen",
                                                            disabled=True
                                                            ),
                                 ),
                                 ui.card(
                                     ui.input_action_button(id="action_button_restriktionen_eingeben",
                                                            label="Restriktionen eingeben",
                                                            disabled=False
                                                            ),
                                     ui.input_action_button(id="action_button_restriktionen_ändern",
                                                            label="Restriktionen ändern",
                                                            disabled=True
                                                            ),
                                     ui.input_action_button(id="action_button_restriktionen_löschen",
                                                            label="Restriktionen löschen",
                                                            disabled=True
                                                            ),
                                 ),
                                 ui.card(
                                     ui.input_action_button(id="change_wertebereich_x1_x2",
                                                            label="Wertebereich eingeben",
                                                            disabled=True
                                                            ),
                                     # HTML und CSS, damit der Text zentriert ist
                                     ui.HTML('<div style="text-align: center;">''<b>''x1 ≥ 0 ; x2 ≥ 0''</b>''</div>'),
                                 )
                             ),
                         ),
                         ui.row(
                             ui.card(
                                 ui.card_header("Import / Export / Save png")
                             )
                         ),
                         width="20%"),
                     ui.layout_columns(
                         ui.card(
                             ui.card_header("Übermittelte Daten"),
                             ui.layout_column_wrap(
                                 ui.card(
                                     ui.card_header("Übersicht der Funktionen"),
                                     ui.HTML("<b>""Zielfunktion:""</b>"),
                                     ui.output_ui("zfkt_text"),
                                     ui.br(),
                                     ui.HTML("<b>""Restriktionen:""</b>"),
                                     ui.output_ui("rest_text"),
                                 ),
                                 ui.card(
                                     ui.card_header("Auswahl der Funktionen"),
                                     ui.input_select(
                                         "select_target_function",
                                         "Select an Zielfunktion:",
                                         choices=target_function_dict,
                                     ),
                                     ui.input_selectize(
                                         "selectize_nebenbedingung",
                                         "Select Nebenbedingungen:",
                                         choices=nebenbedingung_dict,
                                         multiple=True,
                                     ),
                                     ui.HTML("<br>""<br>")
                                 ),
                                 ui.card(
                                     ui.card_header("Übersicht der Zahlenbereiche"),
                                     ui.output_data_frame("zahlenbereiche_df_output")
                                 ),
                                 ui.card(
                                        ui.card_header("Lineare Optimierung - Info"),
                                        ui.output_ui("finale_auswahl_text")
                                 ),
                                 width=1 / 2,
                             ),

                         ),
                         ui.card(
                             ui.card_header("Output"),
                             ui.row(
                                 ui.column(4,
                                           ui.input_action_button(id="lineare_optimierung_button",
                                                                  label="linear optimization",
                                                                  disabled=True
                                                                  )
                                           ),
                                 ui.column(4,
                                           ui.input_action_button(id="Sensitivity_analysis_button",
                                                                  label="sensitivity analysis",
                                                                  disabled=True
                                                                  )

                                           ),
                                 ui.column(4,
                                           ui.input_action_button(id="save_graph_png",
                                                                  label="save graph as png",
                                                                  disabled=True
                                                                  )
                                           )

                             ),
                             ui.output_plot("optimierung_plot")
                         ),
                     )
                 ),
                 ),
    ui.nav_panel("How to use", "Page C content"),
    ui.nav_panel("Über", "Page C content"),
    title="OptiSense",
    id="page",
    # ui.input_slider("n", "Number of bins", 10, 100, 50),
    # ui.output_plot("hist"),
)
