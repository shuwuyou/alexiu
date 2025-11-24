import json

def load_jsonl(path):
    data = {}
    with open(path, "r") as f:
        for line in f:
            obj = json.loads(line)
            pid = obj.get("player_id")
            data[pid] = obj
    return data


def strip_growth(p):
    """Return a deep copy of player p without growth_potential_score."""
    p2 = json.loads(json.dumps(p))  # deep copy
    try:
        if "growth_potential_score" in p2.get("basic_info", {}):
            del p2["basic_info"]["growth_potential_score"]
    except:
        pass
    return p2


def compare_files(file1, file2):
    data1 = load_jsonl(file1)
    data2 = load_jsonl(file2)

    ids1 = set(data1.keys())
    ids2 = set(data2.keys())

    missing_in_2 = ids1 - ids2
    missing_in_1 = ids2 - ids1

    if missing_in_2:
        print("❌ Players missing in second file:", missing_in_2)
    if missing_in_1:
        print("❌ Players missing in first file:", missing_in_1)

    # Compare players common to both
    mismatches = []

    for pid in sorted(ids1 & ids2):
        p1 = data1[pid]
        p2 = strip_growth(data2[pid])

        if p1 != p2:
            mismatches.append(pid)

    if not mismatches and not missing_in_1 and not missing_in_2:
        print("✅ PERFECT MATCH — the ONLY difference is growth_potential_score.")
    else:
        print("❌ Differences found.")
        print("Players with mismatches:", mismatches)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Compare JSONL files with growth potential.")
    parser.add_argument("--file1", required=True, help="Original JSONL file")
    parser.add_argument("--file2", required=True, help="Modified JSONL file (with growth score)")
    args = parser.parse_args()

    compare_files(args.file1, args.file2)
