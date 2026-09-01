from pathlib import Path

from rdflib import Graph


class ShaclLoader:
    """Load the SHACL .ttl files used to validate generated catalog data."""

    @staticmethod
    def load_shapes(directory: str) -> Graph:
        graph = Graph()

        for ttl_file in Path(directory).glob("*.ttl"):
            graph.parse(ttl_file, format="turtle")

        return graph