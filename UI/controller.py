import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        # TO FILL
        nerc = self._view._ddNerc.value
        maxY = self._view._txtYears.value
        maxH = self._view._txtHours.value

        if nerc is None or maxY is None or maxH is None:
            self._view.create_alert("Select every field !")
            self._view.update_page()
            return

        if not int(maxH) or not  int(maxY):
            self._view.create_alert("Insert a coherent value !")
            self._view.update_page()
            return

        self._model.worstCase(nerc, maxY, maxH)





    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
