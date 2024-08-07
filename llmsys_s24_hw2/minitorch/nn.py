from typing import Tuple
import numba
from . import operators
from .autodiff import Context
from .fast_ops import FastOps
from .cuda_ops import CudaOps
from .tensor import Tensor
from .tensor_functions import Function, rand, tensor, tensor_from_numpy
import numpy as np
import math

def tile(input: Tensor, kernel: Tuple[int, int]) -> Tuple[Tensor, int, int]:
    """
    Reshape an image tensor for 2D pooling

    Args:
        input: batch x channel x height x width
        kernel: height x width of pooling

    Returns:
        Tensor of size batch x channel x new_height x new_width x (kernel_height * kernel_width) as well as the new_height and new_width value.
    """

    batch, channel, height, width = input.shape
    kh, kw = kernel
    assert height % kh == 0
    assert width % kw == 0
    # ASSIGN4.3
    new_width = width // kw
    new_height = height // kh

    x = input.contiguous().view(batch, channel, new_height, kh, new_width, kw)
    x = x.permute(0, 1, 2, 4, 3, 5).contiguous()
    x = x.view(batch, channel, new_height, new_width, kh * kw)
    return x, new_height, new_width
    # END ASSIGN4.3


def avgpool2d(input: Tensor, kernel: Tuple[int, int]) -> Tensor:
    """
    Tiled average pooling 2D

    Args:
        input : batch x channel x height x width
        kernel : height x width of pooling

    Returns:
        Pooled tensor
    """
    batch, channel, height, width = input.shape
    # ASSIGN4.3
    x, new_height, new_width = tile(input, kernel)
    return x.mean(dim=4).view(batch, channel, new_height, new_width)
    # END ASSIGN4.3

if numba.cuda.is_available():
    # max_reduce = CudaOps.reduce(operators.max, -1e9)
    from minitorch.cuda_kernel_ops import CudaKernelOps
    max_reduce = CudaKernelOps.reduce(operators.max, -1e9)
else:
    max_reduce = FastOps.reduce(operators.max, -1e9)


def argmax(input: Tensor, dim: int) -> Tensor:
    """
    Compute the argmax as a 1-hot tensor.

    Args:
        input : input tensor
        dim : dimension to apply argmax


    Returns:
        :class:`Tensor` : tensor with 1 on highest cell in dim, 0 otherwise

    """
    out = max_reduce(input, dim)
    return out == input


class Max(Function):
    @staticmethod
    def forward(ctx: Context, input: Tensor, dim: Tensor) -> Tensor:
        "Forward of max should be max reduction"
        # ASSIGN4.4
        out = max_reduce(input, int(dim.item()))
        ctx.save_for_backward(input, out)
        return out
        # END ASSIGN4.4

    @staticmethod
    def backward(ctx: Context, grad_output: Tensor) -> Tuple[Tensor, float]:
        "Backward of max should be argmax (see above)"
        # ASSIGN4.4
        input, out = ctx.saved_values
        return (out == input) * grad_output, 0.0
        # END ASSIGN4.4

        
def max(input: Tensor, dim: int) -> Tensor:
    return Max.apply(input, input._ensure_tensor(dim))


def softmax(input: Tensor, dim: int) -> Tensor:
    r"""
    Compute the softmax as a tensor.



    $z_i = \frac{e^{x_i}}{\sum_i e^{x_i}}$

    Args:
        input : input tensor
        dim : dimension to apply softmax

    Returns:
        softmax tensor
    """
    # ASSIGN4.4
    e = (input - Max.apply(input, tensor([dim]))).exp()
    partition = e.sum(dim=dim)
    return e / partition
    # END ASSIGN4.4


def logsoftmax(input: Tensor, dim: int) -> Tensor:
    r"""
    Compute the log of the softmax as a tensor.

    $z_i = x_i - \log \sum_i e^{x_i}$

    See https://en.wikipedia.org/wiki/LogSumExp#log-sum-exp_trick_for_log-domain_calculations

    Args:
        input : input tensor
        dim : dimension to apply log-softmax

    Returns:
         log of softmax tensor
    """
    # ASSIGN4.4
    e = input
    mx = Max.apply(e, tensor([dim]))
    lse = (e - mx).exp().sum(dim=dim).log() + mx
    return e - lse
    # END ASSIGN4.4


