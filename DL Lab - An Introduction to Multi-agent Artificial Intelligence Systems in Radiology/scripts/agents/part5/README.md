# Part 5: Networking Agent - Agentic Architecture Schema

## Overview

The Networking Agent is a sophisticated multi-agent system that creates comprehensive networking profiles for radiologists. It demonstrates hierarchical multi-agent architectures combining both **sequential** and **parallel** agent workflows.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER INPUT                                        │
│                    "Create a networking profile for [Name]"              │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    ROOT AGENT (SequentialAgent)                          │
│                    networking_agent                                     │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             │ Sequential Flow
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              STEP 1: Verification Agent (LlmAgent)                      │
│              radiologist_verification_agent                              │
│                                                                           │
│  Tools: [google_search]                                                   │
│                                                                           │
│  Input:  Person's name                                                    │
│  Output: Background information, verification status, professional details│
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             │ Sequential Flow
                             │ (Output passed to next agent)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│         STEP 2: Parallel Research Agent (ParallelAgent)                  │
│         parallel_research_agent                                         │
│                                                                           │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐     │
│  │  URL Finder Agent            │  │  Article Agent              │     │
│  │  (LlmAgent)                  │  │  (LlmAgent)                 │     │
│  │                              │  │                              │     │
│  │  Tools: [google_search]      │  │  Tools: [get_semantic_      │     │
│  │                              │  │         scholar_papers]     │     │
│  │  Input: Person name +        │  │  Input: Person name +        │     │
│  │         background info      │  │         background info      │     │
│  │                              │  │                              │     │
│  │  Output: List of URLs        │  │  Output: Most recent &      │     │
│  │          (social media,      │  │          most cited papers   │     │
│  │           personal pages,    │  │          with metadata       │     │
│  │           institutional)     │  │                              │     │
│  └──────────────────────────────┘  └──────────────────────────────┘     │
│           │                                    │                          │
│           └──────────────┬─────────────────────┘                          │
│                          │ Parallel Execution                            │
│                          │ (Both agents run simultaneously)               │
│                          ▼                                                │
│              Combined Results: URLs + Publications                       │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             │ Sequential Flow
                             │ (Combined results passed to formatter)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              STEP 3: Formatter Agent (LlmAgent)                          │
│              profile_formatter_agent                                     │
│                                                                           │
│  Tools: [] (No tools - structured output only)                            │
│                                                                           │
│  Input:  All previous agent outputs:                                     │
│          - Background information (from verification_agent)                │
│          - URLs (from url_finder_agent)                                   │
│          - Publications (from article_agent)                              │
│                                                                           │
│  Output: NetworkingProfile (Pydantic model)                               │
│          - person_name: str                                               │
│          - background: str                                                │
│          - online_presence: List[URLInfo]                                 │
│          - recent_publications: PublicationSection                         │
│            - most_recent_papers: List[Paper]                             │
│            - most_cited_papers: List[Paper]                               │
│          - contact_information: Optional[str]                             │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         STRUCTURED OUTPUT                                 │
│                    (NetworkingProfile Pydantic Model)                    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Agent Flow Details

### Sequential Components

The root agent uses a **SequentialAgent** that executes three main steps in order:

1. **Verification Agent** →
2. **Parallel Research Agent** →
3. **Formatter Agent**

Each step receives the output from the previous step as input.

### Parallel Components

Within the SequentialAgent, Step 2 contains a **ParallelAgent** that runs two agents simultaneously:

- **URL Finder Agent** and **Article Agent** execute in parallel
- Both receive the same input (person name + background from verification agent)
- Their results are combined before being passed to the formatter agent

## Agent Specifications

### 1. Verification Agent (`radiologist_verification_agent`)

- **Type**: `LlmAgent`
- **Model**: `gemini-2.5-flash`
- **Tools**: `[google_search]`
- **Input**: Person's name (from user)
- **Output**: Background information, verification status, professional details
- **Purpose**: Verify if person is a radiologist and gather background information

### 2. Parallel Research Agent (`parallel_research_agent`)

- **Type**: `ParallelAgent`
- **Sub-agents**:
  - `url_finder_agent`
  - `article_agent`
- **Input**: Person name + background (from verification_agent)
- **Output**: Combined results from both sub-agents
- **Purpose**: Run URL finding and article search simultaneously

