# Contributing to MyPodify

Thank you for your interest in contributing to MyPodify! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment. We expect all contributors to:
- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/your-username/mypodify.git
cd mypodify
```
3. Set up your development environment:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

4. Create a new branch for your feature/fix:
```bash
git checkout -b feature/your-feature-name
```

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Use meaningful variable and function names
- Include docstrings for classes and functions
- Keep functions focused and modular

### Directory Structure
- Place new AI helper functions in `ai_helper/`
- Add utility functions to `utils/`
- Update documentation when adding new features

### Documentation

- Update README.md if adding new features or changing functionality
- Include docstrings for new functions and classes
- Comment complex logic or non-obvious implementations
- Update requirements.txt if adding new dependencies

## Making Changes

1. Make your changes in your feature branch
2. Write or update tests as needed
3. Run the test suite to ensure everything passes
4. Update documentation as necessary
5. Commit your changes with clear, descriptive commit messages:
```bash
git commit -m "feat: add support for MP3 file processing"
```

### Commit Message Guidelines

Follow the conventional commits specification:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

## Submitting Changes

1. Push your changes to your fork:
```bash
git push origin feature/your-feature-name
```

2. Create a Pull Request:
   - Go to the original repository
   - Click "New Pull Request"
   - Choose your fork and feature branch
   - Fill out the PR template

### Pull Request Guidelines

- Provide a clear description of the changes
- Link any related issues
- Include screenshots for UI changes
- List any breaking changes
- Update documentation as needed
- Ensure CI checks pass
- Request review from maintainers

## Additional Resources

### Setting Up Local Development

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Configure your environment variables:
```env
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=your_endpoint
AZURE_DOCUMENT_INTELLIGENCE_KEY=your_key
AZURE_SPEECH_KEY=your_speech_key
AZURE_SPEECH_REGION=your_region
OPENAI_API_KEY=your_openai_key
```

### Testing Files

Place test documents in the `my_docs/` directory for testing your changes.

## Questions or Need Help?

- Create an issue for bugs or feature requests
- Join our community discussions
- Contact the maintainers

## License

By contributing to MyPodify, you agree that your contributions will be licensed under the same license as the project.