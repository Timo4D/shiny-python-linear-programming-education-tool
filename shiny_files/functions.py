#from server import target_functions_list
import numpy as np
import math

def function_as_text(list):
    if len(list) == 7:
        return f"({list[0]}) ({str(list[1])}) * x1 + ({str(list[3])}) * x2 {str(list[5])} {str(list[6])}"
    elif len(list) == 6:
        return f"{list[0]} = ({str(list[1])}) * x1 + ({str(list[3])}) * x2 | {str(list[5])}"
    else:
        return "Function not found"

def calculate_highest_xlim_ylim(xlim_list, ylim_list):
    highest_x1 = 0
    highest_x2 = 0
    for x1 in xlim_list:
        if x1 > highest_x1:
            highest_x1 = x1
    for x2 in ylim_list:
        if x2 > highest_x2:
            highest_x2 = x2
    return [highest_x1, highest_x2]

def calculate_schnittpunkte_x1_x2_axis(function, xlim = None, ylim = None):
    if len(function) == 7:
        schnittpunkt_x1 = (function[6] / function[1])
        schnittpunkt_x2 = (function[6] / function[3])
        return [schnittpunkt_x1, schnittpunkt_x2]
    if len(function) == 6:

        xlim_lower_border = None
        xlim_upper_border = None
        ylim_lower_border = None
        ylim_upper_border = None

        if len(xlim) == 0:
            xlim_lower_border = 0
            xlim_upper_border = 1
        elif len(xlim) == 1:
            xlim_lower_border = 0
            xlim_upper_border = xlim[0]
        elif len(xlim) >= 2:
            xlim_lower_border = min(xlim)
            xlim_upper_border = max(xlim)

        if len(ylim) == 0:
            ylim_lower_border = 0
            ylim_upper_border = 1
        elif len(ylim) == 1:
            ylim_lower_border = 0
            ylim_upper_border = ylim[0]
        elif len(ylim) >= 2:
            ylim_lower_border = min(ylim)
            ylim_upper_border = max(ylim)

        intervall_xlim = np.arange(xlim_lower_border, xlim_upper_border, 0.1)
        intervall_ylim = np.arange(ylim_lower_border, ylim_upper_border, 0.1)

        laenge_intervall_xlim = len(intervall_xlim)
        laenge_intervall_ylim = len(intervall_ylim)

        #mittlerer_intervall_wert_xlim = (math.ceil(intervall_xlim[(laenge_intervall_xlim // 2)] * 2) / 2)
        mittlerer_intervall_wert_ylim = (math.ceil(intervall_ylim[(laenge_intervall_ylim // 2)] * 2) / 2)

        zielfunktion_erg = function[1] * mittlerer_intervall_wert_ylim

        schnittpunkt_x1_axis = (zielfunktion_erg / function[3])

        schnittpunkt_x2_axis = mittlerer_intervall_wert_ylim

        return [schnittpunkt_x1_axis, schnittpunkt_x2_axis]
#def find_function_by_dict_entry(dict_entry):
  #  ordnungszahl_liste = 0
 #   for function in target_functions_list:
  #      if function[0] == dict_entry:
  #          return ordnungszahl_liste
  #      ordnungszahl_liste += 1



#def update_function(self, name = "", x1 = "", attribute_1 = "", x2 = "", attribute_2 = ""):
#    if name != "":
#        self.name = name
#    if x1 != "":
#        self.x1 = x1
#    if attribute_1 != "":
#        self.attribute_1 = attribute_1
#    if x2 != "":
#        self.x2 = x2
#    if attribute_2 != "":
#        self.attribute_2 = attribute_2

#def update_target_function(self, name = "", x1 = "", attribute_1 = "", x2 = "", attribute_2 = "", min_max = ""):
#    if name != "":
#        self.name = name
#    if x1 != "":
#        self.x1 = x1
#    if attribute_1 != "":
#        self.attribute_1 = attribute_1
#    if x2 != "":
#        self.x2 = x2
#    if attribute_2 != "":
#        self.attribute_2 = attribute_2
#    if min_max != "":
#        self.min_max = min_max


#def delete_function(self):
#    function_list.remove(self)
#    del self


#def move_target_function_to_front():

#    for function in Functions.function_list:
 #       if isinstance(Functions.function_list[0], TargetFunctions): #ACHTUNG VLLT EHER MIT TYPE!!!!
 #           break
 #       if isinstance(function, TargetFunctions):
 #           Functions.function_list.remove(function)
 #           Functions.function_list.append(Functions.function_list[0])
 #           Functions.function_list[0] = function
 #           break


#def summarize_functions_text():
#    summarized_text = ""
#    for function in Functions.function_list:

#    summarized_text += "<br>" + function.as_text() + "<br>"
 #   return ui.HTML(summarized_text)