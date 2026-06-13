"""Identity-fingerprint clustering for cost control.

Rows that share the same normalized identity fingerprint are grouped so that
Gemini grounding can be performed once per cluster and the evidence reused
across the member rows. Every original ``validation_id`` still produces one
output row.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Dict, List

from .normalization import extract_identity, norm_key, norm_year

# Years are bucketed so that close model years share a cluster.
YEAR_BUCKET_SIZE = 3


def year_bucket(identity: Dict[str, Any]) -> str:
    """Prefer an explicit generation; otherwise bucket the start year."""
    gen = norm_key(identity.get("generation"))
    if gen:
        return gen
    ys = norm_year(identity.get("year_start"))
    if ys is None:
        return "unknown_year"
    base = (ys // YEAR_BUCKET_SIZE) * YEAR_BUCKET_SIZE
    return f"{base}_{base + YEAR_BUCKET_SIZE - 1}"


def cluster_key(identity: Dict[str, Any]) -> str:
    """Deterministic cluster key string.

    Format:
        {make}|{model}|{year_bucket}|{engine}|{fuel_type}|{transmission}|{drivetrain}|{body_type}
    """
    parts = [
        norm_key(identity.get("make")),
        norm_key(identity.get("model")),
        year_bucket(identity),
        norm_key(identity.get("engine")),
        norm_key(identity.get("fuel_type")),
        norm_key(identity.get("transmission")),
        norm_key(identity.get("drivetrain")),
        norm_key(identity.get("body_type")),
    ]
    return "|".join(parts)


def cluster_id(key: str) -> str:
    """Stable short id for a cluster key."""
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]
    return f"CLU-{digest}"


@dataclass
class Cluster:
    cluster_id: str
    cluster_key: str
    member_ids: List[str] = field(default_factory=list)
    # The first member that gets grounded; its evidence is reused by the rest.
    anchor_id: str = ""


def build_clusters(
    variants: List[Dict[str, Any]],
    ordered_ids: List[str],
) -> "ClusterIndex":
    """Group variants by identity fingerprint, preserving input order."""
    by_id = {v.get("validation_id"): v for v in variants}
    clusters: Dict[str, Cluster] = {}
    id_to_cluster: Dict[str, str] = {}

    for vid in ordered_ids:
        variant = by_id.get(vid)
        if variant is None:
            continue
        identity = extract_identity(variant)
        key = cluster_key(identity)
        cid = cluster_id(key)
        cluster = clusters.get(cid)
        if cluster is None:
            cluster = Cluster(cluster_id=cid, cluster_key=key, anchor_id=vid)
            clusters[cid] = cluster
        cluster.member_ids.append(vid)
        id_to_cluster[vid] = cid

    return ClusterIndex(clusters=clusters, id_to_cluster=id_to_cluster)


@dataclass
class ClusterIndex:
    clusters: Dict[str, Cluster]
    id_to_cluster: Dict[str, str]

    @property
    def cluster_count(self) -> int:
        return len(self.clusters)

    def cluster_for(self, validation_id: str) -> Cluster:
        return self.clusters[self.id_to_cluster[validation_id]]

    def is_anchor(self, validation_id: str) -> bool:
        cluster = self.cluster_for(validation_id)
        return cluster.anchor_id == validation_id
