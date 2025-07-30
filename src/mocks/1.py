import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
})

# Data preparation - extracted from artifacts1.json
data = {
    'Model': [
        'Gemini-2.5-Pro',
        'Claude Sonnet 4 (20250514)',
        'o3-2025-04-16',
        'Claude 3.7 Sonnet (20250219)',
        'Qwen3-235B-A22B-Instruct-2507',
        'DeepSeek-R1-0528',
        'Kimi K2 Instruct',
        'Qwen3-Coder-480B-A35B-Instruct',
        'GPT-4.1-2025-04-14',
        'DeepSeek-V3-0324',
        'Qwen3-235B-A22B',
        'hunyuan-A13B',
        'Claude 3.5 Sonnet (20241022)',
        'KAT-V1'
    ],
    'Score': [
        57.74,
        57.28,
        54.04,
        51.32,
        50.62,
        47.73,
        47.65,
        47.15,
        45.95,
        43.50,
        41.09,
        40.95,
        39.85,
        35.21
    ],
    'Type': [
        'Closed-Source',  # Gemini-2.5-Pro
        'Closed-Source',  # Claude Sonnet 4 (20250514)
        'Closed-Source',  # o3-2025-04-16
        'Closed-Source',  # Claude 3.7 Sonnet (20250219)
        'Open-Source',    # Qwen3-235B-A22B-Instruct-2507
        'Open-Source',    # DeepSeek-R1-0528
        'Open-Source',    # Kimi K2 Instruct
        'Open-Source',    # Qwen3-Coder-480B-A35B-Instruct
        'Closed-Source',  # GPT-4.1-2025-04-14
        'Open-Source',    # DeepSeek-V3-0324
        'Open-Source',    # Qwen3-235B-A22B
        'Open-Source',    # hunyuan-A13B
        'Closed-Source',  # Claude 3.5 Sonnet (20241022)
        'Open-Source'     # KAT-V1
    ]
}

print(f"len(data['Model']) = {len(data['Model'])} | len(data['Score']) = {len(data['Score'])}")

df = pd.DataFrame(data)
df = df.sort_values(by='Score', ascending=False).reset_index(drop=True)

# Plot settings
grid_alpha = 0.4
bar_height = 0.6  # thinner bars for tighter spacing
colors_map = {'Closed-Source': '#4C72B0', 'Open-Source': '#55A868'}
colors = df['Type'].map(colors_map)

# Global font settings for a more polished look
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'axes.titlesize': 18,
    'axes.titleweight': 'semibold',
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10
})

# Create figure
total_bars = len(df)
fig_height = max(6, total_bars * 0.3)
fig, ax = plt.subplots(figsize=(10, fig_height))

# Draw bars
y_pos = np.arange(total_bars)
ax.barh(y=y_pos, width=df['Score'], height=bar_height, color=colors)
ax.invert_yaxis()  # highest score on top

# Specify x-axis start at 25
min_limit = 30 #25
max_limit = df['Score'].max() * 1.01
ax.set_xlim(min_limit, max_limit)

# Add a vertical line at the new baseline for emphasis
ax.axvline(min_limit, color='gray', linewidth=1, linestyle='--', alpha=0.7)

# Annotations: only annotate scores above the baseline
offset = max_limit * 0.005
for y, score in zip(y_pos, df['Score']):
    if score >= 30:
        ax.text(score + offset, y, f'{score:.2f}', va='center', fontsize=9)

# Title and labels - adjusted title position
ax.set_title(
    'ArtifactsBench: Overall Performance of Leading Models | Gemini-2.5-pro-Judge', 
    fontfamily='Arial',
    fontstyle='normal',
    pad=20,
    loc='left'  # Changed from default 'center' to 'left' to move title to the left
)
ax.set_xlabel('Overall Score (AVG)')
ax.set_yticks(y_pos)
ax.set_yticklabels(df['Model'])

# Grid and spines
ax.xaxis.grid(True, linestyle='--', alpha=grid_alpha)
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)

# Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color=colors_map['Closed-Source'], lw=4, label='Closed-Source'),
    Line2D([0], [0], color=colors_map['Open-Source'], lw=4, label='Open-Source')
]
ax.legend(handles=legend_elements, title='Model Type', loc='lower right', frameon=False)

plt.tight_layout()

# Save
os.makedirs('figures', exist_ok=True)
save_path = os.path.join('figures', 'main_results_overview_improved.png')
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"Plot saved successfully to {save_path}")