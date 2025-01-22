from db.alerts import network_alerts_db

def alert_removal(self):
    selected_item = self.list_widget.currentItem()
    if selected_item is not None:
        self.list_widget.takeItem(self.list_widget.row(selected_item))

