# Deep Learning Lab: An Introduction to Multi-agent Artificial Intelligence Systems in Radiology

- Moderator: Pouria Rouzrokh MD MPH MHPE
- Speaker: Moein Shariatnia MD
- Speaker: Melina Hosseiny MD

## Overview

In this hands-on workshop, we will explore the concept of multi-agent AI frameworks, emphasizing their importance and unique advantages over single, monolithic models. Attendees will learn how the collaboration of multiple specialized agents can outperform a single powerful model by leveraging task-specific expertise and diverse perspectives. The workshop will provide practical guidance on deploying LLM and VLM agents and connecting them to each other using the Google Agent Development Kit.

## What's Included

This repository contains educational materials and code examples for building multi-agent AI systems using Google's Agent Development Kit (ADK). The main educational resource is the Jupyter notebook located in `./Introduction_to_Multi_Agent_AI_Systems.ipynb`, which provides:

- Introduction to basic agents (LLM-only)
- Augmenting agents with tools (Google Search, native tools)
- Understanding ADK limitations and multi-agent solutions
- Multi-agent pipelines (Sequential, Parallel, Loop)
- Advanced tools integration (MCP servers)
- Custom runners and session management
- Practical examples with radiology applications

## Next Steps: Advanced Multi-Agent System

After reviewing this notebook, we highly recommend exploring our more sophisticated multi-agent AI pipeline implementation:

- **Project Website**: [www.rsna2025-agenticai.com](https://www.rsna2025-agenticai.com)
- **GitHub Repository**: [https://github.com/PouriaRouzrokh/RSNA2025_DLL_AgenticAI](https://github.com/PouriaRouzrokh/RSNA2025_DLL_AgenticAI)

This repository demonstrates a complete production-ready multi-agent system for radiology reporting, featuring:

- A full-stack application with Next.js frontend and FastAPI backend
- Integrated CT scan viewer with NIfTI file support
- Voice transcription and AI-powered report generation workflow
- Complex multi-agent architecture with specialized agents (Orchestrator, Researcher, Synthesizer, Formatter)
- Sub-agents for EHR data, prior reports, and guidelines
- Real-world radiology workstation interface

This advanced example showcases how the concepts learned in this workshop can be applied to build sophisticated, production-ready multi-agent systems in healthcare.
