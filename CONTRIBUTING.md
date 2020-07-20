There is a console app with command-line arguments, `zero_play`, but there's
also an experimental GUI app, `zero_play_gui`. To edit the GUI, do the
following:

1. Download and install [Qt Creator].
2. Run Qt Creator, and open the `.ui` file for the screen you want to change.
3. Read the [Qt Designer documentation], and make the changes you want.
4. Compile the `.ui` file into a Python source file with a command like this:

        pyside2-uic -o main_window.py main_window.ui

To add a new screen to the project:

1. In Qt Creator choose New File or Project from the File menu.
2. In the Qt section, choose Qt Designer Form.
3. Select a widget type, like "Widget", and choose a file name.

[Qt Creator]: https://www.qt.io/download-qt-installer
[Qt Designer documentation]: https://doc.qt.io/qt-5/designer-quick-start.html