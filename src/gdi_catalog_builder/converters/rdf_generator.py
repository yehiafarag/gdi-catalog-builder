from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, DCTERMS

from gdi_catalog_builder.models.catalog import Catalog


class RDFGenerator:
    """Create an RDF graph from a catalog model in DCAT/GDI terms."""

    def generate_catalog_graph(self, catalog: Catalog) -> Graph:
        graph = Graph()

        # Namespaces
        dcat = Namespace("http://www.w3.org/ns/dcat#")
        foaf = Namespace("http://xmlns.com/foaf/0.1/")
        adms = Namespace("http://www.w3.org/ns/adms#")
        dcatap = Namespace("http://data.europa.eu/r5r/")
        healthdcatap = Namespace("http://healthdataportal.eu/ns/health#")
        gdi = Namespace("http://data.gdi.eu/core/p2/")


        graph.bind("dcat", dcat)
        graph.bind("dct", DCTERMS)
        graph.bind("foaf", foaf)
        graph.bind("adms", adms)
        graph.bind("dcatap", dcatap)
        graph.bind("healthdcatap", healthdcatap)
        graph.bind("gdi", gdi)


# Catalog
        catalog_uri = URIRef("https://example.no/catalog")

        graph.add((catalog_uri, RDF.type, dcat.Catalog))
        graph.add((catalog_uri, DCTERMS.title, Literal(catalog.title)))

        if catalog.description:
            graph.add(
                (
                    catalog_uri,
                    DCTERMS.description,
                    Literal(catalog.description),
                )
            )
        for legislation in catalog.applicable_legislation:
            graph.add(
                (
                    catalog_uri,
                    dcatap.applicableLegislation,
                    URIRef(legislation),
                )
            )
        # Datasets
        for dataset in catalog.datasets:

            dataset_uri = URIRef(
                f"https://example.no/dataset/{dataset.title.replace(' ', '_')}"
            )

            graph.add((catalog_uri, dcat.dataset, dataset_uri))
            graph.add((dataset_uri, RDF.type, dcat.Dataset))
            graph.add((dataset_uri, DCTERMS.title, Literal(dataset.title)))


            if dataset.identifier:
                graph.add(
                    (
                        dataset_uri,
                        DCTERMS.identifier,
                        Literal(dataset.identifier),
                    )
                )


            if dataset.description:
                graph.add(
                    (
                        dataset_uri,
                        DCTERMS.description,
                        Literal(dataset.description),
                    )
                )
            if dataset.access_rights:
                graph.add(
                    (
                        dataset_uri,
                        DCTERMS.accessRights,
                        URIRef(dataset.access_rights),
                    )
                )
            for legislation in dataset.applicable_legislation:
                graph.add(
                    (
                        dataset_uri,
                        dcatap.applicableLegislation,
                        URIRef(legislation),
                    )
                )

            # Distributions
            for distribution in dataset.distributions:

                distribution_uri = URIRef(
                    f"{dataset_uri}/distribution/{distribution.title.replace(' ', '_')}"
                )

                graph.add(
                    (
                        dataset_uri,
                        dcat.distribution,
                        distribution_uri,
                    )
                )

                graph.add(
                    (
                        distribution_uri,
                        RDF.type,
                        dcat.Distribution,
                    )
                )

                graph.add(
                    (
                        distribution_uri,
                        DCTERMS.title,
                        Literal(distribution.title),
                    )
                )

                graph.add(
                    (
                        distribution_uri,
                        dcat.accessURL,
                        URIRef(distribution.access_url),
                    )
                )

            # Creators
            for creator in dataset.creators:

                creator_uri = URIRef(
                    f"{dataset_uri}/creator/{creator.name.replace(' ', '_')}"
                )

                graph.add((creator_uri, RDF.type, foaf.Agent))

                graph.add(
                    (
                        creator_uri,
                        foaf.name,
                        Literal(creator.name),
                    )
                )

                graph.add(
                    (
                        dataset_uri,
                        DCTERMS.creator,
                        creator_uri,
                    )
                )

            # Publisher
            if dataset.publisher:

                publisher_uri = URIRef(
                    f"{dataset_uri}/publisher/{dataset.publisher.name.replace(' ', '_')}"
                )

                graph.add((publisher_uri, RDF.type, foaf.Agent))

                graph.add(
                    (
                        publisher_uri,
                        foaf.name,
                        Literal(dataset.publisher.name),
                    )
                )

                graph.add(
                    (
                        dataset_uri,
                        DCTERMS.publisher,
                        publisher_uri,
                    )
                )

            # Identifiers
            for identifier in dataset.identifiers:

                identifier_uri = URIRef(
                    f"{dataset_uri}/identifier/{identifier.notation}"
                )

                graph.add(
                    (
                        dataset_uri,
                        adms.identifier,
                        identifier_uri,
                    )
                )

                graph.add(
                    (
                        identifier_uri,
                        RDF.type,
                        adms.Identifier,
                    )
                )

                graph.add(
                    (
                        identifier_uri,
                        adms.notation,
                        Literal(identifier.notation),
                    )
                )

                if identifier.schema_agency:
                    graph.add(
                        (
                            identifier_uri,
                            adms.schemaAgency,
                            Literal(identifier.schema_agency),
                        )
                    )

                if identifier.name:
                    graph.add(
                        (
                            identifier_uri,
                            DCTERMS.title,
                            Literal(identifier.name),
                        )
                    )
            for health_category in dataset.health_category:
                graph.add(
                    (
                        dataset_uri,
                        healthdcatap.healthCategory,
                        URIRef(health_category),
                    )
                )
            for theme in dataset.theme:
                graph.add(
                    (
                        dataset_uri,
                        dcat.theme,
                        URIRef(theme),
                    )
                )
        return graph