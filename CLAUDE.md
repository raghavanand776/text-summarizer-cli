# Project Context

Project 1 from my Agentic AI build plan: a command-line text summarizer that calls the Claude API directly. I use Claude Code as a pair programmer and review every change.

## Conventions
- Explain reasoning before making changes.
- Keep changes small and reviewable: one function or one file at a time.
- Don't install new packages without asking first.

## Milestones
- **v1:** accept text input, make one Claude API call, print the summary.
- **v2:** add guardrails: max input length, error handling around the API call, cost estimate before the call, and actual token usage after it.

## Purpose
Learn the Messages API shape end to end, before moving on to tool use and agent loops.
