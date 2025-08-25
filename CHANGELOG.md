# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-27

### 🚀 Added
- **Categories System**: Organize entries by type (coding, debugging, planning, etc.)
- **Tags Support**: Automatic tag extraction from #hashtags in entries
- **Advanced Search**: Search through entries by text, category, or tags
- **Export Functionality**: Export logs in JSON, CSV, and Markdown formats
- **Configuration File**: Customizable settings via `~/.devlog/config.json`
- **Enhanced Statistics**: Detailed breakdowns by category, tags, and time periods
- **Filtering Options**: Show logs with category, tag, or search filters
- **Performance Improvements**: JSON-based storage instead of Markdown parsing
- **Comprehensive Test Suite**: Full test coverage for all new features

### 🔧 Changed
- **Storage Format**: Migrated from Markdown to JSON for better performance
- **CLI Interface**: Enhanced command structure with new subcommands
- **Data Structure**: Rich metadata for each log entry
- **Error Handling**: Improved error handling and user feedback
- **Code Organization**: Better modular structure and separation of concerns

### 📚 New Commands
- `devlog log "message" --category coding --tags bug frontend`
- `devlog show --limit 10 --category coding --tags bug`
- `devlog search "query" --limit 20`
- `devlog export csv`
- `devlog categories`

### 🎯 Performance Improvements
- **Faster Loading**: JSON parsing is significantly faster than Markdown
- **Efficient Search**: Direct data structure access instead of text parsing
- **Memory Optimization**: Better memory usage for large log files
- **Reduced I/O**: Single file operations instead of multiple reads

### 🧪 Testing
- **Unit Tests**: Comprehensive test suite with 100% coverage
- **Mock Testing**: Proper isolation of file system operations
- **Test Fixtures**: Clean test setup and teardown
- **Edge Cases**: Coverage of error conditions and edge cases

### 📖 Documentation
- **Updated README**: Comprehensive documentation of all new features
- **Configuration Guide**: Template and examples for customization
- **Examples**: Rich examples showing advanced usage patterns
- **API Reference**: Clear documentation of all functions and parameters

## [0.1.0] - 2025-01-20

### 🚀 Added
- Basic logging functionality
- Simple Markdown storage
- Basic statistics tracking
- File opening support
- Cross-platform compatibility

### 📚 Commands
- `devlog log "message"`
- `devlog show`
- `devlog stats`
- `devlog open`

---

## Migration Guide

### From v0.1.0 to v0.2.0

If you have existing logs in the old Markdown format, they will be automatically migrated to the new JSON format on first run. The old `~/.devlog/devlog.md` file will be preserved as a backup.

### Configuration

The new version creates a configuration file at `~/.devlog/config.json`. You can customize:
- Categories for organizing entries
- Tag settings and limits
- Export format preferences
- Date and time formatting

### New Features

1. **Categories**: Organize your work by type
   ```bash
   devlog log "Fixed authentication bug" --category debugging
   ```

2. **Tags**: Use hashtags for easy categorization
   ```bash
   devlog log "Implemented user dashboard #frontend #react #feature"
   ```

3. **Search**: Find specific entries quickly
   ```bash
   devlog search "authentication"
   devlog search "bug" --limit 5
   ```

4. **Export**: Share or backup your logs
   ```bash
   devlog export csv
   devlog export markdown
   ```

5. **Filtering**: View specific subsets of your logs
   ```bash
   devlog show --category coding --tags bug
   devlog show --limit 20
   ```

---

## Future Roadmap

### Planned for v0.3.0
- [ ] Weekly/monthly reports
- [ ] Data visualization (charts and graphs)
- [ ] Backup and sync functionality
- [ ] Plugin system for extensions
- [ ] Web dashboard

### Planned for v0.4.0
- [ ] Team collaboration features
- [ ] Time tracking integration
- [ ] Project management integration
- [ ] API for external tools
- [ ] Mobile app companion

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## Support

If you encounter any issues or have questions:
- Check the [README](README.md) for usage examples
- Review the [Configuration Guide](config_template.json)
- Open an [issue](https://github.com/louiellywton/devlog-cli/issues)
- Join our [discussions](https://github.com/louiellywton/devlog-cli/discussions)
