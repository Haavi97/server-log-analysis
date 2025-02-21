import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, ColorBar
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral6
import re
from datetime import datetime
from collections import defaultdict
import user_agents

def parse_log_line(line):
    pattern = r'(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+) "([^"]*)" "([^"]*)" (\d+)'
    match = re.match(pattern, line)
    if match:
        ip, remote_log_name, user_id, datetime_str, method, api, protocol, status, bytes_sent, referrer, ua_string, response_time = match.groups()
        
        # Parse datetime
        datetime_obj = datetime.strptime(datetime_str, '%d/%b/%Y:%H:%M:%S %z')
        
        # Parse user agent
        ua = user_agents.parse(ua_string)
        
        return {
            'ip': ip,
            'remote_log_name': remote_log_name,
            'user_id': user_id,
            'datetime': datetime_obj,
            'method': method,
            'api': api,
            'protocol': protocol,
            'status': int(status),
            'bytes_sent': int(bytes_sent),
            'referrer': referrer,
            'ua_string': ua_string,
            'browser': ua.browser.family,
            'os': ua.os.family,
            'device': ua.device.family,
            'response_time': int(response_time)
        }
    return None

def load_log_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            parsed = parse_log_line(line.strip())
            if parsed:
                data.append(parsed)
    return pd.DataFrame(data)

def create_time_series_plot(df, y_column, title):
    source = ColumnDataSource(df)
    p = figure(title=title, x_axis_type='datetime', height=300, width=800)
    p.line('datetime', y_column, source=source)
    p.xaxis.axis_label = 'Time'
    p.yaxis.axis_label = y_column.replace('_', ' ').title()
    return p

def create_bar_plot(df, column, title):
    # Convert to string for categorical axis
    df = df.copy()
    if column == 'status':
        df[column] = df[column].astype(str)
    
    counts = df[column].value_counts()
    # Convert index to strings for categorical axis
    counts.index = counts.index.astype(str)
    
    source = ColumnDataSource(pd.DataFrame({'category': counts.index, 'count': counts.values}))
    
    # Create categorical range from string values
    p = figure(title=title, x_range=counts.index.tolist(), height=300, width=800)
    p.vbar(x='category', top='count', width=0.9, source=source,
           fill_color=factor_cmap('category', Spectral6[:len(counts.index)], counts.index.tolist()))
    
    p.xaxis.axis_label = column.replace('_', ' ').title()
    p.yaxis.axis_label = 'Count'
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label_text_font_size = "12pt"
    p.xaxis.major_label_orientation = 0.7
    
    return p

def main():
    st.set_page_config(layout="wide", page_title="Server Log Analysis")
    
    st.title("Server Log Analysis Dashboard")
    
    # Sidebar
    st.sidebar.header("Analytics Controls")
    
    # File uploader
    uploaded_file = st.sidebar.file_uploader("Upload log file", type=['log', 'txt'])
    
    if uploaded_file is not None:
        # Create a temporary file to store the uploaded content
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_filepath = tmp_file.name
            
        # Load and parse data
        df = load_log_data(tmp_filepath)
        
        # Clean up the temporary file
        import os
        os.unlink(tmp_filepath)
        
        # Time range filter
        st.sidebar.subheader("Time Range")
        date_range = st.sidebar.date_input(
            "Select date range",
            [df['datetime'].dt.date.min(), df['datetime'].dt.date.max()]
        )
        
        # Status code filter
        status_codes = st.sidebar.multiselect(
            "Filter by Status Code",
            options=sorted(df['status'].unique()),
            default=sorted(df['status'].unique())
        )
        
        # Request method filter
        methods = st.sidebar.multiselect(
            "Filter by Request Method",
            options=sorted(df['method'].unique()),
            default=sorted(df['method'].unique())
        )
        
        # Apply filters using pandas operations
        mask = (
            (df['datetime'].dt.date >= pd.Timestamp(date_range[0])) &
            (df['datetime'].dt.date <= pd.Timestamp(date_range[1])) &
            (df['status'].isin(status_codes)) &
            (df['method'].isin(methods))
        )
        filtered_df = df[mask]
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Time Series Analysis")
            
            # Response time over time
            st.bokeh_chart(create_time_series_plot(
                filtered_df,
                'response_time',
                'Response Time Over Time'
            ))
            
            # Requests per hour
            hourly_requests = filtered_df.groupby(
                filtered_df['datetime'].dt.floor('H')
            ).size().reset_index(name='count')
            st.bokeh_chart(create_time_series_plot(
                hourly_requests,
                'count',
                'Requests per Hour'
            ))
        
        with col2:
            st.subheader("Request Analysis")
            
            # Status code distribution
            st.bokeh_chart(create_bar_plot(
                filtered_df,
                'status',
                'Status Code Distribution'
            ))
            
            # Method distribution
            st.bokeh_chart(create_bar_plot(
                filtered_df,
                'method',
                'Request Method Distribution'
            ))
        
        # Additional metrics
        st.subheader("Key Metrics")
        col3, col4, col5 = st.columns(3)
        
        with col3:
            st.metric(
                "Average Response Time",
                f"{filtered_df['response_time'].mean():.2f} ms"
            )
        
        with col4:
            st.metric(
                "Total Requests",
                len(filtered_df)
            )
        
        with col5:
            success_rate = (filtered_df['status'].apply(lambda x: x < 400).mean()) * 100
            st.metric(
                "Success Rate",
                f"{success_rate:.1f}%"
            )
        
        # Detailed tables
        st.subheader("Top APIs")
        top_apis = filtered_df['api'].value_counts().head(10)
        st.table(pd.DataFrame({
            'API': top_apis.index,
            'Count': top_apis.values
        }))
        
        st.subheader("Browser Distribution")
        browser_dist = filtered_df['browser'].value_counts().head(10)
        st.table(pd.DataFrame({
            'Browser': browser_dist.index,
            'Count': browser_dist.values
        }))

if __name__ == "__main__":
    main()