from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class Error_date(BoxLayout):

    def __init__(self, **kwargs):
        super(Error_date, self).__init__(**kwargs)
        Window.size = (320, 590)
        Window.clearcolor = (0, 0, 0, 1)
        self.orientation = 'vertical'
        self.add_widget(Label(text = "ERROR!!!", color = (1, 0, 0, 1), font_size = 32, bold = True))
        self.add_widget(Label(text = "VERSION OBSOLETE", color = (1, 0, 0, 1), font_size = 22, bold = True))
        self.add_widget(Label(text = "Demander au developpeur l'autre version\npour continuer a l'utiliser.", color = (1, 1, 1, 1), font_size = 16))
        self.add_widget(Label(text = "Merci d'avoir tester mon APP!!!", color = (48/255, 84/255, 150/255, 1), font_size = 16))
