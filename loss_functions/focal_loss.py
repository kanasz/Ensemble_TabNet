import torch
import torch.nn as nn
import torch.nn.functional as F

num_classes = 2

def focal_loss(input_values, gamma):
    """Computes the focal loss"""
    p = torch.exp(-input_values)
    # loss = (1 - p) ** gamma * input_values
    loss = (1 - p) ** gamma * input_values * 10
    return loss.mean()


class FocalLoss(nn.Module):
    def __init__(self, weight=None, gamma=0.):
        super(FocalLoss, self).__init__()
        assert gamma >= 0
        self.gamma = gamma
        self.weight = weight

    def forward(self, input, target, features=None):
        return focal_loss(F.cross_entropy(input, target, reduction='none', weight=self.weight), self.gamma)