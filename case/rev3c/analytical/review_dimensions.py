"""Named manufacturer reference profiles; no installed-part or mating claim."""

SWITCH_HEIGHT_PROFILES = {
    'c3_td1183_family_a': {
        'module': 'c3', 'height_mm': {'min': 1.4, 'nominal': 1.5, 'max': 1.6},
        'basis': 'DEALON TD1183 family A option; complete fitted suffix unresolved',
        'source_url': 'https://atta.szlcsc.com/upload/public/pdf/source/20220901/234954DA4D26CA925E3AFEBBCE0B4B64.pdf',
        'safe_overtravel_mm': None, 'electrical_make_mm': None,
    },
    'c3_td1183_family_b': {
        'module': 'c3', 'height_mm': {'min': 1.6, 'nominal': 1.7, 'max': 1.8},
        'basis': 'DEALON TD1183 family B option; different height from A',
        'source_url': 'https://atta.szlcsc.com/upload/public/pdf/source/20220901/234954DA4D26CA925E3AFEBBCE0B4B64.pdf',
        'safe_overtravel_mm': None, 'electrical_make_mm': None,
    },
    'c6_jinbeili_ts1001s': {
        'module': 'c6', 'height_mm': {'min': .45, 'nominal': .55, 'max': .65},
        'basis': 'Current module schematic names TS-1001S; PCB retains Alps identity',
        'source_url': 'https://www.jbl-ec.com/uploads/TS-1001S1_1.png',
        'safe_overtravel_mm': None, 'electrical_make_mm': None,
    },
    'c6_alps_sktaaae010': {
        'module': 'c6', 'height_mm': {'min': .43, 'nominal': .53, 'max': .63},
        'basis': 'Older schematic/current PCB identity; actual fitted lot unknown',
        'source_url': 'https://tech.alpsalpine.com/e/products/detail/SKTAAAE010/',
        'safe_overtravel_mm': None, 'electrical_make_mm': None,
    },
}

USB_CANDIDATES = {
    'startech_usb2cc2m': {
        'manufacturer': 'StarTech', 'mpn': 'USB2CC2M',
        'selected': False, 'body_width_max_mm': 12.2,
        'body_height_max_mm': 6.5, 'body_length_max_mm': 22.7,
        'exposed_shank_mm': [6.55, 6.75], 'strain_relief_length_max_mm': 12.4,
        'source_url': 'https://sgcdn.startech.com/005329/media/sets/USB2CC2M/Diagram/USB2CC2M_Diagram.PDF',
        'source_sha256': 'eaa6da83f13039a1b3f5c2747a088e88aa3f16ba403156599f290608e5982f0f',
        'limits': ['Native mating plane, insertion depth and axis remain unverified.',
                   'Overmold corners, metal-shank cross-section and relief cross-section are not dimensioned.',
                   'Cable OD 4.7 mm is nominal only; no cable tolerance or bend limit is assigned.'],
    },
}

def switch_height_profile(module, name, bound='nominal'):
    """Return an explicitly requested conditional height, never a fitted default."""
    profile = SWITCH_HEIGHT_PROFILES[name]
    if profile['module'] != module:
        raise ValueError('Switch profile belongs to a different module')
    if bound not in ('min', 'nominal', 'max'):
        raise ValueError('Choose a published height reference bound')
    return profile['height_mm'][bound]
