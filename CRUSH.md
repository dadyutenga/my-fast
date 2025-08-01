# CRUSH.md

## Build, Lint, and Test Commands
- **Build**: `npm run build` - Compiles the project.
- **Lint**: `npm run lint` - Checks code for style and potential errors.
- **Test**: `npm run test` - Runs the full test suite.
- **Single Test**: `npm run test -- -t 'test name'` - Runs a specific test by name.

## Code Style Guidelines
- **Imports**: Group imports by source (standard, third-party, local) with a blank line between groups.
- **Formatting**: Use Prettier with default settings for consistent indentation (2 spaces) and line endings.
- **Types**: Use TypeScript with strict mode enabled; explicitly type all variables and functions.
- **Naming Conventions**: Use camelCase for variables/functions, PascalCase for types/classes, and kebab-case for file names.
- **Error Handling**: Always use try-catch for async operations and log errors with context.
- **Comments**: Only add comments for complex logic; keep them concise and relevant.

## Additional Notes
- Ensure all code passes linting before committing.
- Follow existing patterns in the codebase for consistency.
- No specific Cursor or Copilot rules found in the repository.
