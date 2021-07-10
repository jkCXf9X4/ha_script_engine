
class LocalEventWrapper:
    def __init__(self, event) -> None:

        self.id = event.data.get("entity_id")

        self.new_state = event.data.get("new_state").state
        self.old_state = event.data.get("old_state")
        if self.old_state != None:
            self.old_state = self.old_state.state

        # self.new_state_attributes = self.new_state.get("attributes", None)
        # self.old_state_attributes = self.old_state.get("attributes", None)

        self.last_changed = event.data.get("last_changed", None)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, LocalEventWrapper):
            return NotImplemented
        return self.last_changed == o.last_changed
