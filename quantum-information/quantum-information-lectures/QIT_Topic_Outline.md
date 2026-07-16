# III. Quantum Information Theory Topic Outline

### Text reference key:

**W** = Watrous, *The Theory of Quantum Information*; **Wi** = Wilde, *Quantum Information Theory*; **KLW** = Khatri–Lami–Wilde, *Principles of Quantum Communication Theory*; **MM** = Manenti–Motta, *Quantum Information Science*; **J** = Jacobs, *Quantum Measurement Theory and its Applications*.

### Scope: 

**Watrous, Wilde, and KLW** will be the main spine for this module. 

**Manenti–Motta** is useful mainly for background on density operators, quantum maps, decoherence, and entanglement, not for mature channel-capacity proofs. 

**Jacobs** is useful for the measurement/discrimination/information-gain side, but it is not primarily a quantum Shannon coding text. 

------

***Watrous*** covers SDP, distance/discrimination, entropy/source coding, entanglement, and channel capacities; 
Best “spine” for *distance measures → entropy → capacities* with a very theorem-forward style.

***Wilde*** has a full quantum Shannon sequence from distances and entropy through typicality, Schumacher compression, classical/EA/private/quantum communication; 
Best for *quantum Shannon coding proofs and intuition* (typicality, coding constructions, capacity zoo)

***KLW*** has a modern one-shot-to-asymptotic communication emphasis with SDP, hypothesis testing, distinguishability, entropy, entanglement measures, and communication protocols. 
Good for a modern perspective and for tying entropic quantities tightly to communication tasks (also helpful when you want a more “communication theory” style)

***Manenti–Motta***’s relevant coverage is mostly density operators, quantum maps, decoherence, and entanglement; Jacobs’s relevant coverage is quantum measurement theory, information theory concepts, distinguishing quantum states, fidelity of operations, and continuous measurement. 
A good complementary narrative track for students who benefit from “physics-to-QIT” continuity, especially around channels/noise and entanglement themes.

***Jacobs / Busch–Lahti–Pellonpää–Ylinen***: Selectively use as enrichment when we touch measurement optimality, discrimination, and operational meaning (especially around the SDP/decision-theory angles).

------



# Talks

## 1) Operational distance for states: trace distance and Helstrom discrimination

**One-line summary:** Binary state discrimination motivates trace distance as the operational measure of how distinguishable two quantum states are.

**Longer description:** Start from the decision problem: Nature prepares either ρ or σ with known prior probabilities, and the receiver chooses a POVM to guess which state was prepared. Derive the Helstrom measurement and the optimal success/error probability in terms of the trace norm. This lecture should make trace distance feel unavoidable: it is not just a norm, but the exact bias advantage in optimal binary discrimination. It also reinforces the role of POVMs as optimization variables.

**References:**
W: Ch. 3.1, especially 3.1.1.
Wi: Ch. 9.1; also Ch. 10.9 for classical information from quantum systems.
KLW: Ch. 5.3.1, 5.3.2; Ch. 6.1.
MM: Ch. 6, density operators, and Ch. 7, quantum maps, as background.
J: Ch. 2.4, distinguishing quantum states; Ch. 1.7, measurements on ensembles.

------

## 2) Fidelity, purified distance, and gentle measurement

**One-line summary:** Fidelity gives a second notion of closeness that behaves well under purifications, channels, and approximate measurements.

**Longer description:** After trace distance, introduce fidelity as the “overlap-like” measure that remains meaningful for mixed states. Prove or state Uhlmann’s theorem, the Fuchs–van de Graaf inequalities, and monotonicity under channels. Then introduce the gentle measurement principle: a high-probability measurement outcome disturbs the state only slightly. This lecture is important because gentle measurement arguments appear repeatedly in coding proofs.

**References:**
W: Ch. 3.2.
Wi: Ch. 9.2–9.4.
KLW: Ch. 6.2; Appendix 6.B.
MM: Ch. 6–7 as background on mixed states and maps.
J: Ch. 2.3, quantum measurements and information; Ch. 2.5, fidelity of quantum operations.

------

## 3) Many-copy discrimination and the hypothesis-testing viewpoint

