import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import numpy as np
import math
from statsmodels.stats.power import FTestAnovaPower


## GENERAL RESULTS ##

# scores per group (frq, mcq, no_questions)
# one value in a list represents the final score for one student in that group
frq_group_scores = [0.6563, 0.7031, 0.8444, 0.4375, 0.6875, 0.7188, 0.75]
mcq_group_scores = [0.75, 0.875, 0.2344, 0.6406, 0.5156, 0.5781]
no_question_group_scores = [0.2813, 0.5, 0.6094, 0.25, 0.9375, 0.9375]

# convert to dataframe for analysis
data_dict = {
    'score': frq_group_scores + mcq_group_scores + no_question_group_scores,
    'group': ['FRQ']*len(frq_group_scores) + ['MCQ']*len(mcq_group_scores) + ['None']*len(no_question_group_scores)
}
df = pd.DataFrame(data_dict)

# basic stats
print("-- Basic Statistics by Group --")
stats_df = df.groupby('group')['score'].agg(['mean', 'std', 'count', 'min', 'max', 'median'])
stats_df.columns = ['Mean', 'Std Dev', 'N', 'Min', 'Max', 'Median']
print(stats_df.to_string())
print("\n")

# One-Way ANOVA
f_stat, p_val_anova = stats.f_oneway(frq_group_scores, mcq_group_scores, no_question_group_scores)
print(f"-- One-Way ANOVA --")
print(f"F-statistic: {f_stat:.4f}")
print(f"p-value: {p_val_anova:.4f}")
print("\n")

# Pairwise T-Tests
def run_ttest(group1, group2, name1, name2):
    t_stat, p_val = stats.ttest_ind(group1, group2, equal_var=False)
    print(f"{name1} vs {name2}: t={t_stat:.4f}, p-value={p_val:.4f}")

print("-- Pairwise T-Test Results (Welch's) --")
run_ttest(frq_group_scores, mcq_group_scores, "FRQ", "MCQ")
run_ttest(frq_group_scores, no_question_group_scores, "FRQ", "None")
run_ttest(mcq_group_scores, no_question_group_scores, "MCQ", "None")
print("\n")

# Tukey HSD (if ANOVA is significant)
if p_val_anova < 0.05:
    print("--Tukey HSD--")
    tukey = pairwise_tukeyhsd(endog=df['score'], groups=df['group'], alpha=0.05)
    print(tukey)
    print("\n")

# Power Analysis

all_groups = [frq_group_scores, mcq_group_scores, no_question_group_scores]
all_scores = frq_group_scores + mcq_group_scores + no_question_group_scores
tot_mean = np.mean(all_scores)
k_groups = len(all_groups)

ssb = 0
ssw = 0

for group in all_groups:
    group_mean = np.mean(group)
    n_group = len(group)
    ssb += n_group * (group_mean - tot_mean)**2
    ssw += np.sum((np.array(group)-group_mean)**2)
sst = ssb+ssw
eta_sq = ssb / sst
coh_f = math.sqrt(eta_sq / (1-eta_sq))
pow_analysis = FTestAnovaPower()
tot_sample_size = pow_analysis.solve_power(effect_size = coh_f, k_groups = k_groups, alpha = 0.05, power = 0.80)
n_per_group = math.ceil (tot_sample_size/k_groups)
print("--Power Analysis--")
print(f"Required N per group: {n_per_group} participants")

# ----

## COMPARISON OF PERFORMANCE ON MCQ AND FRQ QUESTIONS FOR EACH OF THE GROUPS ##


# dict: keys are question numbers for each question type, values are percentage of students who got the question correct
mcq_question_to_correct = {1: 0.7895, 2: 0.368, 3: 0.632, 4: 0.947, 5: 0.526, 6: 0.842, 7: 0.789}
frq_question_to_correct = {1: 0.2105, 2: 0.7544, 3: 0.7807, 4: 0.7456}

# list of tuples: (percentage of correct answers for FRQ, percentage of correct answers for MCQ), for each student
# each tuple represents one student, the first value is their percentage correct on the FRQ section, the second value is their percentage correct on the MCQ section
frq_data = [(0.8571, 0.5), (0.8571, 0.5833), (0.7143, 0.9444), (0.2857, 0.5556), (0.7143, 0.6667), (0.8571, 0.6111), (0.7143, 0.7778)]
mcq_data = [(1, 0.5556), (1, 0.7778), (0.4286, 0.0833), (0.8571, 0.4722), (0.5714, 0.4722), (0.5714, 0.5833)]
no_question_data = [(0.4286, 0.2778), (0.5714, 0.4444), (0.5714, 0.6389), (0.5714, 0), (0.8571, 1), (0.8571, 1)]

def avg_mcq_frq_per_group(data, name):
    frq_avg = sum(x[0] for x in data) / len(data)
    mcq_avg = sum(x[1] for x in data) / len(data)
    return {'Group': name, 'Test-FRQ Avg': frq_avg, 'Test-MCQ Avg': mcq_avg}

results = [
    avg_mcq_frq_per_group(frq_data, "FRQ Group"),
    avg_mcq_frq_per_group(mcq_data, "MCQ Group"),
    avg_mcq_frq_per_group(no_question_data, "None Group")
]

