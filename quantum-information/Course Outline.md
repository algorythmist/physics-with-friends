What we have covered so far, separated into **introductory classical information theory** and then **foundations of quantum theory / quantum information formalism**.

# I. Introductory Classical Information Theory

1. **Entropy as uncertainty** — Shannon entropy measures the average uncertainty or information content of a discrete random variable.
   We treated entropy as the basic quantitative unit of classical information theory.
   This became the reference point for later von Neumann entropy.
2. **Joint, conditional, and marginal entropy** — Entropy becomes richer when several random variables are considered together.
   We reviewed (H(X,Y)), (H(X|Y)), and the chain rule.
   These ideas later reappear as quantum conditional entropy and mutual information.
3. **Mutual information** — Mutual information measures how much knowing one variable tells us about another.
   Classically, it is nonnegative and symmetric.
   It later becomes the model for quantum mutual information (I(A;B)).
4. **Typical sequences and the AEP** — Long i.i.d. sequences concentrate on a typical set of size about (2^{nH(X)}).
   This is the operational bridge from entropy to coding.
   It later becomes the quantum typical subspace formalism.
5. **Classical source coding** — Entropy gives the optimal compression rate for memoryless classical sources.
   We connected the source coding theorem to typical sequences.
   This is the classical predecessor of Schumacher compression.
6. **Classical noisy channels** — A classical channel is described by transition probabilities (p(y|x)).
   We discussed how the channel changes input distributions into output distributions.
   This sets up the comparison with quantum channels as CPTP maps.
7. **Classical channel capacity** — Channel capacity is the maximum reliable communication rate through a noisy channel.
   The key expression is the maximized mutual information (C=\max_{p(x)} I(X;Y)).
   This becomes the template for Holevo information and quantum channel capacities.
8. **Polarization codes / polar codes** — Polar codes use recursive channel combining and splitting to turn many identical noisy binary-input channels into synthetic channels that become either nearly perfect or nearly useless.
    We studied Arıkan’s channel polarization idea, especially for the BEC, including the $W^-$ and $W^+$ transforms, the iteration $(W,W)\mapsto(W^{--},W^{-+},W^{+-},W^{++})$, and the reliability ordering of synthetic channels.

------

# II. Foundations of Quantum Theory / Quantum Information Formalism

1. **Hilbert spaces and state vectors** — Pure quantum states are represented by unit vectors up to global phase.
   We reviewed inner products, orthonormal bases, adjoints, and Dirac notation.
   This was the linear-algebraic starting point for the quantum part of the course.
2. **Observables and the Born rule** — Measurements of observables are governed by spectral decompositions and Born probabilities.
   We connected self-adjoint operators, eigenvalues, projectors, and measurement probabilities.
   This was the first bridge from linear algebra to physical prediction.
3. **Tensor products and composite systems** — Composite quantum systems are described by tensor product Hilbert spaces.
   We emphasized how product states differ from entangled states.
   This topic became essential for partial trace, purification, and channels.
4. **Computational basis and qubit notation** — The computational basis {|0>,|1\>} gives the standard coordinate system for qubits.
   We used bitstring bases for multi-qubit systems.
   This provided a concrete setting for examples and calculations.
5. **Pure and mixed states** — Pure states represent maximal quantum descriptions by state vectors or rank-one projectors, while mixed states represent statistical uncertainty, subsystem states, or loss of access to an environment through density matrices.
    We distinguished a pure state $|\psi\rangle$ from its projector $|\psi\rangle\langle\psi|$, then generalized to mixed states $\rho=\sum_i p_i|\psi_i\rangle\langle\psi_i|$, emphasizing positivity, trace one, expectation values $\operatorname{Tr}(\rho A)$, and the criterion $\rho^2=\rho$ for purity.
   The same mixed state can have many different ensemble decompositions, so a density matrix is the operational state itself, not a unique ignorance mixture over underlying pure states.
6. **Density matrices** — Density operators generalize pure states and describe mixtures, uncertainty, and subsystems.
   We covered positivity, trace one, spectral decomposition, and expectation values.
   Density matrices became the central state formalism for the rest of the course.
7. **Ensemble decompositions and non-uniqueness** — The same density matrix can arise from many different ensembles of pure states.
   We emphasized that a density matrix is not the same thing as a unique classical mixture.
   This distinction later became crucial for purification and HJW.
8. **Partial trace and reduced states** — The partial trace extracts the state of a subsystem from a joint state.
   We derived it using basis formulas, block matrices, and preservation of local expectation values.
   This became one of the main technical tools of the course.
9. **No-signaling and local statistics** — Local measurement statistics depend only on the reduced state.
   We used partial trace identities to show why operations on one subsystem cannot instantaneously change observable statistics on another.
   This gave operational meaning to reduced density operators.
10. **Schmidt decomposition** — Bipartite pure states have a canonical decomposition in terms of correlated orthonormal bases.
    The Schmidt coefficients determine reduced states and pure-state entanglement.
    This became the bridge to purification and entanglement.
