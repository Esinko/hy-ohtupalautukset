from sovelluslogiikka import Sovelluslogiikka

class BaseKomento:
    def __init__(self, operator: Sovelluslogiikka, operand: int | float) -> None:
        self._operator = operator
        self._operand = operand
        self._original_value = self._operator.arvo()

    def kumoa(self):
        self._operator.aseta_arvo(self._original_value)

class RevertableBaseKomento(BaseKomento):
    def __init__(self, previous_command: BaseKomento | None, **base_params):
        super().__init__(**base_params)
        self._previous_command = previous_command

    def suorita(self):
        pass

class Summa(RevertableBaseKomento):
    def suorita(self):
        self._operator.plus(self._operand)

class Erotus(RevertableBaseKomento):
    def suorita(self):
        self._operator.miinus(self._operand)

class Nollaus(RevertableBaseKomento):
    def suorita(self):
        self._operator.nollaa()

class Kumoa(RevertableBaseKomento):
    def suorita(self):
        if not self._previous_command:
            raise RuntimeError("Nothing to undo.")
        self._previous_command.kumoa()
