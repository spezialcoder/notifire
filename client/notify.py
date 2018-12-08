import gi
from gi.repository import GObject
gi.require_version('Notify', '0.7')
from gi.repository import Notify

class notify(GObject.Object):
        def __init__(self,app_name):

                    super(notify, self).__init__()
                            # lets initialise with the application name
                    Notify.init(app_name)

        def send(self, title, text, file_path_to_icon=""):

                    n = Notify.Notification.new(title, text, file_path_to_icon)
                    n.show()


