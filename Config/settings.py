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
        super().__init__(parent=parent)
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.cb = callback
        self.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

    def setupUi(self, shortcut: str, Version: str, langs: list, current_lang: str, backside: bool) -> None:
        self.ui.lookupTrigger.setKeySequence(QKeySequence(shortcut))
        self.ui.version.setText(f"v {Version}")
        self.ui.languageSelector.addItems(langs)
        self.ui.languageSelector.setCurrentText(current_lang)
        self.ui.checkBox.setChecked(backside)

    def accept(self):
        lookupTrigger = self.ui.lookupTrigger.keySequence().toString()
        lang = self.ui.languageSelector.currentText()
        f_or_b = self.ui.checkBox.isChecked()
        self.cb(lookupTrigger, lang, f_or_b)
        super().accept()
