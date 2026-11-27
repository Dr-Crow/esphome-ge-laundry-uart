"""Check the final enclosure solids against the C3 antenna and coax reservations."""
def check_c3_reservations(half_name, half, antenna, coax):
    results = {}
    for name, reservation in (("fpc", antenna), ("coax", coax)):
        intersection = half & reservation
        volume = sum(s.volume for s in intersection.solids()) if intersection is not None else 0.
        clearance = half.distance_to(reservation)
        if volume > 1e-6 or clearance < 1e-5:
            raise ValueError(
                f"C3 {name} touches or intersects the {half_name}: "
                f"{volume:.6g} mm³ intersection, {clearance:.6g} mm clearance"
            )
        results[f"c3_{name}_{half_name}_overlap_mm3"] = round(volume, 6)
        results[f"c3_{name}_{half_name}_clearance_mm"] = round(clearance, 4)
    return results
