import gi
import optimization

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


def add_filters(dialog):
    filter_text = Gtk.FileFilter()
    filter_text.set_name("Text files")
    filter_text.add_mime_type("text/csv")
    dialog.add_filter(filter_text)

    filter_any = Gtk.FileFilter()
    filter_any.set_name("Any files")
    filter_any.add_pattern("*")
    dialog.add_filter(filter_any)


def get_max(samples):
    max_value = 0.0
    size = len(samples)
    for i in range(size):
        if i == 0:
            max_value = samples[i]
        else:
            if samples[i] > max_value:
                max_value = samples[i]

    return max_value


def scale(samples):
    n = len(samples[0])
    m = len(samples)
    for j in range(n):
        features = []
        for i in range(m):
            features.append(samples[i][j])

        max_value = get_max(features)

        for i in range(m):
            samples[i][j] = samples[i][j] / max_value


class Main(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Gradiente descendente")

        table = Gtk.Table(5, 3, True)
        self.add(table)

        table.set_row_spacing(0, 5)
        table.set_col_spacing(0, 10)

        self.field_entry_x = Gtk.Entry()
        self.field_entry_y = Gtk.Entry()
        self.field_alpha = Gtk.Entry()
        self.field_tolerance = Gtk.Entry()
        self.iterations_field = Gtk.Entry()
        self.analyze_button = Gtk.Button(label="Analizar")
        self.get_x_samples_button = Gtk.Button(label="...")
        self.get_y_samples_button = Gtk.Button(label="...")

        table.attach(Gtk.Label("Archivo de X"), 0, 1, 1, 3)
        table.attach(self.field_entry_x, 1, 3, 1, 3)
        table.attach(self.get_x_samples_button, 3, 4, 1, 3)
        table.attach(Gtk.Label("Archivo de Y"), 0, 1, 3, 5)
        table.attach(self.field_entry_y, 1, 3, 3, 5)
        table.attach(self.get_y_samples_button, 3, 4, 3, 5)
        table.attach(Gtk.Label("Alpha"), 0, 1, 5, 7)
        table.attach(self.field_alpha, 1, 3, 5, 7)
        table.attach(Gtk.Label("Tolerancia"), 0, 1, 7, 9)
        table.attach(self.field_tolerance, 1, 3, 7, 9)
        table.attach(Gtk.Label("Iteraciones"), 0, 1, 9, 11)
        table.attach(self.iterations_field, 1, 3, 9, 11)
        table.attach(self.analyze_button, 3, 4, 11, 13)

        self.get_x_samples_button.connect("clicked", self.button_x_on_click)
        self.get_y_samples_button.connect("clicked", self.button_y_on_click)
        self.analyze_button.connect("clicked", self.analyze_on_click)

    def button_x_on_click(self, widget):
        chooser = Gtk.FileChooserDialog("Seleccionar un archivo", self,
                                        Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                         Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        add_filters(chooser)
        response = chooser.run()

        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + chooser.get_filename())
            self.field_entry_x.set_text(chooser.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        chooser.destroy()

    def button_y_on_click(self):
        chooser = Gtk.FileChooserDialog("Seleccionar un archivo", self,
                                        Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                         Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        add_filters(chooser)
        response = chooser.run()

        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + chooser.get_filename())
            self.field_entry_y.set_text(chooser.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        chooser.destroy()

    def analyze_on_click(self):
        if self.field_entry_x.get_text() is None:
            return

        if self.field_entry_y.get_text() is None:
            return

        if self.field_alpha.get_text() is None:
            return

        if self.field_tolerance.get_text() is None:
            return

        if self.iterations_field.get_text() is None:
            return

        file_x = open(self.field_entry_x.get_text(), 'rU')

        file_y = open(self.field_entry_y.get_text(), 'rU')

        if file_x is not None and file_y is not None:
            alpha = float(self.field_alpha.get_text())
            tol = float(self.field_tolerance.get_text())
            it = float(self.iterations_field.get_text())

            samples_on_x = []
            for line in file_x:
                elements = line.strip().split(',')
                for i in range(len(elements)):
                    elements[i] = float(elements[i])

                samples_on_x.append(elements)

            samples_on_y = []
            for line in file_y:
                elements = line.strip().split(',')
                for i in range(len(elements)):
                    elements[i] = float(elements[i])

                samples_on_y.append(elements)

            result = optimization.gradient_descent(samples_on_x, samples_on_y, alpha, tol, it)

            if result is not None:
                res_path = self.field_entry_x.get_text() + '.res'
                response_file = open(res_path, 'w')

                str_res = ""
                for i in range(len(result)):
                    str_res += repr(result[i])
                    if i < len(result) - 1:
                        str_res += "\r"

                response_file.write(str_res)

        else:
            return


win = Main()

win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
