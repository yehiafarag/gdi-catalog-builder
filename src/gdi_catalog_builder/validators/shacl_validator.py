from rdflib import Graph
from pyshacl import validate


class ShaclValidator:
    """Validate RDF data against the configured GDI SHACL shapes."""

    @staticmethod
    def validate_graph(
            data_graph: Graph,
            shapes_graph: Graph,
    ) -> tuple[bool, str]:

        conforms, _, report_text = validate(
            data_graph=data_graph,
            shacl_graph=shapes_graph,
            inference="rdfs",
            abort_on_first=False,
            allow_infos=True,
            allow_warnings=True,
        )

        return conforms, report_text