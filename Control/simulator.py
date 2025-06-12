from Components.wire import Wire
from Components.wire_group import WireGroup

class Simulator():
    def __init__(self, scene=None):
        self.scene = scene
        self.wire_groups = []
        self.connections = []
        self.num_scans = 3

    def simulate(self):
        self.create_wire_groups()
        self.create_connections()
        for _ in range(self.num_scans):
            self.propagate_signals()

    def create_wire_groups(self):
        """
        Groups wires that are electrically connected (i.e., their endpoints touch).
        Each group is a list of wires, wrapped in a WireGroup.
        """
        self.wire_groups = []

        if not self.scene:
            return

        # Gather all wires from the scene
        wires = [item for item in self.scene.items() if isinstance(item, Wire)]
        visited = set()

        def find_connected_wires(wire, visited, group):
            if wire in visited:
                return
            visited.add(wire)
            group.append(wire)

            for other_wire in wires:
                if other_wire in visited or other_wire is wire:
                    continue
                # Compare endpoints
                w1_p1, w1_p2 = wire.line().p1(), wire.line().p2()
                w2_p1, w2_p2 = other_wire.line().p1(), other_wire.line().p2()
                if (w1_p2 == w2_p1 or w1_p1 == w2_p2 or
                    w1_p1 == w2_p1 or w1_p2 == w2_p2):
                    find_connected_wires(other_wire, visited, group)

        for wire in wires:
            if wire not in visited:
                group = []
                find_connected_wires(wire, visited, group)
                wire_group = WireGroup(group)
                self.wire_groups.append(wire_group)

    def create_connections(self):
        self.connections.clear()  # Clear connections for each simulation run

        if not self.scene:
            return

        # Use wire groups instead of individual wires
        for wire_group in self.wire_groups:
            # For each wire in the group, check both endpoints
            group_points = []
            for wire in wire_group.wires:
                group_points.append(wire.line().p1())
                group_points.append(wire.line().p2())

            for comp in self.scene.items():
                if hasattr(comp, 'conns'):
                    for conn in comp.conns:
                        conn_pos = conn.scenePos()
                        if conn.type == 'output':
                            # If any group endpoint matches the connection, add connection
                            if conn_pos in group_points:
                                self.connections.append((wire_group, comp, conn, conn.type))
                        if conn.type == 'input':
                            if conn_pos in group_points:
                                self.connections.append((wire_group, comp, conn, conn.type))
   
    def propagate_signals(self):
        # First, propagate output states to wire groups
        for wire_group, comp, conn, conn_type in self.connections:
            if conn_type == 'output':
                # Update the state of all wires in the group
                for wire in wire_group.wires:
                    wire.update_state(conn.state)

        # Then, propagate wire group states to input connections
        for wire_group, comp, conn, conn_type in self.connections:
            if conn_type == 'input':
                # Use the state of the first wire in the group (assuming all wires in a group share state)
                if wire_group.wires:
                    conn.update_state(wire_group.wires[0].state)
                    comp.update()

    def print_connections(self):
        for wire_group, comp, conn, conn_type in self.connections:
            print(f"WireGroup: {wire_group}, Component: {comp.__class__.__name__}, Connection: {conn.name}, Type: {conn_type}")