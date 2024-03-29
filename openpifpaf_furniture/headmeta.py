"""Head meta objects contain meta information about head networks.

This includes the name, the name of the individual fields, the composition, etc.
"""

from dataclasses import dataclass, field
from typing import Any, ClassVar, List, Tuple
import openpifpaf
import numpy as np


@dataclass
class CifFurniture(openpifpaf.headmeta.Base):
    """Head meta data for a Composite Intensity Field (CIF)."""

    keypoints: List[str]
    sigmas: List[float]
    pose: Any = None
    draw_skeleton: List[Tuple[int, int]] = None
    score_weights: List[float] = None

    n_confidences: ClassVar[int] = 1
####################  Composite fields extension due to furniture classification  ###################
    n_class: ClassVar[int] = 4
#####################################################################################################

    n_vectors: ClassVar[int] = 1
    n_scales: ClassVar[int] = 1

    vector_offsets = [True]
    decoder_min_scale = 0.0
    decoder_seed_mask: List[int] = None

    training_weights: List[float] = None

    @property
    def n_fields(self):
        return len(self.keypoints)


@dataclass
class CafFurniture(openpifpaf.headmeta.Base):
    """Head meta data for a Composite Association Field (CAF)."""

    keypoints: List[str]
    sigmas: List[float]
    skeleton: List[Tuple[int, int]]
    pose: Any = None
    sparse_skeleton: List[Tuple[int, int]] = None
    dense_to_sparse_radius: float = 2.0
    only_in_field_of_view: bool = False
    
    n_confidences: ClassVar[int] = 1
####################  Composite fields extension due to furniture classification  ###################
    n_class: ClassVar[int] = 4
#####################################################################################################

    n_vectors: ClassVar[int] = 2
    n_scales: ClassVar[int] = 2

    vector_offsets = [True, True]
    decoder_min_distance = 0.0
    decoder_max_distance = float('inf')
    decoder_confidence_scales: List[float] = None

    training_weights: List[float] = None

    @property
    def n_fields(self):
        return len(self.skeleton)

    @staticmethod
    def concatenate(metas):
        # TODO: by keypoint name, update skeleton indices if meta.keypoints
        # is not the same for all metas.
        concatenated = CafFurniture(
            name='_'.join(m.name for m in metas),
            dataset=metas[0].dataset,
            keypoints=metas[0].keypoints,
            sigmas=metas[0].sigmas,
            pose=metas[0].pose,
            skeleton=[s for meta in metas for s in meta.skeleton],
            sparse_skeleton=metas[0].sparse_skeleton,
            only_in_field_of_view=metas[0].only_in_field_of_view,
            decoder_confidence_scales=[
                s
                for meta in metas
                for s in (meta.decoder_confidence_scales
                          if meta.decoder_confidence_scales
                          else [1.0 for _ in meta.skeleton])
            ]
        )
        concatenated.head_index = metas[0].head_index
        concatenated.base_stride = metas[0].base_stride
        concatenated.upsample_stride = metas[0].upsample_stride
        return concatenated

