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
- I was able to get V1 (not hard) to be close to 100% accurate with my update to the template rule which by far ended up being the strongest rule. The only 2 images I missed were modified_09_crop_25pct and modified_00_crop_25pct.
- Main reason Why I failed on those 2 images: Histogram rule failed because the patch had enough of a different color distribution than the original. It makes sense why the metadata rule would have trouble because a crop changes the data(just a bad matchup for the metadata rule), and the Template rule fired correctly for both these images. 
- v1_hard results gives another story. This version had the resize augment as the main as the problem child with the crop augment also giving some trouble. The majority of where resize was used, I failed the image. Only in some crop combinations I failed the rule but crop was certainty a consistent factor.
- for v1_hard I missed 13 images out of a total 60 giving 78% accuracy. Of those cases 11 of them contained resize augments, so I only got 9 of the total number of resize images(20 total) correct. Of those 13 failed images, 6 of them were V3 images, 5 were V6, and 2 from V2. 
- Main reason why I failed on most resize images: Resize changes the size of the image features. Rule 3 searches for positions in the image, but resize distorts that, making this fail. The main issue came from weighing this rule as much as it was. The other 2 rules needed almost max points to cover if a rule 3 was failing. 
## Design decision for V2: what Rule 4 is and why you chose it
- I decided to go with multi-scale template matching for rule 4 as I was getting absolutely thrashed by resize augments and this seemed like the most direct action that I could take against resize. 
- My rule 4 looks at every input image at several sizes in an attempt to allow the resize features to line up with those in the original image before running a template match test. I do not recomend this take for a solution, it made the runtime absolutely explode because its running many checks over and over at different scales. 
## Effect of the change: accuracy before/after on easy vs hard
- from results_v2: easy modified images 59/60 correct. Hard images 43/60 correct(71% accuracy) and I got all of the random/unrelated images correct. Overall 117/135 images correct for 86% accuracy. 
- However, the accuracy for hard images with resize decreased from 9/20 to 6/20 with the addition of rule 4, meaning the reduction in points that R4 takes from metadata and histogram rules was actually detrimental for the overall accuracy as a system. Aka rule 4 doesn't bring enough new information for it to be worth using. 
- Of the hard images (all the versions have 10 total images), I got all of v1 correct. V2 had 2 misses. V3 had 8 misses. V4 had 1 miss. V5 was all correct. V6 had 6 misses. So essentially the addition of rule 4 magnified the underlying tendencies and issues of the system instead of being a brace against them like intended. 
- Also something to note, I only have an overall accuracy increase because easy images and more random images were incorporated to the testing pool with the hard images. Making Non hard images the majority of the testing images.
## Trade-offs: what new costs or risks did Rule 4 introduce
- Tradeoffs for rule 4 are mostly negative seeing that my rule 4 caused a slight decrease in the system's accuracy.
- Runtime: because I set up rule 4 as of brute force it very much increases the runtime of the system, as it essentially resizes 1 image multiple times to check it over and over.
- Risk : Trying more scales can make further false positives with other unrelated images. I don't have any way to prove this but I can't see how that possibility wouldn't be a risk of this approach. 
- Lastly and most importantly, the trade off of taking points away from histogram and metadata tests to give rule 4 a say was not a net positive trade off as it saw the overall system take a decrease in accuracy with hard images with only a 1 image improvement from easy images. 
- Conclusion, my rule 4 kind of worked but backfired. 