def maxpool2d(input: Tensor, kernel: Tuple[int, int]) -> Tensor:
    """
    Tiled max pooling 2D

    Args:
        input: batch x channel x height x width
        kernel: height x width of pooling

    Returns:
        Tensor : pooled tensor
    """
    batch, channel, height, width = input.shape
    # ASSIGN4.4
    x, new_height, new_width = tile(input, kernel)
    return max(x, 4).view(batch, channel, new_height, new_width)
    # END ASSIGN4.4


def dropout(input: Tensor, rate: float, ignore: bool = False) -> Tensor:
    """
    Dropout positions based on random noise.

    Args:
        input : input tensor
        rate : probability [0, 1) of dropping out each position
        ignore : skip dropout, i.e. do nothing at all

    Returns:
        tensor with random positions dropped out
    """
    # ASSIGN4.4
    if ignore:
        return input
    r = rand(input.shape, backend=input.backend)
    drop = rate < r
    return input * drop
    # END ASSIGN4.4


def layer_norm(input: Tensor, eps: float = 1e-5) -> Tensor:
    # ASSIGN4.4
    
    # Calculate mean and variance along the last axis (features)
    batch, channel, height, width = input.shape
    
    mean = input.mean(dim=4).view(batch, channel, height, width)
    variance = input.var(dim=4).view(batch, channel, height, width)
    
    input_normalized = (input - mean) / (variance + eps)
    return input_normalized

    # END ASSIGN4.4


###############################################################################
# Assignment 2 Problem 2
###############################################################################

def GELU(input: Tensor) -> Tensor: 
    """Applies the GELU activation function with 'tanh' approximation element-wise
    https://pytorch.org/docs/stable/generated/torch.nn.GELU.html
    """
    ### BEGIN YOUR SOLUTION
    return 0.5 * input * (1.0 + (math.sqrt(2.0 / math.pi) * (input + 0.044715 * input**3)).tanh())
    # raise NotImplementedError
    ### END YOUR SOLUTION


def logsumexp(input: Tensor, dim: int) -> Tensor:
    """Calculates logsumexp with logsumexp trick for numerical stability
    https://en.wikipedia.org/wiki/LogSumExp

    Args:
        input : The tensor to calculate logsumexp over
        dim : The dimension to reduce over

    Returns:
        out : The output tensor with the same number of dimensions as input (equiv. to keepdims=True)
            NOTE: minitorch functions/tensor functions typically keep dimensions if you provide a dimensions.
    """  
    ### BEGIN YOUR SOLUTION
    return (input.exp().sum(dim)).log()
    # raise NotImplementedError
    ### END YOUR SOLUTION


def one_hot(input: Tensor, num_classes: int) -> Tensor:
    """Takes a Tensor containing indices of shape (*) and returns a tensor of shape (*, num_classes) 
    that contains zeros except a 1 where the index of last dimension matches the corresponding value of the input tensor.
    This is analogous to torch.nn.functional.one_hot (which contains helpful examples you may want to play around with)

    Hint: You may want to use a combination of np.eye, tensor_from_numpy, 
    """
    ### BEGIN YOUR SOLUTION
    raise NotImplementedError
    ### END YOUR SOLUTION


def softmax_loss(logits: Tensor, target: Tensor) -> Tensor:
    """Softmax + Cross Entropy Loss function with 'reduction=None'.
    Formula is provided in writeup.

    Args: 
        logits : (minibatch, C) Tensor of raw logits       
        target : (minibatch, ) Tensor of true labels 

    Returns: 
        loss : (minibatch, )
    """
    result = None
    ### BEGIN YOUR SOLUTION
    raise NotImplementedError
    ### END YOUR SOLUTION
    return result.view(batch_size, )