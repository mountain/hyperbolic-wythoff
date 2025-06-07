import numpy as np
import itertools as it
import hypw.mirror as mir
import hypw.geometry as geom
import hypw.design as dsn
import hypw.color as clr
import hypw.setting as setting
import PIL as pil  # type: ignore
import argparse

from hypw.typing import Transformation, Order


coord = np.linspace(-1, 1, num=setting.width, dtype=np.complex128)
data = np.array([[x, y] for y in coord for x in coord]).reshape(setting.width, setting.width, 2)


# Ensure dsn is imported as: import hypw.design as dsn
# Ensure geom is imported as: import hypw.geometry as geom
# Ensure clr is imported as: import hypw.color as clr
# Ensure np is imported as: import numpy as np
# Ensure Transformation is available from hypw.typing

# Global 'data' should already be defined:
# coord = np.linspace(-1, 1, num=setting.width, dtype=np.complex128)
# data = np.array([[x, y] for y in coord for x in coord]).reshape(setting.width, setting.width, 2)

def generate_tiling_data(mirror: Transformation, style: str, form_tuple=None, pat_id=None):
    disk = geom.radius(data) < 1
    ps = geom.pdm2hbm(data)  # Poincare disk model to half-plane model

    styled_ts = None
    if style == "checkboard":
        styled_ts = dsn.checkboard(ps, mirror)
    elif style == "edged":
        styled_ts = dsn.edged(ps, mirror) # dsn.edged calls dsn.patterned with specific params
    elif style == "patterned":
        if form_tuple is None or pat_id is None:
            raise ValueError("form_tuple and pat_id must be provided for 'patterned' style.")
        styled_ts = dsn.patterned(ps, mirror, form_tuple, pat_id)
    else:
        raise ValueError(f"Unknown style: {style}")

    # Apply disk and offset, ensuring styled_ts is not None (already handled by ValueError)
    ts = (1 + styled_ts) * disk

    max_val = np.max(ts)
    crd = len(np.unique(ts))

    # Ensure colorbar indexing is robust
    # The design functions return boolean arrays for ts.
    # (1 + styled_ts) makes it 0 or 1 for False/True, then disk makes parts outside 0.
    # So ts elements are likely integers (0, 1, possibly more if styled_ts was not just 0/1).
    # Using .astype(int) is a good safeguard for indexing.
    return crd, clr.colorbar(max_val)[ts.astype(int)][:, :, 0, :]


def filename(order: Order, style: str, form_idx: int = None, pat_id: int = None) -> str:
    p, q, r = order
    a = str(int(p)) if p is not np.inf else 'i'
    b = str(int(q)) if q is not np.inf else 'i'
    c = str(int(r)) if r is not np.inf else 'i'

    base = f"{a}{b}{c}"
    if style == "checkboard":
        return f"{base}-checkboard.png"
    elif style == "edged":
        return f"{base}-edged.png"
    elif style == "patterned":
        if form_idx is None or pat_id is None:
            # This case should ideally not be reached if main_cli calls it correctly
            raise ValueError("form_idx and pat_id are required for patterned style filenames.")
        return f"{base}-patterned-form{form_idx}-pat{pat_id:03d}.png" # Ensure pat_id is zero-padded
    else:
        raise ValueError(f"Unknown style for filename: {style}")


def main_cli():
    import time

    parser = argparse.ArgumentParser(description="Generate hyperbolic tilings.")
    parser.add_argument('--p', type=int, default=2, help='Parameter p for the Schwarz triangle (default: 2)')
    parser.add_argument('--q', type=int, default=3, help='Parameter q for the Schwarz triangle (default: 3)')
    parser.add_argument('--r', type=int, default=7, help='Parameter r for the Schwarz triangle (default: 7)')

    # New arguments
    parser.add_argument(
        '--style',
        type=str,
        choices=["checkboard", "edged", "patterned"],
        default="patterned",
        help="The style of tiling to generate. (default: patterned)"
    )
    parser.add_argument(
        '--form_idx',
        type=int,
        default=None, # Explicitly None if not provided
        help="Index of the form from the predefined list (for 'patterned' style). If specified with --pattern_id, generates a single image."
    )
    parser.add_argument(
        '--pattern_id',
        type=int,
        default=None, # Explicitly None if not provided
        help="Pattern ID (e.g., 0-127) (for 'patterned' style). If specified with --form_idx, generates a single image."
    )

    args = parser.parse_args()

    start = time.time()

    p, q, r = args.p, args.q, args.r
    mirror = mir.init((p, q, r))
    print(mirror)
    # Each tuple in 'forms' likely represents a specific configuration for the tiling pattern.
    # These could be defined as named constants if their specific meanings are known,
    # e.g., FORM_A = (0, 0, 1), FORM_B = (0, 1, 0), etc.
    forms = [(0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)] # Ensure this is defined

    if args.style == "checkboard":
        card, img = generate_tiling_data(mirror, style="checkboard")
        if card > 2: # or some relevant condition
            output_filename = filename((args.p, args.q, args.r), style="checkboard")
            pil.Image.fromarray(img).save(output_filename)
            print(f"Saved: {output_filename}")

    elif args.style == "edged":
        card, img = generate_tiling_data(mirror, style="edged")
        if card > 2: # or some relevant condition
            output_filename = filename((args.p, args.q, args.r), style="edged")
            pil.Image.fromarray(img).save(output_filename)
            print(f"Saved: {output_filename}")

    elif args.style == "patterned":
        if args.form_idx is not None and args.pattern_id is not None:
            if 0 <= args.form_idx < len(forms):
                selected_form_tuple = forms[args.form_idx] # Get the form tuple
                card, img = generate_tiling_data(mirror, style="patterned", form_tuple=selected_form_tuple, pat_id=args.pattern_id)
                if card > 2: # or some relevant condition
                    output_filename = filename((args.p, args.q, args.r), style="patterned", form_idx=args.form_idx, pat_id=args.pattern_id)
                    pil.Image.fromarray(img).save(output_filename)
                    print(f"Saved: {output_filename}")
            else:
                # Error message for out of range form_idx remains as print.
                print(f"ERROR: --form_idx {args.form_idx} is out of range for the predefined forms list (0-{len(forms)-1}).")
        else: # Loop for all forms and patterns
            for i_loop_idx in range(len(forms)):
                current_form_tuple = forms[i_loop_idx]
                for j_loop_idx in range(128): # Iterate through pattern IDs 0-127
                    card, img = generate_tiling_data(mirror, style="patterned", form_tuple=current_form_tuple, pat_id=j_loop_idx)
                    if card > 2: # Use the existing condition for saving
                        output_filename = filename((args.p, args.q, args.r), style="patterned", form_idx=i_loop_idx, pat_id=j_loop_idx)
                        pil.Image.fromarray(img).save(output_filename)
                        # print(f"Saved: {output_filename}") # Optional, could be too verbose in a loop

    print("time:", time.time() - start)

if __name__ == '__main__':
    main_cli()
