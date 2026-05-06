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
        nerc_id = self._view._ddNerc.value
        nerc = self._idMap[nerc_id]
        maxY = self._view._txtYears.value
        maxH = self._view._txtHours.value

        print("DEBUG CONTROLLER")
        print("nerc_id =", nerc_id)
        print("maxY =", maxY)
        print("maxH =", maxH)

        if nerc is None or maxY is None or maxH is None:
            self._view.create_alert("Select every field !")
            self._view.update_page()
            return

        if not int(maxH) or not  int(maxY):
            self._view.create_alert("Insert a coherent value !")
            self._view.update_page()
            return

        sol, best = self._model.worstCase(nerc, int(maxY), int(maxH))

        print("RISULTATO FINALE")
        print("best customers =", best)
        print("numero eventi soluzione =", len(sol))

        self._view._txtOut.controls.clear()
        self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {best}"))
        self._view._txtOut.controls.append(ft.Text(f"Tot number of outages: {len(sol)}"))

        for e in sol:
            self._view._txtOut.controls.append(
                ft.Text(
                    f"id={e._id}, customers_affected={e._customers_affected}, "
                    f"from={e._date_event_began}, to={e._date_event_finished}"
                )
            )

        self._view.update_page()

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(
                ft.dropdown.Option(
                    key = str(n.id),
                    text = n.value
                ))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[str(v.id)] = v
