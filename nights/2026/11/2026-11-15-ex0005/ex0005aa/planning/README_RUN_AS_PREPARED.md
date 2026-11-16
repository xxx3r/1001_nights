# EX0005Aa · Cell-by-cell Colab guide

**Status: locally prepared; ZERO real API generations performed in EX0005Aa.** Old EX0005A receipts are frozen. This is a public developmental instrument repair, not a new sealed study.

1. Open `EX0005Aa_Colab.ipynb` in Colab. Start at the top; it reconstructs the two Python source files and independent tests without internet file downloads.
2. Run dependency installation and code cells, then local G0 qualification and 11 offline tests. They do not call the model.
3. Review the four **carried-forward** EX0005A predictions. Set `approved_as_prior_for_aa` to `True` only if you approve reusing them as *prior hypotheses*, not newly written predictions.
4. Choose a **new date after November 15, 2026** and a maximum 4-hour separate session window. Freeze once with `run_luna_aa.py --freeze`; the notebook will show the new SHA. Inspect it before any live calls.
5. Make the Colab secret `OPENAI_API_KEY` available. The child runner receives it through an environment bridge; this avoids Colab userdata's `NoneType.kernel` subprocess error. No secret is printed, written, or committed.
6. During the selected future session only, set `RUN_BILLABLE_API = True`, run the live cell **once**, and preserve its receipt files. No automatic network retries. One call may be billed even if incomplete.
7. Inspect the read-only summary and save the receipt ZIP. Do not rewrite, edit or replace original EX0005A results.

The runner **will not run on November 15 after 20:00**. No Colab API key is available inside this ChatGPT container, and no live Luna API call was made during package construction. API model availability in your account is confirmed only when the future run accesses it.
