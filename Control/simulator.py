from Components.wire import Wire

class Simulator():
    def __init__(self, scene=None):
        self.scene = scene
        self.connections = []

    def simulate(self):
        self.create_connections()
        self.propagate_signals()   

    def create_connections(self):
        self.connections.clear()  # Clear connections for each simulation run

        if not self.scene:
            return
        
        for item in self.scene.items():
            if isinstance(item, Wire):
                for comp in self.scene.items():
                    if hasattr(comp, 'conns'):
                        for conn in comp.conns:
                            if conn.type == 'output':
                                wire_pos = item.line().p1()
                                conn_pos = conn.scenePos()
                                if wire_pos == conn_pos:
                                    self.connections.append((item, comp, conn, conn.type))
                            if conn.type == 'input':
                                wire_pos = item.line().p2()
                                conn_pos = conn.scenePos()
                                if wire_pos == conn_pos:
                                    self.connections.append((item, comp, conn, conn.type))

    def propagate_signals(self):
        # First, propagate output states to wires
        for wire, comp, conn, conn_type in self.connections:
            if conn_type == 'output':
                wire.update_state(conn.state)

        # Then, propagate wire states to input connections
        for wire, comp, conn, conn_type in self.connections:
            if conn_type == 'input':
                conn.update_state(wire.state)
                comp.update()