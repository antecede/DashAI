#!/usr/bin/env python3
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple, Union
import json
from captum.attr import (
    Deconvolution,
    # DeepLift,
    FeatureAblation,
    GuidedBackprop,
    InputXGradient,
    IntegratedGradients,
    Occlusion,
    Saliency,
    LayerIntegratedGradients,
    LayerFeatureAblation,
    LayerConductance,
    # LayerDeepLift,
    LayerActivation,
    LayerGradCam
)
from captum.attr._utils.approximation_methods import SUPPORTED_METHODS

with open('data/response.json') as f:
    response_json = json.load(f)


class NumberConfig(NamedTuple):
    value: int = 1
    limit: Tuple[Optional[int], Optional[int]] = (None, None)
    type: str = "number"


class StrEnumConfig(NamedTuple):
    value: str
    limit: List[str]
    type: str = "enum"


class StrConfig(NamedTuple):
    value: str
    type: str = "string"

Config = Union[NumberConfig, StrEnumConfig, StrConfig]


SUPPORTED_ATTRIBUTION_METHODS = [
    Deconvolution,
    # DeepLift,
    GuidedBackprop,
    InputXGradient,
    IntegratedGradients,
    Saliency,
    FeatureAblation,
    # Occlusion wasn't able to figure out how to make this work
] if response_json["task"] == "vision" else [
    LayerIntegratedGradients,
    LayerFeatureAblation,
    # LayerConductance,
    # LayerDeepLift,
    # LayerActivation,
    # LayerGradCam
]


class ConfigParameters(NamedTuple):
    params: Dict[str, Config]
    help_info: Optional[str] = None  # TODO fill out help for each method
    post_process: Optional[Dict[str, Callable[[Any], Any]]] = None


ATTRIBUTION_NAMES_TO_METHODS = {
    # mypy bug - treating it as a type instead of a class
    cls.get_name(): cls  # type: ignore
    for cls in SUPPORTED_ATTRIBUTION_METHODS
}


def _str_to_tuple(s):
    if isinstance(s, tuple):
        return s
    return tuple([int(i) for i in s.split()])

def _str_to_bool(s):
    return False if s=="False" else True


ATTRIBUTION_METHOD_CONFIG: Dict[str, ConfigParameters] = {
    IntegratedGradients.get_name(): ConfigParameters(
        params={
            "n_steps": NumberConfig(value=25, limit=(2, None)),
            "method": StrEnumConfig(limit=SUPPORTED_METHODS, value="gausslegendre"),
        },
        post_process={"n_steps": int},
    ),
    FeatureAblation.get_name(): ConfigParameters(
        params={"perturbations_per_eval": NumberConfig(value=1, limit=(1, 100))},
    ),
    Deconvolution.get_name(): ConfigParameters(
        params={}
    ),
    Occlusion.get_name(): ConfigParameters(
        params={
            "sliding_window_shapes": StrConfig(value=""),
            "strides": StrConfig(value=""),
            "perturbations_per_eval": NumberConfig(value=1, limit=(1, 100)),
        },
        post_process={
            "sliding_window_shapes": _str_to_tuple,
            "strides": _str_to_tuple,
            "perturbations_per_eval": int,
        },
    ),
    GuidedBackprop.get_name(): ConfigParameters(
        params={}
    ),
    InputXGradient.get_name(): ConfigParameters(
        params={}
    ),
    Saliency.get_name(): ConfigParameters(
        params={
            "abs": StrEnumConfig(limit= ["True", "False"], value="True")
        },
        post_process={
            "abs": _str_to_bool
        }
    ),
    # Won't work as Relu is being used in multiple places (same layer can't be shared)
    # DeepLift.get_name(): ConfigParameters(
    #     params={}
    # ),
    LayerIntegratedGradients.get_name(): ConfigParameters(
        params={
            "n_steps": NumberConfig(value=25, limit=(2, None)),
            "method": StrEnumConfig(limit=SUPPORTED_METHODS, value="gausslegendre"),
        },
        post_process={"n_steps": int},
    ),
    LayerFeatureAblation.get_name(): ConfigParameters(
        params={
            "perturbations_per_eval": NumberConfig(value=1, limit=(1, 100)) 
        }
    ),
    # LayerGradCam.get_name(): ConfigParameters(
    #     params={}
    # ),
    # Won't work as Relu is being used in multiple places (same layer can't be shared) and some problems with layer
    # LayerDeepLift.get_name(): ConfigParameters(
    #     params={}
    # ),
    # LayerConductance.get_name(): ConfigParameters(
    #     params={
    #         "n_steps": NumberConfig(value=25, limit=(2, None)),
    #         "method": StrEnumConfig(limit=SUPPORTED_METHODS, value="gausslegendre"),
    #     }
    # ),
    # LayerActivation.get_name(): ConfigParameters(
    #     params={}
    # )
}
