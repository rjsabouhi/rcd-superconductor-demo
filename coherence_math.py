import math

def clinging_parameter(T, T_critical):
    # Θ(T): clinging approaches zero as T approaches critical temperature
    return max(1e-6, 1 - T / T_critical)

def entropy_gradient(S1, S2):
    # ∇S: symbolic entropy gradient between two symbolic states
    return abs(S2 - S1)

def memory_tension(H, M, R):
    # μ(H, M, R): symbolic memory strain from history (H), memory (M), and resonance (R)
    return abs(H - M) + abs(M - R)

def symbolic_resistance(T, T_critical, S1, S2):
    theta = clinging_parameter(T, T_critical)
    entropy_grad = entropy_gradient(S1, S2)
    return theta * entropy_grad

def coherence(H, M, R):
    # γ(t): coherence measure between history, memory, and resonance
    return 1 / (1 + memory_tension(H, M, R))

def synthetic_zero_transit_time(coherence_value):
    # τ: as coherence → 1, transit time → 0
    return 1 / (coherence_value + 1e-6)