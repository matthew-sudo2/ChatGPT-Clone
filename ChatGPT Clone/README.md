# ChatGPT Clone

A responsive ChatGPT clone built with vanilla HTML, CSS, and JavaScript. Features a modern dark theme interface that closely mimics the official ChatGPT interface.

## 🚀 Features

- **Authentic ChatGPT Interface**: Dark sidebar, clean chat area, and modern design
- **Real AI Responses**: Powered by OpenRouter API with DeepSeek R1 model
- **Responsive Design**: Works on desktop and mobile devices
- **Markdown Support**: Properly formatted responses with code syntax highlighting
- **Typing Indicators**: Animated dots while AI is thinking
- **Auto-resizing Input**: Textarea grows as you type
- **Keyboard Shortcuts**: Enter to send, Shift+Enter for new line

## 📁 Project Structure

```
wahaha/
├── index.html          # Main HTML file
├── css/
│   └── styles.css      # All styling and animations
├── js/
│   └── script.js       # Application logic and API calls
├── assets/             # Images, icons, and other assets
└── README.md           # Project documentation
```

## 🛠️ Setup Instructions

1. **Clone or Download** the project files
2. **Open `index.html`** in your web browser
3. **Start chatting!** No additional setup required

### Alternative Setup Methods:

**Method 1: Double-click**
- Navigate to the project folder
- Double-click `index.html`

**Method 2: Live Server (VS Code)**
- Install the "Live Server" extension in VS Code
- Right-click `index.html` → "Open with Live Server"

**Method 3: Python Server**
```bash
# Navigate to project directory
cd wahaha

# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Then open http://localhost:8000
```

## ⚙️ Configuration

The API configuration can be modified in `js/script.js`:

```javascript
const CONFIG = {
    API_URL: 'https://openrouter.ai/api/v1/chat/completions',
    API_KEY: 'your-api-key-here',
    MODEL: 'deepseek/deepseek-r1:free',
    SITE_NAME: 'SiteName',
    SITE_URL: 'https://www.sitename.com'
};
```

## 🎨 Customization

### Changing Colors
Edit `css/styles.css` to modify the color scheme:
- `#202123` - Sidebar background
- `#343541` - Main background
- `#444654` - Assistant message background
- `#5436da` - User avatar color
- `#19c37d` - Assistant avatar color

### Adding Features
- **Chat History**: Extend the sidebar functionality
- **File Uploads**: Add file input capabilities
- **Voice Input**: Integrate speech recognition
- **Export Chats**: Add download functionality

## 🔧 Dependencies

### External Libraries
- **Marked.js**: Markdown parsing for message formatting
- **Font Awesome**: Icons for the interface

### Browser Support
- Chrome/Chromium 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 📱 Mobile Responsiveness

The interface automatically adapts to mobile devices:
- Sidebar hides on screens < 768px
- Touch-friendly input areas
- Optimized spacing for mobile

## 🚨 Troubleshooting

### Common Issues

**API Errors**
- Check your internet connection
- Verify the API key is correct
- Ensure the OpenRouter service is available

**Styling Issues**
- Clear browser cache
- Check if CSS file is loading properly
- Verify file paths are correct

**JavaScript Errors**
- Open browser developer tools (F12)
- Check the console for error messages
- Ensure all files are in the correct directories

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the project.

---

**Built with ❤️ using vanilla web technologies**