**One-line summary:** Asymptotic hypothesis testing connects distinguishability to entropy, error exponents, and later coding converses.

**Longer description:** Move from one-copy discrimination to n-copy discrimination: ρ versus σ becomes ρ⊗n versus σ⊗n. Introduce symmetric and asymmetric hypothesis testing, Type I/Type II errors, and the idea that relative entropy appears as an optimal error exponent. This is the clean conceptual bridge from distance measures to entropy, because relative entropy becomes the operational rate at which false positives/false negatives can be suppressed. Keep the full proof optional, but make the theorem statements and operational meaning clear.

**References:**
W: Ch. 3.1 for discrimination; Ch. 5.2.3 for relative entropy background.
Wi: Ch. 11.8–11.9; Ch. 12 for recoverability/entropy inequalities as advanced context.
KLW: Ch. 5.3.3; Ch. 7.9–7.10.
MM: Ch. 6–7 for state/map formalism.
J: Ch. 2.4; Ch. 3.8.1 for a measurement-oriented example of distinguishing two states.

------

## 4) Channels as distinguishable objects: diamond norm and channel discrimination

**One-line summary:** The diamond norm is the operational distance governing optimal discrimination of quantum channels, including ancilla-assisted strategies.

**Longer description:** Generalize state discrimination to channel discrimination: an unknown black box implements either 𝒩 or ℳ, and the experimenter may choose an input state, possibly entangled with a reference. Explain why ordinary induced norms are insufficient and why the completely bounded trace norm/diamond norm appears. This lecture should emphasize the Choi picture from the previous module and show how ancillas can improve discrimination. It is also the right point to prepare students for SDP formulations of channel distances.

**References:**
W: Ch. 3.3.
Wi: Ch. 9.5; also Ch. 4 for channel formalism.
KLW: Ch. 5.4; Ch. 6.3; Appendix 6.A.
MM: Ch. 7, quantum maps.
J: Ch. 2.5 for fidelity of quantum operations; Ch. 3.8.1 for discrimination context.

------

## 5) Semidefinite programming for quantum information

**One-line summary:** SDP is introduced as the computational and duality framework behind optimal measurements, trace norms, diamond norms, and later entanglement bounds.

**Longer description:** Give a self-contained SDP lecture: primal and dual form, conic feasibility, weak duality, strong duality under Slater-type conditions, and complementary slackness. Then immediately translate familiar QIT quantities into SDPs: minimum-error discrimination, trace norm, diamond norm, and simple feasibility tests for positive semidefinite constraints. This should be taught as a working mathematical tool rather than as abstract convex optimization. End with one small numerical exercise, ideally using CVXPY.

**References:**
W: Ch. 1.2.3; Ch. 3.3.4.
Wi: Use Ch. 9 as motivation, but Wilde is not the main SDP source.
KLW: Ch. 2.4; Appendix 6.A; Appendix 6.B; later Ch. 9.3.1 and Appendix 9.A.
MM: No major SDP treatment; use only for background examples.
J: No major SDP treatment; use measurement examples as motivation.

------

## 6) Quantum entropy: von Neumann entropy, conditional entropy, and mutual information

**One-line summary:** Von Neumann entropy and its derived quantities become the basic accounting system for compression, correlations, and information flow.

**Longer description:** Define S(ρ), S(A), S(A|B), I(A;B), and I(A;B|C). Emphasize similarities and differences from classical entropy: conditional entropy can be negative, mutual information is still nonnegative, and purification identities radically simplify many calculations. This lecture should be computational: many small examples with pure bipartite states, classical–quantum states, product states, and maximally entangled states. It prepares students for compression and capacity formulas.

**References:**
W: Ch. 5.1–5.2.
Wi: Ch. 10–11, especially 11.1–11.7.
KLW: Ch. 7.2.1–7.2.3.
MM: Ch. 6, density operators; Ch. 9 for entanglement background.
J: Ch. 2.1–2.2.

------

## 7) Quantum relative entropy, data processing, and recoverability intuition

**One-line summary:** Quantum relative entropy is the master divergence, and data processing becomes the main engine for converses and impossibility theorems.

