# EAS 510 - Assignment 1: Digital Forensics Apprentice

A rule-based expert system that matches modified images back to their originals.

This is the **starter repository** for Project 1. Two repositories matter:

| Repository | Role |
|------------|------|
| `delveccj/EAS510_Assignment1_starter` (this repo) | Your **code** lives here. You will fork it, work in your fork, and push your final submission here. |
| `delveccj/EAS510_Assignment1` | The **dataset** (read-only). Clone it for the images; never commit it to your fork. |

## Setup on your Codio box

```bash
# 1. Fork this repo on GitHub, then in your box:
git clone https://github.com/YOUR-USERNAME/EAS510_Assignment1_starter.git
cd EAS510_Assignment1_starter

# 2. Clone the read-only dataset as a sibling folder (images live there):
cd ~/workspace
git clone https://github.com/delveccj/EAS510_Assignment1.git

# 3. Install dependencies:
cd ~/workspace/EAS510_Assignment1_starter
python3 -m pip install -r requirements.txt

# 4. Point this box at YOUR fork (run once):
./setup_git.sh
```

## Repository layout

```
forensics_detective.py   SimpleDetector: register targets + find_best_match
rules.py                 Rule functions (Rule 1: Metadata, Rule 2: Histogram, Rule 3: Template)
test_system.py           Runs the detector over the data folders and writes results_*.txt
scripts/check_output_format.py   Validates a results file against the required format
setup_git.sh, submit.sh  One-time setup + commit/push helper ("backup button")
```

## The task in one paragraph

Implement three interpretable rules (metadata, color histogram, template matching)
that combine into a 0-100 confidence score. Run your system on `modified_images/`
and `random/` and save the full output as `results_v1.txt`. In Phase 2, run on
`hard/`, diagnose a systematic failure, add a **Rule 4**, and save
`results_v1_hard.txt` and `results_v2.txt`. Full instructions are in the Codio guide
and in the assignment PDF in UBLearns.

## Running

```bash
# Phase 1 (easy + random) -> results_v1.txt
python3 test_system.py --modified --random --output results_v1.txt

# Phase 1 on hard cases -> results_v1_hard.txt
python3 test_system.py --hard --output results_v1_hard.txt

# Phase 2 (everything) -> results_v2.txt
python3 test_system.py --modified --hard --random --output results_v2.txt

# Validate any results file against the required format:
python3 scripts/check_output_format.py results_v1.txt
```

The data folders are resolved from a sibling clone of `EAS510_Assignment1`.
If your data is elsewhere, pass `--data-dir /path/to/EAS510_Assignment1`.

## Output format (do not alter)

```
Processing: modified_image_01.jpg
Rule 1 (Metadata): FIRED - Size ratio 0.85 -> 20/30 points
Rule 2 (Histogram): FIRED - Correlation 0.92 -> 25/30 points
Rule 3 (Template): FIRED - Match score 0.76 -> 30/40 points
Final Score: 75/100 -> MATCH to original_03.jpg
```

## Backup doctrine

Your Codio box can be reset at any time. **Your fork on GitHub is the only safe
copy.** After every milestone run `./submit.sh "describe what you did"`. A box
restart never touches GitHub.

## License

Apache 2.0. See `LICENSE`.


## Observed weakness in V1: what failed and why

I changed the metadata trigger and template trigger to 0.55 and 0.20 respectively. As it allowed weaker evidence to contribute points but on the other hand the problem remained the same. They didn't fix the problem of comparing cropped images at different scales. 
In few cases, One of the rule showed strong evidence of the matched image but was discarded cause it wasn't picked up by other rules. The insufficient support from other rules caused it to fail. For example, one of the image had 27 points for match in histogram but was discarded cause the match threshold is 50, while the other metadata and template gave 0.  


## Design decision for V2: what Rule 4 is and why you chose it

Rule 4 addressed multiscale template matching with edge comparision as v1 faced challenges with compression and brightness. I chose multiscale matching because it searches for different sizes within the original. The rule 4 required mutiscale correlation and edge pattern correlation of atleast 0.80 and 0.30, respectively. 

I changed the triggers for the three rules retained from rules.py, namely metadata, histogram and template matching to 15, 30 and 25, respectively and 30 for rule 4. As rule 4 doesnt have the sufficient points to trigger the threshold of 50, it needs evidence from the 3 rules too. 

## Effect of the change: accuracy before/after on easy vs hard

My changed v1 gives the accuracy of 60% while v2 give the accuracy of 83.3% on easy images. On hard images accuracy increased from 55% to 82% approximately. 

## Trade-offs: what new costs or risks did Rule 4 introduce

The trade-off is that the point budget system has changed. The evidence given by first 3 rules have been lowered and now contribute less to matching the images.For example, There could be a case where the metadata gives the evidence and the rule 4 doesn't, but the metadata wont be able to match the threshold alone.

