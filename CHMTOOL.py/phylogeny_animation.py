import math

import manimgx as m

TREE = {'name': None, 'children': [({'name': 'Gamma', 'children': None}, 0.1875), ({'name': None, 'children': [({'name': 'Alpha', 'children': None}, 0.125), ({'name': 'Beta', 'children': None}, 0.125)]}, 0.0625)]}


class PhylogenyAnimation(m.ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=65 * m.DEGREES, theta=-45 * m.DEGREES, zoom=0.9)
        title = m.Text("UPGMA phylogeny", font_size=30)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(m.UP)

        def count_leaves(node):
            if node["children"] is None:
                return 1
            return sum(count_leaves(child) for child, _ in node["children"])

        def tree_height(node):
            if node["children"] is None:
                return 0.0
            return max(length + tree_height(child) for child, length in node["children"])

        leaf_count = count_leaves(TREE)
        radius = max(1.4, min(3.5, leaf_count * 0.25))
        vertical_scale = 4.0 / max(tree_height(TREE), 0.1)
        edge_specs = []
        node_positions = []
        leaf_specs = []
        leaf_index = 0

        def layout(node, height):
            nonlocal leaf_index
            if node["children"] is None:
                angle = 2 * math.pi * leaf_index / leaf_count
                position = [radius * math.cos(angle), radius * math.sin(angle), height]
                leaf_specs.append((node["name"], position, angle))
                leaf_index += 1
                node_positions.append(position)
                return position, 1

            child_positions = []
            for child, branch_length in node["children"]:
                child_position, child_count = layout(
                    child, height - branch_length * vertical_scale
                )
                child_positions.append((child_position, child_count))

            total_count = sum(count for _, count in child_positions)
            position = [
                sum(child_position[axis] * count for child_position, count in child_positions)
                / total_count
                for axis in range(3)
            ]
            for child_position, _ in child_positions:
                edge_specs.append((position, child_position))
            node_positions.append(position)
            return position, total_count

        layout(TREE, 0.0)
        edge_specs.reverse()
        edges = m.VGroup(*[
            m.Line3D(start, end, thickness=0.025, color=m.TEAL)
            for start, end in edge_specs
        ])
        nodes = m.VGroup(*[
            m.Dot3D(point, radius=0.07, color=m.GOLD)
            for point in node_positions
        ])
        labels = m.VGroup(*[
            m.Text(name, font_size=20).move_to([
                point[0] + 0.3 * math.cos(angle),
                point[1] + 0.3 * math.sin(angle),
                point[2],
            ])
            for name, point, angle in leaf_specs
        ])

        self.play(m.FadeIn(edges), run_time=2)
        self.play(m.FadeIn(nodes), run_time=1)
        self.play(m.LaggedStart(*[m.Write(label) for label in labels], lag_ratio=0.15), run_time=2)
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(3)
        self.stop_ambient_camera_rotation()
