from kivy.app import App
from calc_view import Calc_view
from error_date import Error_date
import datetime
from kivy.core.window import Window

# Window.size = (320, 590)
Window.clearcolor = (0,0,0)

# Window.minimum_width = 320
# Window.minimum_height = 590
# Window.maximum_width = 320
# Window.maximum_height = 590

# Window.resizable = False


class Traitement(App):

    max_date = datetime.date(2024, 6, 6) # date de fin
    min_date = datetime.date(2024, 5, 3) # date de sorti
    cv = Calc_view()
    err = Error_date()

    def build(self):
        if datetime.datetime.now().date() > self.max_date or datetime.datetime.now().date() < self.min_date:
            return self.err
        else:
            return self.cv
    
