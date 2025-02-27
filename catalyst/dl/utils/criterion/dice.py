import torch

from catalyst.utils import get_activation_fn


def dice(
    outputs: torch.Tensor,
    targets: torch.Tensor,
    eps: float = 1e-7,
    threshold: float = None,
    activation: str = "Sigmoid"
):
    """
    Computes the dice metric

    Args:
        outputs (list):  A list of predicted elements
        targets (list): A list of elements that are to be predicted
        eps (float): epsilon
        threshold (float): threshold for outputs binarization
        activation (str): An torch.nn activation applied to the outputs.
            Must be one of ["none", "Sigmoid", "Softmax2d"]

    Returns:
        double:  Dice score
    """
    activation_fn = get_activation_fn(activation)
    outputs = activation_fn(outputs)

    if threshold is not None:
        outputs = (outputs > threshold).float()

    intersection = (targets * outputs).mean(dim=2).mean(dim=2)
    union = targets.mean(dim=2).mean(dim=2) + outputs.mean(dim=2).mean(dim=2)
    dice = ((2 * intersection + eps) / (union + eps)).mean()

    return dice


__all__ = ["dice"]
