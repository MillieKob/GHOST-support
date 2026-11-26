# GHOST-support
Code written to coordinate and run equipment necessary for a GHOST experiment and perform analysis on the acquired data.

## Introduction

GHOST (Generalised Heterodyne Optical Sampling Techniques) is a field-resolved spectroscopy method operating in up to the Petahertz regime encompassing visible and UV parts of the electromagnetic spectrum. It's a family of techniques which use the nonlinear interaction of the test pulse (pulse to be measured) with a sampling pulse (used for heterodyne detection). In this implementation of the GHOST setup we use the second harmonic of the sampling pulse with the sum frequency of the test and sampling as our local oscillator (LO) and heterodyne signal respectively. Hence this is an SFG/SHG GHOST.

## Theory

The field that we want to mesure is called the test field and it can be written as
$$ E_T = A_T(t)e^{i\omega_T t + \phi_T} $$
The field that is used to generate the LO and the signal is called the sampling field and can be written as
$$ E_S = A_S(t)e^{i\omega_S t + \phi_S} $$
Here, $A_S$ and $A_T$ are the field envelopes of the sampling and test pulses specifically, which are equal to the square root of their time-dependent intensity, $\omega_S$ and $\omega_T$ are the carrier frequencies of the waves, and $\phi_S$ and $\phi_T$ are the phases of the sampling and test pulses.
