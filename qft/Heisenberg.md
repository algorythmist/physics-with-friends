# The Heisenberg Picture

$
\newcommand{\ket}[1]{\left|{#1}\right\rangle}
\newcommand{\bra}[1]{\left\langle{#1}\right|}
\newcommand{\braket}[2]{\left\langle{#1}\middle|{#2}\right\rangle}
\newcommand{\slash}[1]{#1\!\!\!/}
$

Consider a partial differential equation, such as the heat equation

$$
\partial_t \psi(x,t) = a\partial_x^2 \psi(x,t)
$$

In an elementatary PDE of Physics course, $\psi$ is viewed as a function of two real variables $\psi:\mathbb{R} \times [0, \infty]$. 
The customary solution proceeds with separation of variables.

There is another viewpoint from Functional Analysis, in which $\psi$, as a funcion of $x$, is viewed as a vector in an infinite dimentional vector space of functions. In this scenario, the heat equation is simpley an first order ordinary differential equation in this space:

$$
\frac{d}{dt}\psi_t = aD^2 \psi
$$

Where $D^2$ is a linear operator activing on this space. 

This is in complete analogy to a system of linear ordinary differential equations in finite dimensions:

$$
\frac{d}{dt}x_t = Ax_0
$$

where $x \in \mathbb{R}^n$ and $A$ is an $n \times n$ squera matrix. 

The solution to this system is given by 

$$
x_t = e^{At}x_0
$$

where the matrix exponential was used. An easy way to compute the matrix exponential, if the matrix A is diagonalizable, is via its eigenvalue decomposition, which is also known as a spectum resolution.

Here is a brief overview of the theory: If A is normal (meaning it commutes with its hermitian conjugate), then it has a complete set of eigenvectors $v_i$ and it can be written as 

$$
A = \sum_{i=1}^n \lambda_i v_i v_i^\dagger
$$

The for any analytic function of the matrix $f(x) = \sum_{i=1}^n f(\lambda_i) v_i v_i^\dagger$, so in particularm

$$
x_t = \sum_{i=1}^n e^{\lambda_i t} v_i v_i^\dagger x_0
$$

Let's go back to the problem of solving the heat equation

$$
\frac{d}{dt}\psi_t = aD^2 \psi
$$


For the problem to be fully specified we need to define **initial conditions** and **boundary conditions**. 
As far the initial conditions are concerned, we just need to specify the value of the function at time 0, 
by requiring that $\psi(x,0) = \psi_o(x)$ for some known function $\psi_o(x)$.

The boundary conditons are crucial as they define both the vector space in which these functions live, as well as the properties of the differential operator (in this case $D^2 = d^2/dx^2$

For simplicity we assume the $x \in [0,L]$ with the conditions

$$
\psi(0,t) = 0, \psi(L,t) = 0
$$

Representing a heated bar of length $L$ whose endpoints are kept at constant temperaure. More general boundary conditions on $[0,L]$ can be reduced to this form with some mathematical trickery.

It may not be immediately apparent, but these boundary conditions imply that the space where the solutions live is a Hilbert space with innner product

$$
\braket{\psi}{\phi} = \int_0^L dx\bar{\psi}(x)\phi(x)
$$

We are looking for eignvectors and eigenvalues of the linear operator $D^2$ in this space:

$$
D^2 \psi = -\lambda \psi
$$

A simple differential equation whose general solution is 

$$
\psi(x) = c_1 e^{i\sqrt{\lambda}x} + c_2 e^{-i\sqrt{\lambda}x}
$$

Inserting the boundary conditions, we get $\psi(0,t) = 0 \implies c_2 = -c_1$ 
and $0 = c_1 (e^{i\sqrt{\lambda}L} -_2 e^{-i\sqrt{\lambda}L}) \implies \sin(\sqrt{\lambda}L) = 0$

For the last condition to hold, $\sqrt{\lambda}L$ must be a multiple of $\pi n$ for any integer $n$, therefore we get the quantization condition

$$
\lambda_n = {(\frac{\pi n}{L})}^2  
$$

It also follows from (?), that the general form of the eigenfunctions of $D^2$ are given by 

$$
\psi_n(x) = \sqrt{\frac{2}{L}}\sin(\frac{n\pi x}{L})
$$

where $\sqrt{\frac{2}{L}}$ is a normalization factor.


In parallel with the finite dimensional case, we can write

$$
D^2 = \sum_{n=-\infty}^\infty -\lambda_n \ket{\psi_n}\bra{\psi_n} \implies\\
e^{aD^2 t} = \sum_{n=-\infty}^\infty e^{-{a(\frac{\pi n}{L})}^2 t } \ket{\psi_n}\bra{\psi_n}
$$

Therefore

$$
\ket{\psi_t} = \sum_{n=-\infty}^\infty \braket{\psi_n}{\psi_0} e^{{-a(\frac{\pi n}{L})}^2 t } \ket{\psi_n}
$$

TODO: Maybe solve for psi_0 = T

In the case of the heat equation a is a positive constant $a > 0$. 
If we set $a = \frac{i\hbar}{2m}$ we recover the Schodinger equation. 
The solution to the heated bar problem becomes the solution to the particle in a box.

$$
\ket{\psi_t} = \sum_{n=-\infty}^\infty \braket{\psi_n}{\psi_0} e^{-iE_n t } \ket{\psi_n}
$$

where

$$
E_n = \frac{n^2 \pi^2 \hbar^2}{2m L^2}
$$

whereas $ \frac{i\hbar}{2m} D^2 = p^2/2m$ is the Hamiltotian $H$, 

$$
\ket{\psi_t} = e^{-iHt}\ket{\psi_0}
$$

What does all this have to do with the Heisenberg picture? In my previous article I showed that position and momentum are just rotated versions of each other, related by a unitary tranformation called the Fourier transform.

$$
p = U_F x U^\dagger_F
$$
$$
x = U^\dagger_F p U_F
$$




```python

```