#### 2a. URL Finder Agent (`url_finder_agent`)

- **Type**: `LlmAgent`
- **Model**: `gemini-2.5-flash`
- **Tools**: `[google_search]`
- **Input**: Person name + background (from verification_agent)
- **Output**: List of URLs (social media, personal pages, institutional)
- **Purpose**: Find publicly available web pages about the person

#### 2b. Article Agent (`semantic_scholar_agent`)

- **Type**: `LlmAgent`
- **Model**: `gemini-2.5-flash`
- **Tools**: `[get_semantic_scholar_papers]` (custom function tool)
- **Input**: Person name + background (from verification_agent)
- **Output**: Most recent papers (up to 10) and most cited papers (up to 10)
- **Purpose**: Find research articles from Semantic Scholar database

### 3. Formatter Agent (`profile_formatter_agent`)

- **Type**: `LlmAgent`
- **Model**: `gemini-2.5-flash`
- **Tools**: `[]` (No tools)
- **Output Schema**: `NetworkingProfile` (Pydantic model)
- **Input**: All previous agent outputs combined
- **Output**: Structured `NetworkingProfile` object
- **Purpose**: Compile all information into a structured networking profile

## Data Flow

```
User Input
    │
    ├─→ verification_agent
    │       │
    │       ├─→ Uses google_search tool
    │       │
    │       └─→ Output: Background info
    │               │
    │               ├─→ url_finder_agent (parallel)
    │               │       │
    │               │       ├─→ Uses google_search tool
    │               │       │
    │               │       └─→ Output: URLs
    │               │
    │               └─→ article_agent (parallel)
    │                       │
    │                       ├─→ Uses get_semantic_scholar_papers tool
    │                       │
    │                       └─→ Output: Publications
    │                               │
    │                               └─→ Combined Results
    │                                       │
    │                                       └─→ formatter_agent
    │                                               │
    │                                               └─→ Output: NetworkingProfile (structured)
```

## Key Architectural Patterns

### 1. Sequential Workflow

The root agent uses `SequentialAgent` to ensure:

- Verification happens first (needed for subsequent steps)
- Research happens after verification (uses background info)
- Formatting happens last (needs all research results)

### 2. Parallel Execution

The `ParallelAgent` enables:

- **Efficiency**: URL finding and article search run simultaneously
- **Independence**: Both tasks don't depend on each other
- **Speed**: Reduces total execution time

### 3. Structured Output

The formatter agent uses Pydantic models for:

- **Type Safety**: Ensures output structure is validated
- **Programmatic Access**: Easy to parse and process
- **Consistency**: Guaranteed output format

## Tool Usage

| Agent              | Tool Type       | Tool Name                     | Purpose                           |
| ------------------ | --------------- | ----------------------------- | --------------------------------- |
| Verification Agent | Native ADK      | `google_search`               | Search for background information |
| URL Finder Agent   | Native ADK      | `google_search`               | Find publicly available URLs      |
| Article Agent      | Custom Function | `get_semantic_scholar_papers` | Query Semantic Scholar API        |
| Formatter Agent    | None            | -                             | Returns structured Pydantic model |

## Output Structure

The final output is a `NetworkingProfile` Pydantic model with:

```python
class NetworkingProfile(BaseModel):
    person_name: str
    background: str
    online_presence: List[URLInfo]
    recent_publications: PublicationSection
        - most_recent_papers: List[Paper]
        - most_cited_papers: List[Paper]
    contact_information: Optional[str]
```

This structured output can be:

- Parsed programmatically by custom runners
- Converted to markdown files
- Used in downstream applications
- Validated for type safety

## Execution Flow Summary

1. **Sequential Step 1**: Verification Agent runs first
2. **Sequential Step 2**: Parallel Research Agent runs (contains parallel execution)
   - URL Finder Agent and Article Agent run simultaneously
   - Results are combined
3. **Sequential Step 3**: Formatter Agent compiles everything into structured output

## Benefits of This Architecture

- **Modularity**: Each agent has a single, focused responsibility
- **Efficiency**: Parallel execution reduces total time
- **Scalability**: Easy to add more agents or modify existing ones
- **Maintainability**: Clear separation of concerns
- **Type Safety**: Structured output ensures consistency
