from scripts import clustering


def _ident(**kw):
    base = {
        "make": "Mazda", "model": "3", "engine": "2.0L", "transmission": "automatic",
        "fuel_type": "petrol", "drivetrain": "FWD", "body_type": "Hatchback",
        "year_start": 2014, "year_end": 2018, "generation": "BM",
    }
    base.update(kw)
    return base


def test_cluster_key_deterministic():
    a = clustering.cluster_key(_ident())
    b = clustering.cluster_key(_ident())
    assert a == b
    assert a.count("|") == 7  # 8 fields


def test_cluster_key_differs_on_identity_change():
    base = clustering.cluster_key(_ident())
    changed = clustering.cluster_key(_ident(engine="2.5L"))
    assert base != changed


def test_cluster_id_stable():
    key = clustering.cluster_key(_ident())
    assert clustering.cluster_id(key) == clustering.cluster_id(key)
    assert clustering.cluster_id(key).startswith("CLU-")


def test_build_clusters_groups_same_identity():
    variants = [
        {"validation_id": "VAL-1", "standard_variant": _ident(trim="Base")},
        {"validation_id": "VAL-2", "standard_variant": _ident(trim="Sport")},
        {"validation_id": "VAL-3", "standard_variant": _ident(engine="2.5L")},
    ]
    idx = clustering.build_clusters(variants, ["VAL-1", "VAL-2", "VAL-3"])
    # VAL-1 and VAL-2 share identity (trim is not part of the key)
    assert idx.cluster_for("VAL-1").cluster_id == idx.cluster_for("VAL-2").cluster_id
    assert idx.cluster_for("VAL-1").cluster_id != idx.cluster_for("VAL-3").cluster_id
    assert idx.is_anchor("VAL-1")
    assert not idx.is_anchor("VAL-2")
