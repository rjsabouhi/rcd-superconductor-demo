from coherence_math import symbolic_resistance, coherence, synthetic_zero_transit_time
from material_params import materials

def predict_superconductivity(material_name):
    mat = materials[material_name]
    T = mat["T_critical"]
    resistance = symbolic_resistance(T, T, mat["S1"], mat["S2"])
    coh = coherence(mat["H"], mat["M"], mat["R"])
    tau = synthetic_zero_transit_time(coh)

    return {
        "Material": material_name,
        "Resistance at Tc": resistance,
        "Coherence": coh,
        "Synthetic Zero Transit Time": tau
    }

def predict_all():
    results = {}
    for name in materials:
        results[name] = predict_superconductivity(name)
    return results