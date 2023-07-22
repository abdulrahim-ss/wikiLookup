from aqt import QDialog, QLayout, QKeySequence, qtmajor

if qtmajor < 6:
    from .qt.qt5.config_settings import Ui_Settings
else:
    from .qt.qt6.config_settings import Ui_Settings

class Settings(QDialog):
    """
    Dialog shown when clicking on "Config" in the Add-ons window.
    """

    def __init__(self, parent, callback):
        """
            Callback function handles passing the settings values along to the rest of the add-on code.
        """
        super().__init__(parent=parent)
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.cb = callback
        self.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

    def setupUi(self, shortcut: str, Version: str, backside: bool) -> None:
        """
            Sets the values for the UI elements in the config dialogue. Called upon initialization.
        """
        self.ui.lookupTrigger.setKeySequence(QKeySequence(shortcut))
        self.ui.version.setText(f"v {Version}")
        # self.ui.languageSelector.addItems(langs)
        # self.ui.languageSelector.setCurrentText(current_lang)
        self.ui.checkBox.setChecked(backside)

    def accept(self):
        """
            Called when user clicks on the "accept" button. Passes through the settings values to the callback
            function - which is passed through as a parameter to the class upon initialization.
        """
        lookupTrigger = self.ui.lookupTrigger.keySequence().toString()
        # lang = self.ui.languageSelector.currentText()
        f_or_b = self.ui.checkBox.isChecked()
        self.cb(lookupTrigger, f_or_b)
        super().accept()