**Longer description:** Define D(ρ‖σ), discuss support conditions, and prove or carefully state monotonicity under CPTP maps. Present data processing as the statement that physical processing cannot make states more distinguishable. Then explain why this is the mathematical heart of many converse theorems: every coding task is compared with an ideal task or a useless channel. If time permits, introduce the Petz recovery map as the equality-case/reversibility intuition.

**References:**
W: Ch. 5.2.3.
Wi: Ch. 11.8–11.9; Ch. 12.
KLW: Ch. 7.2–7.3; Ch. 7.11 for channel information measures.
MM: Ch. 6–7 as background.
J: Ch. 2.1–2.3 for entropy/information motivation.

------

## 8) Typical subspaces and the quantum AEP

**One-line summary:** Typical subspaces are the quantum analogue of typical sequences and enable asymptotic coding proofs.

**Longer description:** Since students already know classical Shannon theory, begin by recalling the AEP and then translate it into spectral/projector language. Define the typical projector for ρ⊗n and prove the three key estimates: high probability, dimension about 2ⁿS(ρ), and near-flatness of ρ⊗n on the typical subspace. This lecture should be proof-oriented because these estimates are the engine behind Schumacher compression and HSW achievability. It also helps students see why quantum coding proofs look like “operator-valued typicality.”

**References:**
W: Ch. 5.3.2; Ch. 7 for permutation/symmetric-subspace background if desired.
Wi: Ch. 14–15.
KLW: Ch. 2.5; Ch. 7.10; later Ch. 12 and 14 for asymptotic uses.
MM: No direct typical-subspace coding treatment; use Ch. 6 background.
J: Ch. 4.2 has physical typicality themes, but not as a coding-theorem spine.

------

## 9) Schumacher compression

**One-line summary:** An i.i.d. quantum source with density operator ρ can be compressed to approximately S(ρ) qubits per signal.

**Longer description:** Present the quantum source coding task: encode n outputs of a memoryless quantum source into a smaller Hilbert space and decode with high fidelity. Use the typical subspace to prove achievability and then explain the converse: compressing below S(ρ) loses information. This is the quantum analogue of Shannon source coding, but with a crucial twist: the goal is to preserve coherent quantum states, not just classical labels. It is the first full coding theorem in the sequence.

**References:**
W: Ch. 5.3.2.
Wi: Ch. 18.
KLW: Ch. 7 for entropy tools; Ch. 14 for related quantum communication ideas.
MM: Ch. 6–7 background.
J: Appendix H.1 mentions the Schumacher–Westmoreland–Wootters theorem; use only as a side reference.

------

## 10) Classical information in quantum ensembles: Holevo information and accessible information

**One-line summary:** Holevo information quantifies how much classical information can be encoded into and recovered from quantum states.

**Longer description:** Introduce classical–quantum states ρ_XB = ∑_x p(x)|x⟩⟨x| ⊗ ρ_B^x and define χ = I(X;B). Contrast χ with accessible information, which requires optimizing over measurements. Prove or state the Holevo bound: no measurement can extract more classical mutual information than χ. This lecture links the measurement formalism, entropy, and classical communication through quantum systems.

**References:**
W: Ch. 5.3.3; Ch. 8.1.
Wi: Ch. 10.9; Ch. 13.3; Ch. 20.
KLW: Ch. 3.2.8; Ch. 7.11; Ch. 12.
MM: Ch. 6–7 background.
J: Ch. 2.3; Ch. 2.4.

------

## 11) HSW theorem: classical capacity of a quantum channel with product-state coding

**One-line summary:** The Holevo–Schumacher–Westmoreland theorem gives the basic achievable rate for transmitting classical information through a noisy quantum channel.

**Longer description:** Define classical communication over a quantum channel: codewords are input states, the channel acts independently, and Bob performs a collective measurement. State the HSW theorem and carefully explain the regularization issue: unlike the classical channel capacity formula, quantum channel classical capacity generally involves possible nonadditivity. Present the achievability proof at a structured level using random coding, typical projectors, and the packing lemma. The converse should be connected back to Holevo information and data processing.

**References:**
W: Ch. 8.1.1–8.1.2.
Wi: Ch. 16; Ch. 20.
KLW: Ch. 12.
MM: No direct HSW proof; Ch. 7 as quantum channel background.
J: Appendix H.1 as an auxiliary measurement-theory reference.

