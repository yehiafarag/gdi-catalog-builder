from datetime import datetime, timezone

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, XSD

from gdi_catalog_builder.models.catalog import Catalog


class RDFGenerator:
    """Create an RDF graph from a catalog model in DCAT/GDI terms."""

    base_url = "http://gdi-norway.onemilliongenomes.eu"

    def generate_catalog_graph(self, catalog: Catalog) -> Graph:
        graph = Graph()

        dcat = Namespace("http://www.w3.org/ns/dcat#")
        foaf = Namespace("http://xmlns.com/foaf/0.1/")
        adms = Namespace("http://www.w3.org/ns/adms#")
        dcatap = Namespace("http://data.europa.eu/r5r/")
        healthdcatap = Namespace("http://healthdataportal.eu/ns/health#")
        gdi = Namespace("http://data.gdi.eu/core/p2/")
        vcard = Namespace("http://www.w3.org/2006/vcard/ns#")

        graph.bind("dcat", dcat)
        graph.bind("dct", DCTERMS)
        graph.bind("foaf", foaf)
        graph.bind("adms", adms)
        graph.bind("dcatap", dcatap)
        graph.bind("healthdcatap", healthdcatap)
        graph.bind("gdi", gdi)
        graph.bind("vcard", vcard)

        current_datetime = datetime.now(timezone.utc)
        catalog_uri = URIRef(f"{self.base_url}/catalog/2")

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
            if legislation and legislation.strip():
                graph.add(
                    (
                        catalog_uri,
                        dcatap.applicableLegislation,
                        URIRef(legislation.strip()),
                    )
                )

        graph.add(
            (
                catalog_uri,
                DCTERMS.modified,
                Literal(
                    current_datetime.isoformat(),
                    datatype=XSD.dateTime,
                ),
            )
        )

        for dataset_index, dataset in enumerate(catalog.datasets):
            dataset_identifier = dataset.identifier or f"dataset-{dataset_index + 1}"
            dataset_uri = URIRef(f"{self.base_url}/dataset/{dataset_identifier}")

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
                if legislation and legislation.strip():
                    graph.add(
                        (
                            dataset_uri,
                            dcatap.applicableLegislation,
                            URIRef(legislation.strip()),
                        )
                    )

            for standard in dataset.conforms_to:
                if standard and standard.strip():
                    graph.add(
                        (
                            dataset_uri,
                            DCTERMS.conformsTo,
                            URIRef(standard.strip()),
                        )
                    )

            for distribution_index, distribution in enumerate(dataset.distributions):
                distribution_uri = URIRef(
                    f"{dataset_uri}/distribution/{distribution_index + 1}"
                )

                graph.add((dataset_uri, dcat.distribution, distribution_uri))
                graph.add((distribution_uri, RDF.type, dcat.Distribution))

                if distribution.title and distribution.title.strip():
                    graph.add(
                        (
                            distribution_uri,
                            DCTERMS.title,
                            Literal(distribution.title.strip(), lang="en"),
                        )
                    )

                for language, description in distribution.description.items():
                    if description and description.strip():
                        graph.add(
                            (
                                distribution_uri,
                                DCTERMS.description,
                                Literal(description.strip(), lang=language),
                            )
                        )

                for legislation in distribution.applicable_legislation:
                    if legislation and legislation.strip():
                        graph.add(
                            (
                                distribution_uri,
                                dcatap.applicableLegislation,
                                URIRef(legislation.strip()),
                            )
                        )

                if distribution.format:
                    graph.add(
                        (
                            distribution_uri,
                            DCTERMS.format,
                            Literal(distribution.format),
                        )
                    )

                if distribution.access_url:
                    graph.add(
                        (
                            distribution_uri,
                            dcat.accessURL,
                            URIRef(distribution.access_url),
                        )
                    )

                if distribution.download_url:
                    graph.add(
                        (
                            distribution_uri,
                            dcat.downloadURL,
                            URIRef(distribution.download_url),
                        )
                    )

                if distribution.media_type:
                    graph.add(
                        (
                            distribution_uri,
                            dcat.mediaType,
                            Literal(distribution.media_type),
                        )
                    )

                if distribution.issued:
                    graph.add(
                        (
                            distribution_uri,
                            DCTERMS.issued,
                            Literal(distribution.issued, datatype=XSD.dateTime),
                        )
                    )

                distribution_modified = distribution.modified or current_datetime.isoformat()
                graph.add(
                    (
                        distribution_uri,
                        DCTERMS.modified,
                        Literal(distribution_modified, datatype=XSD.dateTime),
                    )
                )

                rights_statements = {
                    language: statement.strip()
                    for language, statement in distribution.rights.items()
                    if statement and statement.strip()
                }
                if rights_statements:
                    rights_node = BNode()
                    graph.add((distribution_uri, DCTERMS.rights, rights_node))
                    graph.add((rights_node, RDF.type, DCTERMS.RightsStatement))
                    for language, statement in rights_statements.items():
                        graph.add(
                            (
                                rights_node,
                                RDFS.label,
                                Literal(statement, lang=language),
                            )
                        )

                if distribution.status:
                    graph.add(
                        (
                            distribution_uri,
                            adms.status,
                            URIRef(distribution.status),
                        )
                    )

            for creator in dataset.creators:
                creator_node = BNode()
                graph.add((dataset_uri, DCTERMS.creator, creator_node))
                graph.add((creator_node, RDF.type, foaf.Agent))
                if creator.name:
                    graph.add((creator_node, foaf.name, Literal(creator.name)))
                if creator.identifier:
                    graph.add(
                        (
                            creator_node,
                            DCTERMS.identifier,
                            URIRef(creator.identifier),
                        )
                    )

            if dataset.publisher:
                publisher_node = BNode()
                graph.add((dataset_uri, DCTERMS.publisher, publisher_node))
                graph.add((publisher_node, RDF.type, foaf.Agent))
                if dataset.publisher.name:
                    graph.add(
                        (
                            publisher_node,
                            foaf.name,
                            Literal(dataset.publisher.name),
                        )
                    )
                if dataset.publisher.identifier:
                    graph.add(
                        (
                            publisher_node,
                            DCTERMS.identifier,
                            URIRef(dataset.publisher.identifier),
                        )
                    )

            if dataset.issued:
                graph.add(
                    (
                        dataset_uri,
                        DCTERMS.issued,
                        Literal(dataset.issued, datatype=XSD.dateTime),
                    )
                )

            if dataset.modified or dataset.issued:
                graph.add(
                    (
                        dataset_uri,
                        DCTERMS.modified,
                        Literal(
                            (dataset.modified or current_datetime.isoformat()),
                            datatype=XSD.dateTime,
                        ),
                    )
                )

            for identifier in dataset.identifiers:
                identifier_uri = URIRef(
                    f"{dataset_uri}/identifier/{identifier.notation}"
                )
                graph.add((dataset_uri, adms.identifier, identifier_uri))
                graph.add((identifier_uri, RDF.type, adms.Identifier))
                graph.add((identifier_uri, adms.notation, Literal(identifier.notation)))
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
                if health_category and health_category.strip():
                    graph.add(
                        (
                            dataset_uri,
                            healthdcatap.healthCategory,
                            URIRef(health_category.strip()),
                        )
                    )

            for theme in dataset.theme:
                if theme and theme.strip():
                    graph.add(
                        (
                            dataset_uri,
                            dcat.theme,
                            URIRef(theme.strip()),
                        )
                    )

            provenance_statements = {
                language: statement.strip()
                for language, statement in dataset.provenance.items()
                if statement and statement.strip()
            }
            if provenance_statements:
                provenance_node = BNode()
                graph.add((dataset_uri, DCTERMS.provenance, provenance_node))
                graph.add((provenance_node, RDF.type, DCTERMS.ProvenanceStatement))
                for language, statement in provenance_statements.items():
                    graph.add(
                        (
                            provenance_node,
                            RDFS.label,
                            Literal(statement, lang=language),
                        )
                    )

            if dataset.type:
                graph.add((dataset_uri, DCTERMS.type, URIRef(dataset.type)))

            for language, note in dataset.version_notes.items():
                if note and note.strip():
                    graph.add(
                        (
                            dataset_uri,
                            adms.versionNotes,
                            Literal(note.strip(), lang=language),
                        )
                    )

            for contact_point in dataset.contact_points:
                normalized_email = None
                if contact_point.email:
                    normalized_email = contact_point.email.strip()
                    if not normalized_email.startswith("mailto:"):
                        normalized_email = f"mailto:{normalized_email}"

                if not (contact_point.fn and normalized_email):
                    continue

                contact_node = BNode()
                graph.add((dataset_uri, dcat.contactPoint, contact_node))
                graph.add((contact_node, RDF.type, vcard.Kind))

                if contact_point.fn:
                    graph.add((contact_node, vcard.fn, Literal(contact_point.fn)))
                if normalized_email:
                    graph.add(
                        (
                            contact_node,
                            vcard.hasEmail,
                            URIRef(normalized_email),
                        )
                    )
                if contact_point.identifier:
                    graph.add(
                        (
                            contact_node,
                            vcard.hasUID,
                            URIRef(contact_point.identifier),
                        )
                    )
                if contact_point.url:
                    graph.add(
                        (
                            contact_node,
                            vcard.hasURL,
                            URIRef(contact_point.url),
                        )
                    )

            for keyword in dataset.keyword:
                if keyword and keyword.strip():
                    graph.add(
                        (
                            dataset_uri,
                            dcat.keyword,
                            Literal(keyword.strip(), lang="en"),
                        )
                    )

        return graph
