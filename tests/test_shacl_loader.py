from gdi_catalog_builder.validators.shacl_loader import ShaclLoader


def test_load_shacl_shapes():

    graph = ShaclLoader.load_shapes(
        "schemas/gdi/PiecesShape"
    )

    assert len(graph) > 0