------

## 12) SDP reappearance I: optimal measurements, accessible information bounds, and multi-hypothesis discrimination

**One-line summary:** Minimum-error state discrimination and related measurement optimizations show how SDP dual variables become operational certificates.

**Longer description:** Revisit the SDP lecture in a concrete setting: optimize over POVM elements {E_k} to discriminate an ensemble {p_k,ρ_k}. Derive the primal SDP and dual SDP, then interpret dual feasible operators as upper bounds on success probability. Work through examples such as two-state discrimination, trine states, or symmetric ensembles. This is also a natural place to discuss why accessible information is hard: the measurement optimization is convex for fixed ensemble, but information objectives can be subtler than linear success probability.

**References:**
W: Ch. 3.1.2; Ch. 1.2.3.
Wi: Ch. 9.1; Ch. 10.9.
KLW: Ch. 2.4; Ch. 5.3.2; Ch. 6.1.
MM: Ch. 6–7 background.
J: Ch. 2.3–2.4.

------

## 13) Entanglement as a resource: Schmidt structure, LOCC, and entanglement entropy

**One-line summary:** Entanglement becomes the first major resource theory in which entropy has direct operational meaning.

**Longer description:** Introduce entanglement not just as “nonclassical correlation” but as a resource that can be transformed, consumed, distilled, and used to simulate communication tasks. Review the Schmidt decomposition, entropy of entanglement for pure states, LOCC, teleportation, and dense coding. The key message is that pure-state bipartite entanglement has a clean entropy theory, while mixed-state entanglement is harder and less reversible. This prepares the ground for entanglement-assisted capacities and quantum capacity.

**References:**
W: Ch. 6.1–6.3.
Wi: Ch. 3.6, 3.8; Ch. 6; Ch. 19.
KLW: Ch. 3.2.3; Ch. 5.1–5.2; Ch. 9.
MM: Ch. 9.
J: Not central; only measurement/information background.

------

## 14) Mixed-state entanglement, PPT criterion, and entanglement measures

**One-line summary:** Mixed-state entanglement introduces separability, PPT tests, witnesses, and multiple inequivalent entanglement measures.

**Longer description:** Define separable and entangled mixed states, then introduce positive partial transpose as a computable necessary condition for separability and, in low dimensions, a complete criterion. Explain entanglement witnesses and why mixed-state entanglement theory is not as simple as pure-state theory. Then give a survey of measures: relative entropy of entanglement, distillable entanglement, entanglement cost, negativity, and Rains-type quantities. The goal is not to prove everything, but to give students enough structure to understand later capacity upper bounds.

**References:**
W: Ch. 6.1; Ch. 6.2.3.
Wi: Ch. 19.2.
KLW: Ch. 3.2.9; Ch. 9.
MM: Ch. 9.
J: Not central.

------

## 15) SDP reappearance II: PPT relaxations, entanglement witnesses, and computable bounds

**One-line summary:** SDP methods give practical tests and relaxations for entanglement and for capacity upper bounds.

**Longer description:** Use the PPT constraint as the main example of a semidefinite constraint in entanglement theory. Show how to formulate PPT membership, entanglement witness searches, and negativity as SDPs or SDP-adjacent convex programs. Then connect this to the broader coding story: many difficult capacities are bounded by relaxations based on PPT-preserving, Rains, or related computable quantities. This lecture makes SDP feel like a real research tool rather than a one-off technique.

**References:**
W: Ch. 1.2.3; Ch. 6.1–6.2.3.
Wi: Ch. 19.2; Ch. 24.9 as context for distillation.
KLW: Ch. 3.2.9; Ch. 4.6.3; Ch. 9.2.1; Ch. 9.3.1; Appendix 9.A.
MM: Ch. 9.
J: Not central.

------

## 16) Entanglement-assisted classical communication and capacity

**One-line summary:** Shared entanglement turns the classical capacity problem into a clean single-letter formula governed by quantum mutual information.

**Longer description:** Begin with superdense coding as the noiseless example, then move to entanglement-assisted communication over noisy channels. State the entanglement-assisted classical capacity theorem: the capacity is the maximum quantum mutual information I(A;B) over channel inputs. Emphasize why this theorem is cleaner than the unassisted HSW capacity: entanglement assistance restores additivity. This lecture is a major payoff for the entropy formalism.

