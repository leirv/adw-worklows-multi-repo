# Designer

Create a new DDR (Design Decision Record) in `ddr/*.md` to resolve the `Task` using the exact specified markdown `Plan Format`. Follow the `Instructions` to create the plan, use the `Relevant Files` to focus on the right files. Follow the `Report` section to properly report the results of your work.

## Instructions

- IMPORTANT: You're writing a DDR to resolve a Task based on the `Task` that will provide the code-level design for the application.
- IMPORTANT: The `Task` describes the Task that will be resolved by this design approach. Remember we're not resolving the Task, we're creating the DDR that will be used to resolve the Task based on the `Plan Format` below.
- You're writing a DDR to design the code structure, class relationships, and method flows. It should be thorough and precise so developers know exactly how to implement it.
- Create the DDR in the `ddr/*.md` file. Name it appropriately based on the `Task`.
- Use the plan format below to create the plan.
- Research the codebase to understand existing patterns, classes, and services before designing new ones.
- IMPORTANT: Replace every <placeholder> in the `Plan Format` with the requested value. Add as much detail as needed to accomplish the Task.
- Use your reasoning model: THINK HARD about class responsibilities, method contracts, and data flow.
- Respect requested files in the `Relevant Files` section.
- Start your research by reading the `README.md` file.
- `adws/*.py` contain astral uv single file python scripts. So if you want to run them use `uv run <script_name>`.
- When you finish creating the DDR for the task, follow the `Report` section to properly report the results of your work.

## Relevant Files

Focus on the following files:
- `README.md` - Contains the project overview and instructions.
- `app/**` - Contains the codebase client/server.
- `scripts/**` - Contains the scripts to start and stop the server + client.
- `adws/**` - Contains the AI Developer Workflow (ADW) scripts.

Ignore all other files in the codebase.

## Plan Format

```md
# Task: <Task name>

## Task Description
<describe the Task in detail>

## Design Overview
<high-level description of the code design approach>

## Class/Service Design

### <ClassName or ServiceName>
- **Responsibility**: <single responsibility of this class>
- **Location**: <file path where this class should live>
- **Dependencies**: <list of classes/services this depends on>

#### Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| <method_name> | <params with types> | <return type> | <what it does> |

### <Another ClassName or ServiceName>
<repeat structure as needed>

## Data Flow
<describe the flow of data through the system using arrow notation>

Example:
- User Request → ControllerA.handleRequest()
  → ServiceB.process(data)
  → RepositoryC.save(entity)
  → Returns Result

<add your actual data flow here>

## Method Contracts

### <ClassName.methodName>
- **Input**: <describe expected input and validation>
- **Output**: <describe expected output>
- **Errors**: <describe error conditions and exceptions thrown>
- **Side Effects**: <describe any side effects (DB writes, events, etc.)>

<repeat for key methods>

## Dependency Injection
<describe how dependencies will be injected/wired>

## Error Handling Strategy
<describe how errors flow through the design>

## Relevant Files
Use these files to implement the design:

<find and list the files that are relevant to the task, describe why they are relevant in bullet points. If there are new files that need to be created to accomplish the task, list them in an h3 'New Files' section.>

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

<list step by step tasks as h3 headers plus bullet points. use as many h3 headers as needed to accomplish the task. Order matters, start with the foundational shared changes required then move on to the specific changes. Your last step should be running the `Validation Commands` to validate the task is complete with zero regressions.>

## Validation Commands
Execute every command to validate the task is complete with zero regressions.

<list commands you'll use to validate with 100% confidence the task is complete with zero regressions. every command must execute without errors so be specific about what you want to run to validate the task is complete with zero regressions. Don't validate with curl commands.>
- `cd app/server && uv run pytest` - Run server tests to validate the task is complete with zero regressions

## Notes
<optionally list any additional notes or context that are relevant to the task that will be helpful to the developer>
```

## Task
$ARGUMENTS

## Report
- Summarize the work you've just done in a concise bullet point list.
- Include a path to the DDR you created in the `ddr/*.md` file.
