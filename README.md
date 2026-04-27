# Smart Study Planner 🧠

A premium, SaaS-style dashboard built with Python and Streamlit that optimizes study schedules using a **Dynamic Greedy Algorithm**.

![Dashboard Preview](https://raw.githubusercontent.com/your-username/smart-study-planner/main/preview.png)

## 🚀 Features

- **Dynamic Greedy Scheduling**: Allocates study hours based on difficulty, urgency, and a fairness penalty to prevent subject burnout.
- **SaaS Dashboard UI**: Dark-themed, glassmorphic interface with color-coded metric cards and interactive intensity heatmaps.
- **Resource Analytics**: Donut charts for time distribution and real-time utilization metrics.
- **Interactive Syllabus**: Add subjects dynamically and re-generate your plan instantly.
- **Exportable Plans**: Download your optimized schedule as a CSV file.

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit, Custom CSS
- **Visualization**: Plotly Express
- **Logic/Algorithm**: Python (Dynamic Greedy Heuristic)
- **Data Processing**: Pandas

## 🧠 Algorithmic Thinking

The system uses a **Dynamic Greedy Algorithm** to solve the scheduling problem:
1. **Priority Heuristic**: `(Difficulty * 3) + (20 / DaysLeft)`.
2. **Progress Penalty**: Every hour allocated to a subject reduces its priority temporarily, ensuring **Fairness** across the syllabus.
3. **Complexity**: $O(n \log n)$ for sorting, making it instantaneous for real-world usage.

## 📦 Installation & Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/smart-study-planner.git
   cd smart-study-planner
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
