# Server Log Analysis Dashboard 📊

A powerful and interactive dashboard built with Streamlit and Bokeh for analyzing server logs. This project includes both the dashboard application and a test log file generator for development and testing purposes.

![Python](https://img.shields.io/badge/python-v3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.29-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)


## 🌟 Features

- Real-time log analysis with interactive visualizations
- Time series analysis of response times and request frequency
- Status code distribution analysis
- Request method distribution
- Browser and OS analytics
- Customizable date range filtering
- Status code and request method filtering
- Export capabilities for analyzed data
- Test log file generator for development

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/server-log-analysis.git
cd server-log-analysis
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## 📊 Running the Dashboard

1. Start the Streamlit server:
```bash
streamlit run server_log_dashboard.py
```

2. Open your browser and navigate to:
```
http://localhost:8501
```

## 🔧 Generating Test Log Files

The repository includes a test file generator (`test_file_generator.py`) that creates sample log files for testing and development.

1. To generate test logs:
```bash
python test_file_generator.py --lines 1000
```

Parameters:
- `--lines`: Number of log entries to generate (default: 1000)

The generator will create a file with the specified number of log entries in the correct format for the dashboard.

## 📦 Project Structure

```
server-log-analysis/
├── log_dashboard.py        # Main dashboard application
├── test_file_generator.py  # Test log file generator
├── requirements.txt        # Project dependencies
├── README.md              # Project documentation
└── sample_logs/           # Directory for generated test logs
```

## 🚀 Deploying to Streamlit Cloud

1. Create an account on [Streamlit Cloud](https://streamlit.io/cloud)

2. Connect your GitHub repository to Streamlit Cloud

3. Deploy your app:
   - Select your repository
   - Choose the main file as `server_log_dashboard.py`
   - Click "Deploy"

Your app will be available at: `https://share.streamlit.io/yourusername/server-log-analysis/main/log_dashboard.py`

## 🌍 Live Demo

Check out the live demo of the dashboard here: [Server Log Analysis Dashboard](https://your-demo-link-here)

## 📝 Requirements

Create a `requirements.txt` file with the following content:

```txt
streamlit==1.32.0
bokeh==3.3.4
pandas==2.2.1
user-agents==2.2.0
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - For the amazing web app framework
- [Bokeh](https://bokeh.org/) - For powerful visualizations
- [Pandas](https://pandas.pydata.org/) - For data manipulation capabilities

## 📞 Support

For support and questions, please open an issue in the GitHub repository.
