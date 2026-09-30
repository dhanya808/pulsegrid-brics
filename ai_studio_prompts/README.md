# Google AI Studio Instructions & Prompt Tuning Guide

This folder contains the prompt engineering specifications and edge-case handling instructions tuned for **Gemini 3.8 Flash** in Google AI Studio.

## 🎯 Target Model: `gemini-3.8-flash`
* **Temperature**: `0.2` (Low temperature for authoritative, deterministic logistical calculations)
* **Max Output Tokens**: `1200`
* **Top-P**: `0.95`
* **Top-K**: `40`

---

## 📋 How to Test in Google AI Studio

1. Open [Google AI Studio](https://aistudio.google.com/).
2. Click **Create New Prompt** -> Select **Chat Prompt** or **Freeform Prompt**.
3. In the Model dropdown, select **Gemini 3.8 Flash** (or Gemini 2.5 Flash).
4. In the **System Instructions** box, paste the contents of `system_instructions.json` -> `system_instruction.role` and `core_principles`.
5. Run the evaluation prompts found in `sample_eval_prompts` to observe instantaneous, highly accurate emergency triage briefs with zero hallucinations.

---

## 🛡️ Edge Cases Handled Gracefully
1. **Double-Deficit Trap**: When both clinics in a district are low on inventory, the model refuses to compromise the donor and automatically escalates to the Tier-3 State Depot.
2. **Cold-Chain Biologicals**: Automatically detects temperature-sensitive drugs (Insulin, Rabies, Snake Antivenom) and enforces active refrigerated cryo-van transport (2°C - 8°C).
3. **Data Sovereignty Protection**: Never requires or leaks individualized patient records; computes priority scores strictly from aggregate facility telemetry.
