---
name: ai-agent-workflows
description: Add AI steps to an automation, such as classifying, summarizing, extracting data, drafting replies, AI agents with tools, or RAG over documents, with cost and safety controls. Use when the user wants ChatGPT, Claude, Gemini or another LLM inside n8n, Activepieces or another workflow tool, or asks to build an AI agent workflow or chatbot.
---

# AI Agent Workflows

AI steps are powerful and the easiest place to waste money or ship wrong answers. Use the smallest AI step that does the job, and check its output before it reaches a customer.

## Step 1: Pick the AI pattern

| Pattern | Use it for | Notes |
|---|---|---|
| Single prompt | Summarize, rewrite, translate, draft a reply | Cheapest and most predictable |
| Classifier | Route tickets, tag leads, detect spam or sentiment | Give a fixed list of labels and a "none" option |
| Extractor | Pull fields from emails, PDFs, invoices | Ask for JSON with a fixed schema |
| Agent with tools | Tasks that need to look things up or take several actions | Slower and pricier; limit the tools and steps |
| RAG | Answer from your own documents | Needs a vector store and a document loader step |

Start with the simplest pattern that works. Most "agent" ideas are really a classifier plus normal steps.

## Step 2: Write the prompt

- Put the role and rules in the system message, the data in the user message.
- Ask for structured output (JSON with named fields) whenever the next step reads it, and use the tool's structured output parser if it has one.
- Include 1 or 2 short examples of good output.
- Say what to do when unsure: return `"unknown"` or ask for review instead of guessing.

## Step 3: Control cost

- Use a small, cheap model for classifying and extracting; save large models for writing or reasoning.
- Trim the input: send only the fields the model needs, not the whole record.
- Cap output length and the number of agent steps.
- Estimate the monthly cost: runs per month × tokens per run × the model's price. Tell the user the number.

## Step 4: Keep humans in the loop

- Anything sent to customers, money moves and deletions need an approval step first (Slack or email with approve and reject).
- Log the prompt, the output and the final decision so mistakes can be traced.
- Never let an AI step write credentials or change permissions.

## Step 5: Test

Run 10 to 20 real examples, including messy ones, before going live. Report how many were right and fix the prompt or labels before raising volume.

## Deliver

The pattern, the model choice with a reason, the full prompt, the output schema, the cost estimate, and where the human check sits in the flow.