11. **Purification** — Every mixed state can be viewed as the reduced state of a larger pure state.
    We constructed purifications using spectral decompositions and vectorization.
    This reframed mixedness as entanglement with an environment.
12. **Uniqueness of purification** — Any two purifications of the same state are related by an isometry on the purifying system.
    This result explains why the purifying system has freedom but the reduced state is fixed.
    It prepared the way for HJW and Stinespring dilation.
13. **HJW theorem and ensemble steering** — Different ensemble decompositions of the same density matrix arise from measurements on a purifying system.
    We treated this as the formal version of quantum steering.
    It tied together purification, measurements, and the non-uniqueness of ensembles.
14. **Projective measurements / PVMs** — Projective measurements are described by mutually orthogonal projectors summing to the identity.
    We covered Born probabilities, selective updates, and Lüders post-measurement states.
    This was the first full measurement model.
15. **Non-selective projective measurements and pinching** — If the measurement outcome is ignored, the state is dephased in the measurement basis.
    We wrote the update as (\rho\mapsto \sum_m P_m\rho P_m).
    This provided a concrete example of a quantum channel.
16. **Degenerate measurements and Lüders update** — Degenerate projective measurements preserve coherence inside each eigenspace while destroying coherence between eigenspaces.
    This clarified the difference between measuring an eigenspace and measuring a complete basis.
    It also showed why state update rules contain physical assumptions.
17. **Noisy projective measurements** — A noisy measurement can be modeled as a sharp projective measurement followed by classical readout noise.
    The effects take the form (E_k=\sum_j q(k|j)P_j).
    This was the transition from PVMs to general POVMs.
18. **POVMs and effects** — A POVM is a collection of positive effects (E_k\ge 0) summing to the identity.
    POVMs describe the most general measurement statistics (p(k)=\operatorname{Tr}(E_k\rho)).
    This separated measurement probabilities from state-update rules.
19. **Naimark dilation** — Every POVM can be realized as a projective measurement on a larger Hilbert space.
    We used ancillas, isometries, and unitary extensions to show how generalized measurements arise physically.
    This connected POVMs back to ordinary projective measurement.
20. **Kraus operators and instruments** — Kraus operators describe both outcome probabilities and post-measurement state updates.
    For outcome (k), an instrument has the form (\mathcal E_k(\rho)=\sum_\alpha K_{k,\alpha}\rho K_{k,\alpha}^\dagger).
    The associated effect is (E_k=\sum_\alpha K_{k,\alpha}^\dagger K_{k,\alpha}).
21. **Selective vs non-selective evolution** — Selective evolution conditions on a measurement outcome, while non-selective evolution sums over outcomes.
    This distinction separated instruments from channels.
    It also clarified when we are describing observed data versus ignored measurement records.
22. **Stinespring dilation** — Every completely positive map can be represented by an isometry into a larger system followed by a partial trace.
    This generalized the Naimark idea from measurements to arbitrary quantum processes.
    It gave a physical model: add ancilla, evolve unitarily/isometrically, discard environment.
23. **CPTP maps / quantum channels** — Quantum channels are completely positive trace-preserving maps on density operators.
    We studied them as the general model of physical evolution, noise, and open-system dynamics.
    Examples included dephasing, depolarizing, and amplitude-damping-type channels.
24. **Complete positivity** — Positivity alone is not enough; a physical map must remain positive when extended by an identity map on any reference system.
    This motivated complete positivity as the correct condition for quantum dynamics.
    It also explained why entanglement forces stronger constraints than classical probability.
25. **Trace preservation and trace-nonincreasing maps** — Channels preserve trace, while individual measurement outcomes are trace-nonincreasing.
    This distinction encoded normalization versus probability of occurrence.
    It helped organize instruments, selective maps, and full CPTP channels.
26. **Choi matrix and Choi–Jamiołkowski representation** — A linear map can be represented by applying it to one half of a maximally entangled operator.
    The Choi matrix makes complete positivity and trace preservation checkable by matrix conditions.
    It became the main algebraic representation of quantum channels.
27. **Kraus–Stinespring–Choi equivalence** — Kraus operators, Stinespring dilations, and Choi matrices are three equivalent views of the same structure.
    Kraus gives the operator-sum form, Stinespring gives the physical dilation, and Choi gives the matrix representation.
    We treated this triad as the organizing framework for generalized quantum processes.
28. **Worked measurement/channel examples** — We used examples such as unsharp qubit measurements, trine POVMs, and amplitude-damping-style channels.
    These examples showed how effects, Kraus operators, instruments, dilations, and Choi matrices are computed concretely.
    They also prepared the course for discrimination, entropy, and quantum Shannon theory.
29. **Transition to quantum Shannon theory** — Having built states, measurements, instruments, channels, and Choi matrices, the next stage is operational information theory.
    The natural next tools are trace distance, fidelity, relative entropy, typical subspaces, Schumacher compression, and channel capacities.
    This is the direction we are now organizing into the 20-lecture quantum Shannon/coding sequence.