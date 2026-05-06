import copy

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = []
        self.loadNerc()
        self._listRightEvents = []
        self._bestCustomer = 0


    def worstCase(self, nerc, maxY, maxH):
        self._solBest = []
        self._bestCustomer = 0
        self._listRightEvents = []

        self.loadEvents(nerc)

        print("DEBUG MODEL")
        print("NERC selezionato:", nerc)
        print("Eventi caricati:", len(self._listEvents))

        for e in self._listEvents:
            durata = self._getDurationHours(e)
            if durata <= maxH:
                self._listRightEvents.append(e)

        print("Eventi candidati dopo filtro ore:", len(self._listRightEvents))

        self.ricorsione(
            pos = 0,
            parziale = [],
            maxY = maxY,
            maxH = maxH,
            currentHours = 0.0,
            currentCustomer = 0,
            minYear = None,
            maxYear = None
        )

        return self._solBest, self._bestCustomer


    def ricorsione(self, pos, parziale, maxY, maxH, currentHours, currentCustomer, minYear, maxYear):
        # CONDIZIONE TERMINALE
        if pos == len(self._listRightEvents):
            if currentCustomer > self._bestCustomer:
                self._bestCustomer = currentCustomer
                self._solBest = copy.deepcopy(parziale)
            return

        e = self._listRightEvents[pos]

        self.ricorsione(
            pos + 1,
            parziale,
            maxY,
            maxH,
            currentHours,
            currentCustomer,
            minYear,
            maxYear
        )

        durata = self._getDurationHours(e)
        nuoviHours = currentHours + durata

        eventYear = e._date_event_began.year
        nuovoMinYear = eventYear if minYear is None else min(minYear,  eventYear)
        nuovoMaxYear = eventYear if maxYear is None else max(maxYear, eventYear)

        if nuoviHours <= maxH and (nuovoMaxYear - nuovoMinYear) <= maxY:
            parziale.append(e)

            nuoviCustomers = currentCustomer + self._getCustomers(e)

            self.ricorsione(
                pos + 1,
                parziale,
                maxY,
                maxH,
                nuoviHours,
                nuoviCustomers,
                nuovoMinYear,
                nuovoMaxYear,
            )

            parziale.pop()


    def _getDurationHours(self, event):
        delta = event._date_event_finished - event._date_event_began
        return delta.total_seconds() / 3600.0

    def _getCustomers(self, event):
        return 0 if event._customers_affected is None else event._customers_affected


    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc