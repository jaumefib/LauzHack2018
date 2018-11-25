class NiceJourney:
    """Problem of finding a better graph for the traveling options"""

    def __init__(self, initial):
        self.initial = initial

    def actions(self, state):
        """Returns the list of actions which are allowed to be taken from the given state"""
        allowed_actions = ["increment", "discrease"]
        return allowed_actions

    def value(self, state):
        """Value of the state"""

    def result(self, state, action):
        """Modify the state with the selected action"""
        modify(state,action)

