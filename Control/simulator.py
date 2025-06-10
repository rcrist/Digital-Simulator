from Components.wire import Wire

class Simulator():
    def __init__(self, scene=None):
        self.scene = scene
        self.connections = []
        self.num_scans = 3

    def simulate(self):
        self.create_connections()
        for _ in range(self.num_scans):
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
            # print(f"Propagating signal from {conn.name} of {comp.__class__.__name__} to wire")
            if conn_type == 'input':
                conn.update_state(wire.state)
                comp.update()

    def print_connections(self):
        for wire, comp, conn, conn_type in self.connections:
            print(f"Wire: {wire.name}, Component: {comp.__class__.__name__}, Connection: {conn.name}, Type: {conn_type}")