transfer_df = pd.DataFrame(results)
print(transfer_df.to_string(index=False))
print("\n")




# ----

## GENERAL RESULTS ANALYSIS FOR NOTE-TAKERS VS NON NOTE-TAKERS IN MCQ AND FRQ GROUPS ##

# results for people who took notes vs those who did not
# each value in the list represents the final score for one student in that group (who took notes or not)
frq_notes_results = [0.6563, 0.7031, 0.6875, 0.75]
frq_no_notes_results = [0.8444, 0.4375, 0.7188]

# comparison of note-takers vs non note-takers for FRQ section
t_frq, p_frq = stats.ttest_ind(frq_notes_results, frq_no_notes_results, equal_var=False)

mcq_notes_results = [0.75, 0.875, 0.6406, 0.5156]
mcq_no_notes_results = [0.2344, 0.5781]

# comparison of note-takers vs non note-takers for MCQ section
t_mcq, p_mcq = stats.ttest_ind(mcq_notes_results, mcq_no_notes_results, equal_var=False)

print("--- Notes vs No Notes Analysis ---")
print(f"FRQ Group (Notes vs No Notes): t={t_frq:.4f}, p={p_frq:.4f}")
print(f"MCQ Group (Notes vs No Notes): t={t_mcq:.4f}, p={p_mcq:.4f}")
print("\n")


# comparison of FINAL RESULTS of note-takers in FRQ and MCQ groups
t_notes_comp, p_notes_comp = stats.ttest_ind(frq_notes_results, mcq_notes_results, equal_var=False)

print(f"-- Comparison of Total Scores (FRQ Notes vs MCQ Notes) --")
print(f"Mean FRQ+Notes: {sum(frq_notes_results)/len(frq_notes_results):.4f}")
print(f"Mean MCQ+Notes: {sum(mcq_notes_results)/len(mcq_notes_results):.4f}")
print(f"Result: t={t_notes_comp:.4f}, p-value={p_notes_comp:.4f}")
print("\n")


# ----

## ANALYSIS OF PERFORMANCE ON FRQ VS MCQ QUESTIONS FOR NOTE-TAKERS VS NON NOTE-TAKERS ##

### note-takers analysis ###

# list of tuples: (percentage of correct answers for FRQ, percentage of correct answers for MCQ), for each student who took notes vs those who did not
# each tuple represents one student, the first value is their percentage correct on the FRQ section, the second value is their percentage correct on the MCQ section
# list one corresponds to FRQ group who took notes
# list two corresponds to MCQ group who took notes
frq_notes_pairs = [(0.5, 0.8571), (0.5833, 0.8571), (0.6667, 0.7143), (0.7778, 0.7143)]
mcq_notes_pairs = [(0.5556, 1), (0.7778, 1), (0.4722, 0.8571), (0.4722, 0.5714)]


# combine all note-takers answers for FRQ questions and MCQ questions
# list one corresponds to percentage correct on FRQ questions for all note-takers (in both FRQ and MCQ groups)
# list two corresponds to percentage correct on MCQ questions for all note-takers (in both FRQ and MCQ groups)
all_notes_frq = [p[0] for p in frq_notes_pairs + mcq_notes_pairs]
all_notes_mcq = [p[1] for p in frq_notes_pairs + mcq_notes_pairs]

# comparison of FRQ vs MCQ performance for note-takers
t_paired, p_paired = stats.ttest_rel(all_notes_frq, all_notes_mcq)

print(f"--- Format Comparison (Note-takers) ---")
print(f"FRQ Section vs MCQ Section: t={t_paired:.4f}, p={p_paired:.4f}")
print("\n")

### non note-takers analysis ###

# list of tuples: (percentage of correct answers for FRQ, percentage of correct answers for MCQ) for each student who did not take notes
# each tuple represents one student, the first value is their percentage correct on the FRQ section, the second value is their percentage correct on the MCQ section
# list one corresponds to FRQ group who did not take notes
# list two corresponds to MCQ group who did not take notes
frq_no_notes_pairs = [(0.9444, 0.7143), (0.5556, 0.2857), (0.6111, 0.8571)]
mcq_no_notes_pairs = [(0.0833, 0.4286), (0.5833, 0.5714)]

# combine all NON note-takers answers for FRQ questions and MCQ questions
# list one corresponds to percentage correct on FRQ questions for all non note-takers (in both FRQ and MCQ groups)
# list two corresponds to percentage correct on MCQ questions for all non note-takers (in both FRQ and MCQ groups)
all_no_notes_frq = [p[0] for p in frq_no_notes_pairs + mcq_no_notes_pairs]
all_no_notes_mcq = [p[1] for p in frq_no_notes_pairs + mcq_no_notes_pairs]

# comparison of FRQ vs MCQ performance for non note-takers
t_paired_no, p_paired_no = stats.ttest_rel(all_no_notes_frq, all_no_notes_mcq)

print(f"--- Format Comparison (Non Note-takers) ---")
print(f"FRQ Section vs MCQ Section: t={t_paired_no:.4f}, p={p_paired_no:.4f}")
print("\n")