**References:**
W: Ch. 8.1.3.
Wi: Ch. 6.2; Ch. 21.
KLW: Ch. 11.
MM: Ch. 9 for entanglement background.
J: Not central.

------

## 17) Quantum capacity: coherent information and the LSD theorem

**One-line summary:** Quantum capacity is governed by coherent information, but unlike entanglement-assisted capacity it generally requires regularization.

**Longer description:** Define the task of quantum communication: preserving unknown quantum states or entanglement through many uses of a noisy channel. Introduce coherent information I(A⟩B) = −S(A|B) and explain why negative conditional entropy is now a feature, not a bug. State the Lloyd–Shor–Devetak theorem and explain the achievability idea via decoupling or entanglement transmission. The converse should be framed around data processing and the no-cloning/no-broadcasting intuition.

**References:**
W: Ch. 8.2.1–8.2.2.
Wi: Ch. 11.5; Ch. 13.5; Ch. 24.
KLW: Ch. 14.
MM: Ch. 7–8 background on maps and decoherence.
J: Not central.

------

## 18) Degradable channels, anti-degradable channels, and worked capacity examples

**One-line summary:** Special channel classes show when capacity formulas simplify and when quantum communication is impossible.

**Longer description:** Define complementary channels, degradable channels, and anti-degradable channels. Explain why degradability often makes coherent information additive, while anti-degradability implies zero quantum capacity by a no-cloning argument. Work through examples such as erasure channels, dephasing/Pauli channels, and amplitude damping where appropriate. This lecture is essential because it turns abstract capacity formulas into calculable examples.

**References:**
W: Ch. 8.2; Ch. 8.3 for nonadditivity context.
Wi: Ch. 24.7.
KLW: Ch. 4.3.2; Ch. 4.5; Ch. 14.3.1–14.3.2.
MM: Ch. 7–8 background.
J: Not central.

------

## 19) Private classical communication and wiretap-style quantum channels

**One-line summary:** Private communication asks how much classical information can be sent to Bob while remaining hidden from an environment or eavesdropper.

**Longer description:** Introduce the private classical communication task using the channel’s complementary output as Eve’s system. Define private information as a difference between Bob’s and Eve’s Holevo informations and explain why regularization again appears. Relate private capacity to quantum capacity, secret key distillation, and decoupling ideas. This lecture can be mostly conceptual unless you want to prove a simplified private coding theorem.

**References:**
W: Not a primary source here; use Ch. 8 as background on capacities.
Wi: Ch. 13.2 and 13.6; Ch. 23.
KLW: Ch. 15; Ch. 16.
MM: No direct private-capacity treatment.
J: Not central, except for measurement/information context.

------

## 20) Capstone: resource inequalities and computable SDP bounds for communication tasks

**One-line summary:** The final lecture unifies classical, quantum, private, and entanglement-assisted communication as resource transformations with computable converse bounds.

**Longer description:** Organize the whole module into a resource table: noiseless classical bits, qubits, shared entanglement, private bits, and noisy channel uses. Show how different capacity theorems are different conversion rates among these resources. Then return to SDP and convex relaxations: diamond norm bounds, PPT-assisted bounds, Rains-type bounds, and numerical upper bounds on communication performance. This is the “mature-level” synthesis lecture: students should leave seeing quantum Shannon theory as a network of operational tasks, entropy formulas, and optimization problems.

**References:**
W: Ch. 8; Ch. 1.2.3; Ch. 6 for entanglement background.
Wi: Ch. 25–26; also Ch. 20–24.
KLW: Ch. 17–20 for assisted communication and secret-key settings; Ch. 19 for LOCC/PPT-assisted quantum communication.
MM: Ch. 9 for entanglement background.
J: Ch. 2–3 only as a measurement/information supplement.

------

This ordering moves from **operational distinguishability** → **entropy and data processing** → **source coding** → **classical channel coding** → **entanglement resources** → **entanglement-assisted, quantum, and private capacities**, with SDP appearing as a recurring computational and duality tool rather than an isolated technique.