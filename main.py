import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from kivy.animation import Animation
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
IMAGE_SCREEN_NAME = 'image_screen'
ADMIN_SCREEN_NAME = 'admin'
STANFORD_SCREEN_NAME = 'stanford_screen'

class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """

    def clickPressed(self, label):
        clicks = int(label)
        clicks = clicks +1
        clicks = str(clicks)
        self.ids.click_counter.text = clicks

    def togglePressed(self, label):
        toggle = label
        if toggle == "On":
            self.ids.toggle_text.text = "Off"
        else:
            self.ids.toggle_text.text = "On"

    def motorPressed(self, label):
        toggle = label
        if toggle == "Motor On":
            self.ids.toggle_motor_label.text = "Motor Off"
        else:
            self.ids.toggle_motor_label.text = "Motor On"


    def imagePressed(self):

        SCREEN_MANAGER.current = 'image_screen'

    def stanfordPressed(self):

        anim_to_random_pos()
        SCREEN_MANAGER.current = 'image_screen'


    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        PauseScreen.pause(pause_scene_name='pauseScene', transition_back_scene='main', text="Test", pause_duration=5)

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'

    def anim_to_random_pos(self):
        random_x = random() * (Window.width - self.width)
        random_y = random() * (Window.height - self.height)

        anim = Animation(x=random_x, y=random_y,
                             duration=4,
                             t='in_sine')
        anim.start(self)



class ImageScreen(Screen):
    def __init__(self, **kwargs):
        Builder.load_file('ImageScreen.kv')
        super(ImageScreen, self).__init__(**kwargs)
    def imageBack(self):

        SCREEN_MANAGER.current = 'main'

class StanfordScreen(Screen):
    def __init__(self, **kwargs):
            Builder.load_file('StanfordScreen.kv')
            super(StanfordScreen, self).__init__(**kwargs)

    def imageBack(self):
        SCREEN_MANAGER.current = 'main'

class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(
            ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(
            MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(ImageScreen(name=IMAGE_SCREEN_NAME))
SCREEN_MANAGER.add_widget(StanfordScreen(name=STANFORD_SCREEN_NAME))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
