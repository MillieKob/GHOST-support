# GHOST-support
Code written to coordinate and run equipment necessary for a GHOST experiment and perform analysis on the acquired data.

## Introduction

GHOST (Generalised Heterodyne Optical Sampling Techniques) is a field-resolved spectroscopy method operating in up to the Petahertz regime encompassing visible and UV parts of the electromagnetic spectrum. It's a family of techniques which use the nonlinear interaction of the test pulse (pulse to be measured) with a cross-polarised sampling pulse (used for heterodyne detection). In this implementation of the GHOST setup we use the second harmonic of the sampling pulse with the sum frequency of the test and sampling as our local oscillator (LO) and heterodyne signal (HS) respectively. These are generated in a z-cut BBO crytsal, hence this is an SFG/SHG GHOST.

## Theory

The field that we want to mesure is called the test field and it can be written as: \
'''math
E_T = A_T(t)e^{i(\omega_T t + \phi_T)}
'''
The field that is used to generate the LO and the signal is called the sampling field and can be written as: \
$$ E_S = A_S(t)e^{i(\omega_S (t+\tau) + \phi_S)} $$
Here, $A_S$ and $A_T$ are the field envelopes of the sampling and test pulses specifically, which are equal to the square root of their time-dependent intensity, $\omega_S$ and $\omega_T$ are the carrier frequencies of the waves, and $\phi_S$ and $\phi_T$ are the phases of the sampling and test pulses. Here, $\tau$ is the delay between the test and sampling pulses.\
The LO is the result of second harmonic generation of the sampling pulse, and so we can write its electric field as follows:\
$$ E_{LO} = A_S^2(t)e^{i(2\omega_S (t+\tau) + 2\phi_S)} $$
Likewise the HS is generated through sum-frequency generation between the test and sampling pulses and thus can be written as:\
$$ E_{HS} = A_S(t)A_T(t)e^{i(\omega_S (t+\tau) + \omega_T(t) + \phi_T + \phi_S)}
If the frequency of the test and sampling pulse match, then we can detect an interference signal by measuring the intensity with a photodetector. By writing $\omega_S=\omega_T=\omega$ we find:\
$$ I_{HS+LO} = I_{HS} + I_{LO} + 2A_S^3A_T\cos(\omega\tau+\phi_T-\phi_S) $$ 
If the test and sampling pulses originate from the same laser, then in a given shot $\phi_T=\phi_s$ and hence this method of detection works even without carrier-envelope phase (CEP) stable pulses as the phase term cancels out.