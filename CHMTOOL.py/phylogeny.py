import re

from animation import render_phylogeny_animation


def build_upgma_tree(names, sequences):
    if len(names) < 2 or len(names) != len(sequences):
        raise ValueError("Enter at least two named sequences.")
    if len(set(names)) != len(names):
        raise ValueError("Sequence names must be unique.")
    if any(not re.fullmatch(r"[A-Za-z0-9_.-]+", name) for name in names):
        raise ValueError("Use letters, numbers, underscores, dots, or hyphens in names.")
    if not sequences[0] or any(len(sequence) != len(sequences[0]) for sequence in sequences):
        raise ValueError("Sequences must all have the same nonzero aligned length.")

    allowed_bases = set("ACGTRYSWKMBDHVN-")
    if any(set(sequence) - allowed_bases for sequence in sequences):
        raise ValueError("Sequences may contain DNA bases, IUPAC ambiguity codes, and gaps.")

    clusters = {
        index: {
            "size": 1,
            "height": 0.0,
            "node": {"name": name, "children": None},
        }
        for index, name in enumerate(names)
    }
    distances = {}
    for first in range(len(sequences)):
        for second in range(first + 1, len(sequences)):
            comparable = [
                (left, right)
                for left, right in zip(sequences[first], sequences[second])
                if left in "ACGT" and right in "ACGT"
            ]
            if not comparable:
                raise ValueError(
                    "Each sequence pair needs at least one comparable A, C, G, or T site."
                )
            differences = sum(left != right for left, right in comparable)
            distances[(first, second)] = differences / len(comparable)

    next_cluster = len(names)
    while len(clusters) > 1:
        first, second = min(distances, key=distances.get)
        first_cluster = clusters[first]
        second_cluster = clusters[second]
        height = distances[(first, second)] / 2
        first_branch = max(0.0, height - first_cluster["height"])
        second_branch = max(0.0, height - second_cluster["height"])
        merged = {
            "size": first_cluster["size"] + second_cluster["size"],
            "height": height,
            "node": {
                "name": None,
                "children": [
                    (first_cluster["node"], first_branch),
                    (second_cluster["node"], second_branch),
                ],
            },
        }

        remaining = [cluster_id for cluster_id in clusters if cluster_id not in (first, second)]
        updated_distances = {
            pair: distance
            for pair, distance in distances.items()
            if first not in pair and second not in pair
        }
        for other in remaining:
            first_distance = distances[tuple(sorted((first, other)))]
            second_distance = distances[tuple(sorted((second, other)))]
            average = (
                first_cluster["size"] * first_distance
                + second_cluster["size"] * second_distance
            ) / merged["size"]
            updated_distances[tuple(sorted((next_cluster, other)))] = average

        del clusters[first]
        del clusters[second]
        clusters[next_cluster] = merged
        distances = updated_distances
        next_cluster += 1

    return clusters.popitem()[1]["node"]


def phylogeny_tree():
    print("\nUPGMA tree from aligned DNA sequences (p-distance)")
    try:
        sequence_count = int(input("Number of sequences (at least 2): "))
        if sequence_count < 2:
            print("Enter at least two sequences.")
            return
        names = []
        sequences = []
        for index in range(sequence_count):
            names.append(input("Sequence {} name: ".format(index + 1)).strip())
            sequences.append(input("Sequence {} DNA: ".format(index + 1)).strip().upper())
        root = build_upgma_tree(names, sequences)
    except ValueError as error:
        print("Could not build tree:", error)
        return

    print("\nTree (branch lengths are substitutions per site):")
    print("Root")

    def draw(node, prefix=""):
        for index, (child, branch_length) in enumerate(node["children"]):
            is_last = index == len(node["children"]) - 1
            connector = "`-- " if is_last else "|-- "
            label = child["name"] if child["name"] is not None else "clade"
            print(prefix + connector + "{} ({:.4g})".format(label, branch_length))
            if child["children"]:
                draw(child, prefix + ("    " if is_last else "|   "))

    def to_newick(node):
        if node["children"] is None:
            return node["name"]
        children = [
            "{}:{:.8g}".format(to_newick(child), branch_length)
            for child, branch_length in node["children"]
        ]
        return "(" + ",".join(children) + ")"

    draw(root)
    print("Newick:", to_newick(root) + ";")
    if input("Render a 3D animation with ManimGX? (y/N): ").strip().lower() == "y":
        render_phylogeny_animation(root)