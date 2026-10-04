#!/usr/bin/env python3
"""Rewards a marker protein enriched toward IP, penalizes it more heavily if enriched toward WCL."""

import argparse
import csv
import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "organelle_marker_lists.json"


def main():
    parser = argparse.ArgumentParser(description="Per-protein organelle marker specificity score")
    parser.add_argument("--differential_expression_file", required=True)
    parser.add_argument("--organelle_list", required=True)
    parser.add_argument("--reward", type=float, default=1.0)
    parser.add_argument("--penalty", type=float, default=2.0)
    parser.add_argument("--output_folder", required=True)
    args = parser.parse_args()

    output_folder = Path(args.output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    # @step: Loading organelle marker list
    with open(DATA_FILE) as f:
        marker_lists = json.load(f)
    if args.organelle_list not in marker_lists:
        raise SystemExit(f"Unknown organelle_list {args.organelle_list!r}; available: {sorted(marker_lists)}")
    member_genes = set(marker_lists[args.organelle_list]["genes"])

    # @step: Loading fold-change scores
    rows = []
    with open(args.differential_expression_file) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["gene"] not in member_genes:
                continue
            fold_change = float(row["log2_fold_change"])
            if fold_change >= 0:
                value = args.reward * abs(fold_change)
            else:
                value = -args.penalty * abs(fold_change)
            rows.append({
                "protein": row["protein"],
                "gene": row["gene"],
                "organelle_specificity": value,
                "fold_change": fold_change,
            })

    # @step: Writing organelle specificity scores
    with open(output_folder / "organelle_specificity.tsv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["protein", "gene", "organelle_specificity", "fold_change"], delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} organelle specificity scores against {args.organelle_list!r} ({len(member_genes)} markers)", file=sys.stderr)
    print("Organelle specificity scoring complete.", file=sys.stderr)


if __name__ == "__main__":
    main()
